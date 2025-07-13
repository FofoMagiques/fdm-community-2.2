const express = require("express");
const session = require("express-session");
const axios = require("axios");
const cookieParser = require("cookie-parser");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cookieParser());
app.use(session({
    secret: process.env.SESSION_SECRET || "fdm-super-secret",
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false, // Passe à true si HTTPS
        httpOnly: true,
        maxAge: 1000 * 60 * 60 * 24 // 1 jour
    }
}));

app.use(express.static("public")); // Pour servir tes fichiers frontend

// Récupérer les infos de l'utilisateur connecté
app.get("/api/user", (req, res) => {
    if (req.session.user) {
        res.json(req.session.user);
    } else {
        res.status(401).json({ error: "Non connecté" });
    }
});

// Callback OAuth2 Discord
app.get("/api/callback", async (req, res) => {
    const code = req.query.code;
    if (!code) return res.redirect("/");

    try {
        // Échange du code contre un token
        const tokenResponse = await axios.post("https://discord.com/api/oauth2/token", new URLSearchParams({
            client_id: process.env.DISCORD_CLIENT_ID,
            client_secret: process.env.DISCORD_CLIENT_SECRET,
            grant_type: "authorization_code",
            code: code,
            redirect_uri: process.env.DISCORD_REDIRECT_URI
        }), {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        });

        const access_token = tokenResponse.data.access_token;

        // Récupère les infos de l'utilisateur
        const userResponse = await axios.get("https://discord.com/api/users/@me", {
            headers: {
                Authorization: `Bearer ${access_token}`
            }
        });

        // Sauvegarde en session
        req.session.user = {
            id: userResponse.data.id,
            username: userResponse.data.username,
            avatar: userResponse.data.avatar
        };

        // Redirige vers la homepage
        res.redirect("/");
    } catch (error) {
        console.error("Erreur OAuth:", error.message);
        res.redirect("/error.html");
    }
});

// Déconnexion
app.get("/logout", (req, res) => {
    req.session.destroy(() => {
        res.clearCookie("connect.sid");
        res.redirect("/");
    });
});

app.listen(PORT, () => console.log(`🌍 Serveur lancé sur http://localhost:${PORT}`));
