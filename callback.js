// FDM Community - Discord OAuth Callback Handler

// Configuration
const DISCORD_CLIENT_ID = "1393406406865977477";
const DISCORD_REDIRECT_URI = window.location.origin + "/callback.html";

// State management
let authCode = null;
let error = null;
let loading = true;

// DOM elements
const loadingState = document.getElementById('loading-state');
const successState = document.getElementById('success-state');
const errorState = document.getElementById('error-state');
const authCodeElement = document.getElementById('auth-code');
const errorMessageElement = document.getElementById('error-message');
const retryAuthBtn = document.getElementById('retry-auth-btn');
const returnHomeBtn = document.getElementById('return-home-btn');

// Utility functions
function getURLParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function showState(state) {
    // Hide all states
    loadingState.style.display = 'none';
    successState.style.display = 'none';
    errorState.style.display = 'none';
    
    // Show requested state
    state.style.display = 'block';
}

function handleDiscordAuth() {
    const discordAuthUrl = `https://discord.com/api/oauth2/authorize?client_id=${DISCORD_CLIENT_ID}&redirect_uri=${encodeURIComponent(DISCORD_REDIRECT_URI)}&response_type=code&scope=identify`;
    window.location.href = discordAuthUrl;
}

function returnHome() {
    window.location.href = "./";
}

// Process OAuth callback
function processCallback() {
    const code = getURLParameter('code');
    const errorParam = getURLParameter('error');
    
    if (errorParam) {
        error = 'Connexion annulée ou refusée';
        loading = false;
        showError();
        return;
    }
    
    if (code) {
        authCode = code;
        // Simulate processing delay
        setTimeout(() => {
            loading = false;
            showSuccess();
            
            // Auto-redirect after 3 seconds
            setTimeout(() => {
                returnHome();
            }, 3000);
        }, 2000);
    } else {
        error = 'Code d\'autorisation manquant';
        loading = false;
        showError();
    }
}

function showSuccess() {
    showState(successState);
    
    if (authCodeElement && authCode) {
        authCodeElement.textContent = `Code: ${authCode.substring(0, 20)}...`;
    }
    
    console.log('Discord auth code received:', authCode);
    
    // Here you would typically:
    // 1. Send the code to your backend
    // 2. Backend exchanges code for access token
    // 3. Backend fetches user info from Discord
    // 4. Backend creates/updates user session
    // 5. Redirect to authenticated area
}

function showError() {
    showState(errorState);
    
    if (errorMessageElement) {
        errorMessageElement.textContent = error;
    }
}

// Event handlers
function initEventHandlers() {
    if (retryAuthBtn) {
        retryAuthBtn.addEventListener('click', handleDiscordAuth);
    }
    
    if (returnHomeBtn) {
        returnHomeBtn.addEventListener('click', returnHome);
    }
}

// Initialize the callback page
function initCallback() {
    // Show loading state initially
    showState(loadingState);
    
    // Initialize event handlers
    initEventHandlers();
    
    // Process the callback
    processCallback();
    
    console.log('🔗 Discord OAuth callback handler initialized');
}

// Wait for DOM to be fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCallback);
} else {
    initCallback();
}