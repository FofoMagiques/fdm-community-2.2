from fastapi import FastAPI, HTTPException, Depends, Request, Response, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
import uuid
import jwt
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configuration
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
SESSION_SECRET = os.environ.get('SESSION_SECRET')
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')
DISCORD_GUILD_ID = os.environ.get('DISCORD_GUILD_ID')
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

# Admin user IDs
ADMIN_USER_IDS = ["449682043404812288"]

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Create the main app
app = FastAPI(title="FDM Community API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Pydantic models
class User(BaseModel):
    id: str
    username: str
    discriminator: str
    avatar: Optional[str] = None
    email: Optional[str] = None
    is_admin: bool = False
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    discord_id: str
    username: str
    discriminator: str
    avatar: Optional[str] = None
    email: Optional[str] = None

class ServerStats(BaseModel):
    member_count: int
    online_count: int
    boost_count: int
    channel_count: int
    role_count: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LoginResponse(BaseModel):
    access_token: str
    user: User

# Utility functions
def create_access_token(user_id: str) -> str:
    """Create JWT access token"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SESSION_SECRET, algorithm="HS256")

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(token, SESSION_SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from token"""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_doc = await db.users.find_one({"id": user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user_doc)

async def get_discord_user_info(access_token: str) -> Dict[str, Any]:
    """Get user info from Discord API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")
        return response.json()

async def get_discord_guilds(access_token: str) -> List[Dict[str, Any]]:
    """Get user's Discord guilds"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://discord.com/api/v10/users/@me/guilds",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            return []
        return response.json()

async def get_discord_server_stats() -> ServerStats:
    """Get Discord server statistics"""
    if not DISCORD_BOT_TOKEN or not DISCORD_GUILD_ID:
        return ServerStats(
            member_count=0,
            online_count=0,
            boost_count=0,
            channel_count=0,
            role_count=0
        )
    
    async with httpx.AsyncClient() as client:
        try:
            # Get guild info
            guild_response = await client.get(
                f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}",
                headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
            )
            
            if guild_response.status_code != 200:
                logger.error(f"Failed to fetch guild info: {guild_response.status_code}")
                return ServerStats(member_count=0, online_count=0, boost_count=0, channel_count=0, role_count=0)
            
            guild_data = guild_response.json()
            
            # Get channels
            channels_response = await client.get(
                f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/channels",
                headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
            )
            
            channels_data = channels_response.json() if channels_response.status_code == 200 else []
            
            # Get roles
            roles_response = await client.get(
                f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/roles",
                headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
            )
            
            roles_data = roles_response.json() if roles_response.status_code == 200 else []
            
            return ServerStats(
                member_count=guild_data.get("member_count", 0),
                online_count=guild_data.get("approximate_presence_count", 0),
                boost_count=guild_data.get("premium_subscription_count", 0),
                channel_count=len(channels_data),
                role_count=len(roles_data)
            )
            
        except Exception as e:
            logger.error(f"Error fetching Discord stats: {e}")
            return ServerStats(member_count=0, online_count=0, boost_count=0, channel_count=0, role_count=0)

# Routes
@api_router.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FDM Community API"}

@api_router.get("/auth/discord")
async def discord_auth():
    """Initiate Discord OAuth"""
    discord_oauth_url = (
        f"https://discord.com/api/oauth2/authorize?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=identify%20email%20guilds"
    )
    return {"url": discord_oauth_url}

@api_router.get("/auth/callback")
async def discord_callback(code: str, request: Request):
    """Handle Discord OAuth callback"""
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_response = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        
        token_data = token_response.json()
        access_token = token_data["access_token"]
        
        # Get user info
        user_info = await get_discord_user_info(access_token)
        
        # Check if user is in the Discord server
        guilds = await get_discord_guilds(access_token)
        is_in_server = any(guild["id"] == DISCORD_GUILD_ID for guild in guilds)
        
        if not is_in_server:
            raise HTTPException(status_code=403, detail="You must be a member of the FDM Discord server")
        
        # Create or update user
        user_id = user_info["id"]
        is_admin = user_id in ADMIN_USER_IDS
        
        user_doc = {
            "id": user_id,
            "username": user_info["username"],
            "discriminator": user_info.get("discriminator", "0000"),
            "avatar": user_info.get("avatar"),
            "email": user_info.get("email"),
            "is_admin": is_admin,
            "last_login": datetime.utcnow()
        }
        
        # Update or insert user
        await db.users.update_one(
            {"id": user_id},
            {"$set": user_doc, "$setOnInsert": {"joined_at": datetime.utcnow()}},
            upsert=True
        )
        
        # Create access token
        jwt_token = create_access_token(user_id)
        
        # Set session
        request.session["user_id"] = user_id
        request.session["access_token"] = jwt_token
        
        return {"access_token": jwt_token, "user": user_doc}

@api_router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@api_router.post("/auth/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return {"message": "Logged out successfully"}

@api_router.get("/stats")
async def get_stats():
    """Get Discord server statistics"""
    stats = await get_discord_server_stats()
    return stats

@api_router.get("/users")
async def get_users(current_user: User = Depends(get_current_user)):
    """Get all users (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = await db.users.find().to_list(1000)
    return [User(**user) for user in users]

@api_router.get("/users/{user_id}")
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    """Get user by ID"""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user_doc = await db.users.find_one({"id": user_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user_doc)

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    """Delete user (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.users.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

@api_router.get("/admin/dashboard")
async def admin_dashboard(current_user: User = Depends(get_current_user)):
    """Get admin dashboard data"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get user statistics
    total_users = await db.users.count_documents({})
    admin_users = await db.users.count_documents({"is_admin": True})
    
    # Get recent users
    recent_users = await db.users.find().sort("joined_at", -1).limit(10).to_list(10)
    
    # Get server stats
    server_stats = await get_discord_server_stats()
    
    return {
        "total_users": total_users,
        "admin_users": admin_users,
        "recent_users": [User(**user) for user in recent_users],
        "server_stats": server_stats
    }

# Include the router in the main app
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    """Shutdown database client"""
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)