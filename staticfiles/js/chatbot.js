// Chatbot functionality
class Chatbot {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.toggleBtn = document.getElementById('chatbot-toggle');
        this.chatWindow = document.getElementById('chatbot-window');
        this.closeBtn = document.getElementById('chatbot-close');
        this.input = document.getElementById('chatbot-input');
        this.sendBtn = document.getElementById('chatbot-send');
        this.messagesContainer = document.getElementById('chatbot-messages');

        this.bindEvents();
    }

    bindEvents() {
        // Toggle chatbot
        this.toggleBtn.addEventListener('click', () => this.toggle());
        
        // Close chatbot
        this.closeBtn.addEventListener('click', () => this.close());
        
        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Send on Enter key
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize input
        this.input.addEventListener('input', () => {
            this.input.style.height = 'auto';
            this.input.style.height = this.input.scrollHeight + 'px';
        });
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.chatWindow.classList.add('active');
        this.isOpen = true;
        this.input.focus();
        this.scrollToBottom();
    }

    close() {
        this.chatWindow.classList.remove('active');
        this.isOpen = false;
    }

    async sendMessage() {
        const message = this.input.value.trim();
        if (!message || this.isLoading) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.input.value = '';
        this.input.style.height = 'auto';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove typing indicator
            this.hideTypingIndicator();

            if (response.ok) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                console.error('Chatbot error:', data.error);
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection and try again.', 'bot');
            console.error('Network error:', error);
        }
    }

    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        if (sender === 'bot') {
            const icon = document.createElement('i');
            icon.className = 'bi bi-robot';
            messageContent.appendChild(icon);
        }

        const text = document.createElement('p');
        text.textContent = content;
        messageContent.appendChild(text);

        messageDiv.appendChild(messageContent);
        this.messagesContainer.appendChild(messageDiv);

        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.isLoading = true;
        this.sendBtn.disabled = true;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typing-indicator';

        const typingContent = document.createElement('div');
        typingContent.className = 'typing-indicator';

        for (let i = 0; i < 3; i++) {
            const span = document.createElement('span');
            typingContent.appendChild(span);
        }

        typingDiv.appendChild(typingContent);
        this.messagesContainer.appendChild(typingDiv);

        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isLoading = false;
        this.sendBtn.disabled = false;

        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});
