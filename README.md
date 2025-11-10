# 🔮 SHADOW WHISPER - Haunted AI Chat

*A terrifying Halloween experience powered by quantum-entangled AI*

![Halloween Theme](https://img.shields.io/badge/Theme-Haunted%20Halloween-ff6b00?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-black?style=for-the-badge)

## 🎃 Live Demo

Experience the horror live: **[https://halloween-chat.onrender.com/](https://halloween-chat.onrender.com/)**

*Deployed on Render.com for seamless performance*

## 📖 About This Project

Welcome to **SHADOW WHISPER**, where reality bends and shadows speak! This haunted chat application creates a truly terrifying Halloween experience through advanced AI and atmospheric design.

**⚠️ WARNING**: This application is designed for thrill-seekers and horror enthusiasts. Proceed with caution!

## ✨ Features

- **👻 Haunted AI Chat**: Converse with SHADOW WHISPER, an entity from beyond
- **🔊 Voice of the Damned**: Text-to-speech with FREE Google TTS
- **📍 Location-Based Terror**: Automatic city detection with personalized scary predictions
- **🎨 Dark Halloween UI**: Animated ghosts, bats, and floating text elements
- **⚡ 100% FREE**: No API costs, no subscriptions, completely open source
- **🌍 Cross-Platform**: Works on all devices and dimensions

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Internet connection

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/shadow-whisper.git
cd shadow-whisper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Launch the application**
```bash
python app.py
```
4. **Visit the experience** → http://127.0.0.1:5000

**Deployment on Render.com**

We successfully deployed this project on Render.com. Use this configuration:

```bash
# render.yaml
services:
  - type: web
    name: shadow-whisper
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

**🔮 API Integration**

**FREE AI Backend - MLVOCA DeepSeek**
```python
# No API keys needed
payload = {
    "model": "deepseek-r1:1.5b",
    "prompt": "You are a haunted AI spirit..."
}
```
**FREE Text-to-Speech - Google TTS**
```python
# Converts text to atmospheric voice
tts = gTTS(text=scary_message, lang='en')
```

**🎭 Usage Examples**
```bash
// Ask questions like:
- "What awaits me tonight?"
- "Tell me a Halloween story"
- "Who's watching me?"
- "What's my fate?"
```

⚡ Features

Dynamic Name System

· Randomly assigns atmospheric names: "Lost Soul", "Doomed Wanderer", "Cursed One"
· Personalized experience for each visitor

Location-Based Predictions

· Automatically detects user's city
· Generates customized scary predictions
· Uses Markov chains for unique responses

Animated Atmosphere

· Floating ghosts and bats
· Atmospheric sound effects
· Glowing text animations
· Crystal ball predictions

🔧 Configuration

Environment Variables

```bash
SECRET_KEY=your-secret-key-here
```

Customization

· Modify VICTIM_NAMES in app.py for new identities
· Add more predictions in generate_scary_prediction()
· Customize CSS in static/style.css for different themes

Remember: The shadows are always watching! 🎃👻💀

**Questions?**

Ask me questions at @amirrezahmi2002@gmail.com.
