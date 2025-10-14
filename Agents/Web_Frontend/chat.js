// Configuration - À MODIFIER selon votre setup
const CONFIG = {
    PARLANT_API_URL: 'http://localhost:8000/api/v1',
    AGENT_ID: 'YOUR_AGENT_ID', // À remplacer après création de l'agent
    CUSTOMER_ID: 'customer-demo-123', // ID du client/patient
};

// État de l'application
let sessionId = null;
let isProcessing = false;

// Éléments DOM
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');
const connectionStatus = document.getElementById('connection-status');
const quickActionBtns = document.querySelectorAll('.quick-action-btn');

// Initialiser la session au chargement
async function initializeSession() {
    try {
        showConnectionStatus('connecting');
        
        // Créer une nouvelle session Parlant
        const response = await fetch(
            `${CONFIG.PARLANT_API_URL}/agents/${CONFIG.AGENT_ID}/sessions`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    customer_id: CONFIG.CUSTOMER_ID,
                    metadata: {
                        source: 'web_frontend',
                        timestamp: new Date().toISOString()
                    }
                })
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        sessionId = data.id;
        
        console.log('✅ Session Parlant initialisée:', sessionId);
        showConnectionStatus('connected');
        
    } catch (error) {
        console.error('❌ Erreur initialisation session:', error);
        showConnectionStatus('error');
        addSystemMessage(
            '⚠️ Impossible de se connecter au serveur Parlant. ' +
            'Vérifiez que le serveur est démarré sur ' + CONFIG.PARLANT_API_URL
        );
    }
}

// Envoyer un message à l'agent
async function sendMessage(message) {
    if (!sessionId) {
        addSystemMessage('⚠️ Session non initialisée. Tentative de reconnexion...');
        await initializeSession();
        if (!sessionId) return;
    }

    if (isProcessing) {
        console.log('Message en cours de traitement, veuillez patienter');
        return;
    }

    try {
        isProcessing = true;
        showTypingIndicator();
        disableInput(true);

        const response = await fetch(
            `${CONFIG.PARLANT_API_URL}/agents/${CONFIG.AGENT_ID}/sessions/${sessionId}/messages`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    kind: 'message',
                    source: 'user'
                })
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        console.log('📥 Réponse Parlant:', data);

        hideTypingIndicator();

        // Extraire le texte de la réponse
        let responseText = '';
        let toolUsed = null;

        // Parcourir les événements pour trouver la réponse et les tools
        if (data.events && Array.isArray(data.events)) {
            // Chercher les tool calls
            const toolCalls = data.events.filter(e => e.kind === 'tool_call');
            if (toolCalls.length > 0) {
                toolUsed = toolCalls[0].tool_name;
                console.log('🔧 Tool utilisé:', toolUsed);
            }

            // Chercher le message de l'agent
            const agentMessages = data.events.filter(e => 
                e.kind === 'agent_message' || e.kind === 'message'
            );
            
            if (agentMessages.length > 0) {
                responseText = agentMessages[agentMessages.length - 1].message || 
                              agentMessages[agentMessages.length - 1].content ||
                              '';
            }
        }

        // Fallback si pas trouvé dans events
        if (!responseText && data.message) {
            responseText = data.message;
        }
        if (!responseText && data.response) {
            responseText = data.response;
        }

        // Afficher la réponse
        if (responseText) {
            addAgentMessage(responseText, toolUsed);
        } else {
            console.warn('Aucune réponse trouvée dans:', data);
            addSystemMessage('⚠️ Réponse reçue mais format inattendu. Voir console.');
        }

    } catch (error) {
        console.error('❌ Erreur envoi message:', error);
        hideTypingIndicator();
        
        if (error.message.includes('404')) {
            addSystemMessage(
                '❌ Agent non trouvé. Vérifiez que AGENT_ID est correct dans chat.js'
            );
        } else if (error.message.includes('Failed to fetch')) {
            addSystemMessage(
                '❌ Impossible de contacter le serveur. Vérifiez que Parlant est démarré.'
            );
            showConnectionStatus('error');
        } else {
            addSystemMessage('❌ Erreur: ' + error.message);
        }
    } finally {
        isProcessing = false;
        disableInput(false);
    }
}

// Ajouter un message utilisateur
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(message)}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
        <div class="message-avatar">👤</div>
    `;
    
    chatMessages.insertBefore(messageDiv, typingIndicator);
    scrollToBottom();
}

// Ajouter un message agent
function addAgentMessage(message, toolUsed = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent';
    
    let toolIndicator = '';
    if (toolUsed) {
        const toolInfo = getToolInfo(toolUsed);
        toolIndicator = `
            <div class="tool-indicator">
                <span class="tool-icon">${toolInfo.icon} ${toolInfo.label}</span>
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-bubble">
                ${formatMessage(message)}
            </div>
            ${toolIndicator}
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.insertBefore(messageDiv, typingIndicator);
    scrollToBottom();
}

// Ajouter un message système
function addSystemMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(message)}</div>
        </div>
    `;
    
    chatMessages.insertBefore(messageDiv, typingIndicator);
    scrollToBottom();
}

// Obtenir les infos d'un tool
function getToolInfo(toolName) {
    const tools = {
        'qna': { icon: '📚', label: 'Réponse FAQ' },
        'sql_query': { icon: '🗄️', label: 'Base de données' },
        'get_upcoming_slots': { icon: '📅', label: 'Créneaux disponibles' },
        'schedule_appointment': { icon: '✅', label: 'Rendez-vous confirmé' },
        'get_lab_results': { icon: '🔬', label: 'Résultats d\'analyses' },
    };
    
    return tools[toolName] || { icon: '🔧', label: 'Outil' };
}

// Afficher/masquer l'indicateur de frappe
function showTypingIndicator() {
    typingIndicator.classList.add('show');
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.classList.remove('show');
}

// Gérer le statut de connexion
function showConnectionStatus(status) {
    const statusElement = connectionStatus;
    
    switch(status) {
        case 'connected':
            statusElement.style.background = '#4ade80';
            break;
        case 'connecting':
            statusElement.style.background = '#fbbf24';
            break;
        case 'error':
            statusElement.style.background = '#ef4444';
            break;
    }
}

// Activer/désactiver l'input
function disableInput(disabled) {
    userInput.disabled = disabled;
    sendButton.disabled = disabled;
    quickActionBtns.forEach(btn => btn.disabled = disabled);
}

// Formater le message (Markdown basique + HTML safe)
function formatMessage(text) {
    return escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>')
        .replace(/`(.*?)`/g, '<code>$1</code>');
}

// Échapper HTML pour éviter XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Obtenir l'heure actuelle formatée
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Scroll automatique vers le bas
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Gérer la soumission du formulaire
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message || isProcessing) return;
    
    // Ajouter le message de l'utilisateur
    addUserMessage(message);
    
    // Vider l'input
    userInput.value = '';
    
    // Envoyer le message
    await sendMessage(message);
    
    // Refocus sur l'input
    userInput.focus();
});

// Gérer les boutons d'actions rapides
quickActionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const message = btn.getAttribute('data-message');
        if (message && !isProcessing) {
            userInput.value = message;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
});

// Gérer la touche Enter (sans Shift)
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Initialiser au chargement de la page
window.addEventListener('load', async () => {
    console.log('🚀 Initialisation du frontend Parlant...');
    console.log('📍 API URL:', CONFIG.PARLANT_API_URL);
    console.log('🤖 Agent ID:', CONFIG.AGENT_ID);
    
    // Vérifier la configuration
    if (CONFIG.AGENT_ID === 'YOUR_AGENT_ID') {
        addSystemMessage(
            '⚠️ Configuration requise: Veuillez mettre à jour AGENT_ID dans chat.js ' +
            'après avoir exécuté setup_agent.py'
        );
        disableInput(true);
        return;
    }
    
    // Initialiser la session
    await initializeSession();
    
    // Focus sur l'input
    userInput.focus();
});

// Gérer la déconnexion/rechargement
window.addEventListener('beforeunload', () => {
    if (sessionId) {
        console.log('👋 Fermeture de la session:', sessionId);
        // Optionnel: Appeler une API pour clore la session proprement
    }
});

