// FDM Community - Main JavaScript

// Configuration Discord OAuth
const DISCORD_CLIENT_ID = "1393406406865977477";
const DISCORD_REDIRECT_URI = "http://teamfdm.fr/FDM/callback.html";

// Events data
const events = [
    {
        id: 1,
        title: "Serveur Minecraft RP - Collaboration",
        date: "2025-03-01",
        time: "20:00",
        description: "Lancement de notre serveur Minecraft RP en collaboration avec un autre serveur ! Télécharge notre launcher custom pour une expérience unique avec des mods exclusifs.",
        category: "Gaming",
        participants: 25,
        maxParticipants: 50,
        status: "upcoming",
        hasDownload: true,
        downloadText: "Télécharger le launcher"
    }
];

// State management
let participatingEvents = new Set();

document.getElementById("discord-auth-btn").addEventListener("click", async () => {
    try {
        // Demande au backend l'URL d'auth Discord
        const response = await fetch("/api/auth/discord");
        if (!response.ok) throw new Error("Erreur lors de la récupération de l'URL OAuth");

        const data = await response.json();

        // Redirige vers Discord pour l'authentification
        window.location.href = data.auth_url;
    } catch (err) {
        console.error(err);
        alert("Impossible de se connecter pour le moment.");
    }
});

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function getCategoryClass(category) {
    const categoryClasses = {
        Gaming: "badge-gaming",
        Esport: "badge-esport",
        Social: "badge-social",
        Créatif: "badge-creative"
    };
    return categoryClasses[category] || "badge-gaming";
}

function getStatusClass(status) {
    const statusClasses = {
        upcoming: "badge-upcoming",
        ongoing: "badge-ongoing",
        past: "badge-past"
    };
    return statusClasses[status] || "badge-upcoming";
}

function getStatusText(status) {
    const statusTexts = {
        upcoming: "À venir",
        ongoing: "En cours",
        past: "Terminé"
    };
    return statusTexts[status] || "Inconnu";
}

// Event handling functions
function handleDiscordAuth() {
    const discordAuthUrl = `https://discord.com/api/oauth2/authorize?client_id=${DISCORD_CLIENT_ID}&redirect_uri=${encodeURIComponent(DISCORD_REDIRECT_URI)}&response_type=code&scope=identify`;
    window.location.href = discordAuthUrl;
}

function handleJoinServer() {
    // Placeholder for Discord server invite link
    // Replace with your actual Discord invite link
    window.open("https://discord.gg/uamaVGnVJ2", "_blank");
}

function handleParticipate(eventId, eventTitle) {
    if (participatingEvents.has(eventId)) {
        participatingEvents.delete(eventId);
        showNotification(`Participation annulée pour "${eventTitle}"`, "info");
    } else {
        participatingEvents.add(eventId);
        showNotification(`Participation confirmée pour "${eventTitle}"`, "success");
    }
    updateEventButtons();
    
    // Save to localStorage
    localStorage.setItem('fdm_participating_events', JSON.stringify(Array.from(participatingEvents)));
}

function handleDownload(eventTitle) {
    // Placeholder for launcher download
    showNotification("Le launcher sera bientôt disponible ! 🚀", "info");
    console.log(`Téléchargement du launcher pour "${eventTitle}"`);
}

function updateEventButtons() {
    const participateButtons = document.querySelectorAll('[data-event-id]');
    participateButtons.forEach(button => {
        const eventId = parseInt(button.dataset.eventId);
        if (participatingEvents.has(eventId)) {
            button.textContent = "✓ Inscrit";
            button.className = "btn btn-participating";
        } else {
            button.textContent = "Participer";
            button.className = "btn btn-participate";
        }
    });
}

// Notification system
function showNotification(message, type = "info") {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${type === 'success' ? 'var(--fdm-green)' : type === 'error' ? '#f44336' : 'var(--fdm-pink)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        max-width: 300px;
        animation: slideIn 0.3s ease;
    `;

    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .notification-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }
        .notification-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            padding: 0;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    `;
    document.head.appendChild(style);

    // Add to page
    document.body.appendChild(notification);

    // Add close functionality
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', () => {
        notification.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Render events
function renderEvents() {
    const upcomingEvents = events.filter(event => event.status === 'upcoming');
    const upcomingEventsContainer = document.getElementById('upcoming-events');
    const noEventsContainer = document.getElementById('no-events');

    if (upcomingEvents.length === 0) {
        document.querySelector('.events-upcoming').style.display = 'none';
        noEventsContainer.style.display = 'block';
        return;
    }

    document.querySelector('.events-upcoming').style.display = 'block';
    noEventsContainer.style.display = 'none';

    upcomingEventsContainer.innerHTML = upcomingEvents.map(event => {
        const isParticipating = participatingEvents.has(event.id);
        return `
            <div class="event-card">
                <div class="event-header">
                    <span class="event-badge ${getCategoryClass(event.category)}">${event.category}</span>
                    <span class="event-badge ${getStatusClass(event.status)}">${getStatusText(event.status)}</span>
                </div>
                
                <h3 class="event-title">${event.title}</h3>
                
                <div class="event-meta">
                    <div class="event-meta-item">
                        <span>📅</span>
                        <span>${formatDate(event.date)}</span>
                    </div>
                    <div class="event-meta-item">
                        <span>🕐</span>
                        <span>${event.time}</span>
                    </div>
                </div>
                
                <p class="event-description">${event.description}</p>
                
                <div class="event-stats">
                    <span>👥 ${event.participants} participants</span>
                    ${event.maxParticipants ? `<span>Max: ${event.maxParticipants}</span>` : ''}
                </div>
                
                <div class="event-actions">
                    <button 
                        class="btn ${isParticipating ? 'btn-participating' : 'btn-participate'}" 
                        data-event-id="${event.id}"
                        onclick="handleParticipate(${event.id}, '${event.title}')"
                    >
                        ${isParticipating ? '✓ Inscrit' : 'Participer'}
                    </button>
                    
                    ${event.hasDownload ? `
                        <button 
                            class="btn btn-download" 
                            onclick="handleDownload('${event.title}')"
                        >
                            📥 ${event.downloadText}
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// Load saved participating events from localStorage
function loadParticipatingEvents() {
    try {
        const saved = localStorage.getItem('fdm_participating_events');
        if (saved) {
            const eventIds = JSON.parse(saved);
            participatingEvents = new Set(eventIds);
        }
    } catch (error) {
        console.error('Error loading participating events:', error);
        participatingEvents = new Set();
    }
}

// Smooth scroll functionality
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize animations on scroll
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.stat-card, .event-card, .server-info-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

async function checkUserAuth() {
    try {
        const res = await fetch("/api/user");
        if (!res.ok) throw new Error();

        const user = await res.json();

        // Affiche les infos dans l'interface
        const authBtn = document.getElementById("discord-auth-btn");
        if (authBtn) {
            authBtn.innerHTML = `<img src="https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png?size=32" style="border-radius:50%;width:1.5rem;height:1.5rem;margin-right:0.5rem;"> ${user.username}`;
            authBtn.disabled = true;
        }
    } catch (err) {
        // L'utilisateur n'est pas connecté
        console.log("Utilisateur non connecté");
    }
}

// Initialize the application
function initApp() {
    // Load saved data
    loadParticipatingEvents();
    
    // Render events
    renderEvents();
    
    // Bind event handlers
    const discordAuthBtn = document.getElementById('discord-auth-btn');
    if (discordAuthBtn) {
        discordAuthBtn.addEventListener('click', handleDiscordAuth);
    }
    
    const joinServerBtn = document.getElementById('join-server-btn');
    if (joinServerBtn) {
        joinServerBtn.addEventListener('click', handleJoinServer);
    }
    
    // Initialize other features
    initSmoothScroll();
    initScrollAnimations();
    checkUserAuth();
    
    console.log('🎮 FDM Community website initialized!');
}

// Wait for DOM to be fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}