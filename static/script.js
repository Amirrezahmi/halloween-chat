class HauntedChat {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.audioPlayer = document.getElementById('audioPlayer');
        
        this.initEventListeners();
        this.addSpookyEffects();
    }
    
    initEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage(data.response, 'ai');
            } else {
                this.addMessage('The spirits are too restless to respond...', 'ai');
            }
            
        } catch (error) {
            this.addMessage('The veil between worlds is too thick... Try again.', 'ai');
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = text;
        
        messageContent.appendChild(messageText);
        messageDiv.appendChild(messageContent);
        
        if (sender === 'ai') {
            const speakBtn = document.createElement('button');
            speakBtn.className = 'speak-btn';
            speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
            speakBtn.onclick = () => this.speakText(text);
            messageDiv.appendChild(speakBtn);
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        // Add typing effect for AI messages
        if (sender === 'ai') {
            this.typeWriterEffect(messageText, text);
        }
    }
    
    typeWriterEffect(element, text) {
        element.textContent = '';
        let i = 0;
        
        const typing = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            } else {
                clearInterval(typing);
            }
        }, 20);
    }
    
    async speakText(text) {
        try {
            const response = await fetch('/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.audioPlayer.src = data.audio_url;
                this.audioPlayer.play();
            }
        } catch (error) {
            console.error('Speech error:', error);
        }
    }
    
    addSpookyEffects() {
        // Random creepy sounds occasionally
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% chance every 30 seconds
                this.playCreepySound();
            }
        }, 30000);
        
        // Floating text effect
        this.createFloatingText();
    }
    
    playCreepySound() {
        // Simple creepy sound using audio context
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(50, audioContext.currentTime + 1);
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 1);
    }
    
    createFloatingText() {
        const texts = ['BEWARE', 'HE IS WATCHING', 'DONT LOOK BACK', 'THEY ARE HERE'];
        setInterval(() => {
            if (Math.random() < 0.3) {
                const text = texts[Math.floor(Math.random() * texts.length)];
                this.showFloatingText(text);
            }
        }, 10000);
    }
    
    showFloatingText(text) {
        const floatingText = document.createElement('div');
        floatingText.textContent = text;
        floatingText.style.cssText = `
            position: fixed;
            top: ${Math.random() * 80 + 10}%;
            left: ${Math.random() * 80 + 10}%;
            color: #ff0000;
            font-family: 'Creepster', cursive;
            font-size: 1.5rem;
            opacity: 0;
            pointer-events: none;
            z-index: 1000;
            text-shadow: 0 0 10px red;
            animation: floatText 3s ease-in-out;
        `;
        
        document.body.appendChild(floatingText);
        
        setTimeout(() => {
            document.body.removeChild(floatingText);
        }, 3000);
    }
}

// Add floating text animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes floatText {
        0% { opacity: 0; transform: translateY(0) scale(0.5); }
        50% { opacity: 1; transform: translateY(-50px) scale(1); }
        100% { opacity: 0; transform: translateY(-100px) scale(0.5); }
    }
`;
document.head.appendChild(style);

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    new HauntedChat();
});

// Global function for speak buttons in initial message
function speakText(text) {
    const chat = new HauntedChat();
    chat.speakText(text);
}