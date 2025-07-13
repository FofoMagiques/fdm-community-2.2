import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth Context
const AuthContext = React.createContext();

// Auth Provider Component
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get(`${API}/auth/me`);
        setUser(response.data);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('access_token');
      delete axios.defaults.headers.common['Authorization'];
    } finally {
      setLoading(false);
    }
  };

  const login = async () => {
    try {
      const response = await axios.get(`${API}/auth/discord`);
      window.location.href = response.data.url;
    } catch (error) {
      console.error('Login failed:', error);
      alert('Erreur lors de la connexion Discord');
    }
  };

  const logout = async () => {
    try {
      await axios.post(`${API}/auth/logout`);
      localStorage.removeItem('access_token');
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook to use auth context
const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Loading Component
function LoadingSpinner() {
  return (
    <div className="loading-screen">
      <div className="loading-spinner"></div>
    </div>
  );
}

// Main Landing Page Component (Your Original Design)
function LandingPage() {
  const { user, login, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [onlineCount, setOnlineCount] = useState(95);

  useEffect(() => {
    fetchStats();
    // Update online count every 30 seconds
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/stats`);
      setStats(response.data);
      setOnlineCount(response.data.member_count || 95);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleJoinServer = () => {
    window.open("https://discord.gg/uamaVGnVJ2", "_blank");
  };

  return (
    <div className="fdm-landing">
      {/* Header */}
      <header className="fdm-header">
        <div className="fdm-logo-section">
          <img src="/image/Logo FDM V3.png" alt="FDM Logo" className="fdm-logo" />
          <span className="fdm-logo-text">FDM</span>
        </div>
        
        <div className="fdm-auth-section">
          {user ? (
            <div className="fdm-user-info">
              <div className="fdm-user-details">
                {user.avatar && (
                  <img 
                    src={`https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`}
                    alt="Avatar"
                    className="fdm-user-avatar"
                  />
                )}
                <span className="fdm-user-name">{user.username}</span>
                {user.is_admin && <span className="fdm-admin-badge">Admin</span>}
              </div>
              <button onClick={logout} className="fdm-logout-btn">
                Déconnexion
              </button>
            </div>
          ) : (
            <button onClick={login} className="fdm-discord-btn">
              🎮 Se connecter avec Discord
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="fdm-main">
        {/* Hero Section */}
        <section className="fdm-hero">
          <img src="/image/Logo FDM V3.png" alt="Logo FDM" className="fdm-hero-logo" />
          <h1 className="fdm-hero-title">Bienvenue sur FDM</h1>
          <p className="fdm-hero-description">
            Le serveur Discord des amis ! Né au lycée, FDM est devenu une communauté soudée où on se retrouve pour jouer ensemble, rigoler et passer de bons moments. Que tu sois là depuis le début ou nouveau, tu es le bienvenu !
          </p>
          
          <button onClick={handleJoinServer} className="fdm-join-btn">
            📞 Rejoindre le serveur
          </button>
          
          <div className="fdm-online-count">
            <span className="fdm-online-text">Plus de </span>
            <span className="fdm-online-number">{onlineCount}</span>
            <span className="fdm-online-text"> amis connectés</span>
          </div>
        </section>

        {/* Server Profile Section */}
        <section className="fdm-server-profile">
          <h2 className="fdm-section-title">Profil du serveur FDM</h2>
          <p className="fdm-section-subtitle">Une bande d'amis unis par le gaming</p>
          
          <div className="fdm-stats-grid">
            <div className="fdm-stat-card">
              <div className="fdm-stat-icon">👥</div>
              <div className="fdm-stat-number">{stats?.member_count || 95}</div>
              <div className="fdm-stat-label">Membres totaux</div>
            </div>
            
            <div className="fdm-stat-card">
              <div className="fdm-stat-icon">🟢</div>
              <div className="fdm-stat-number">{stats?.online_count || 12}</div>
              <div className="fdm-stat-label">En ligne maintenant</div>
            </div>
            
            <div className="fdm-stat-card">
              <div className="fdm-stat-icon">📅</div>
              <div className="fdm-stat-number">{stats?.boost_count || 1}</div>
              <div className="fdm-stat-label">Événements ce mois</div>
            </div>
            
            <div className="fdm-stat-card">
              <div className="fdm-stat-icon">⭐</div>
              <div className="fdm-stat-number">Feb 2020</div>
              <div className="fdm-stat-label">Depuis</div>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section className="fdm-about">
          <h2 className="fdm-about-title">📖 À propos de FDM</h2>
          <div className="fdm-about-content">
            <p>
              FDM (Fils De Mec) est née d'une amitié de lycée qui a grandi pour devenir une vraie communauté. 
              Nous sommes un groupe d'amis passionnés de gaming, de discussions et de bons moments partagés.
            </p>
            <p>
              Que tu sois fan de jeux vidéo, de discussions nocturnes ou simplement à la recherche d'une communauté bienveillante, 
              FDM est faite pour toi ! Rejoins-nous et découvre une famille numérique qui t'attend.
            </p>
          </div>
        </section>

        {/* Admin Panel for logged in admins */}
        {user && user.is_admin && (
          <section className="fdm-admin-panel">
            <h2 className="fdm-section-title">🔧 Panel Administrateur</h2>
            <div className="fdm-admin-grid">
              <div className="fdm-admin-card">
                <h3>Gestion des utilisateurs</h3>
                <p>Gérer les membres de la communauté</p>
                <div className="fdm-admin-stats">
                  <span>Utilisateurs connectés: {stats?.member_count || 0}</span>
                </div>
              </div>
              <div className="fdm-admin-card">
                <h3>Statistiques serveur</h3>
                <p>Statistiques détaillées du serveur Discord</p>
                <div className="fdm-admin-stats">
                  <span>Salons: {stats?.channel_count || 0}</span><br />
                  <span>Rôles: {stats?.role_count || 0}</span>
                </div>
              </div>
              <div className="fdm-admin-card">
                <h3>Configuration</h3>
                <p>Paramètres et configuration du site</p>
                <div className="fdm-admin-stats">
                  <span>Boosts: {stats?.boost_count || 0}</span>
                </div>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

// Callback Component
function CallbackPage() {
  const [processing, setProcessing] = useState(true);

  useEffect(() => {
    handleCallback();
  }, []);

  const handleCallback = async () => {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      
      if (code) {
        const response = await axios.get(`${API}/auth/callback?code=${code}`);
        const { access_token, user } = response.data;
        
        localStorage.setItem('access_token', access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        window.location.href = '/';
      } else {
        throw new Error('No code received');
      }
    } catch (error) {
      console.error('Callback failed:', error);
      alert('Erreur lors de la connexion. Veuillez réessayer.');
      window.location.href = '/';
    } finally {
      setProcessing(false);
    }
  };

  if (processing) {
    return (
      <div className="fdm-callback-processing">
        <div className="fdm-callback-content">
          <img src="/image/Logo FDM V3.png" alt="FDM Logo" className="fdm-callback-logo" />
          <div className="loading-spinner"></div>
          <p className="fdm-callback-message">Connexion en cours...</p>
        </div>
      </div>
    );
  }

  return <Navigate to="/" replace />;
}

// Main App Component
function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/callback" element={<CallbackPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;