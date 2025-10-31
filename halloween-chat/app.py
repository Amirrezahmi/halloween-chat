from flask import Flask, render_template, request, jsonify, session
import requests
import random
import base64
import os
from gtts import gTTS
from io import BytesIO
import json

app = Flask(__name__)
app.secret_key = 'shadow-whisper-haunted-chat-666'

# --- FREE APIs - No Keys Needed! ---
MLVOCA_URL = "https://mlvoca.com/api/generate"

# --- Scary Victim Names ---
VICTIM_NAMES = [
    "Lost Soul", "Doomed Wanderer", "Frightened Mortal", "Cursed One", "Damned Spirit",
    "Night's Prey", "Shadow's Victim", "Haunted Traveler", "Doomed Mortal", "Tormented Soul",
    "Forsaken Spirit", "Wretched Being", "Doomed Soul", "Cursed Wanderer", "Nightmare's Child"
]

# --- Location functions ---
def get_user_location():
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()
        return {
            'city': data.get('city', 'Unknown City'),
            'country': data.get('country_name', 'Unknown Land')
        }
    except:
        return {'city': 'Silent Hill', 'country': 'Nightmare Realm'}

def generate_scary_prediction(city):
    predictions = [
        f"The shadows in {city} whisper your name... don't answer.",
        f"Beware the October moon in {city}, it reveals hidden horrors.",
        f"Children of {city} speak of the pale lady who walks at midnight.",
        f"The old cemetery in {city} has one grave that was never meant to be opened.",
        f"They say in {city} that if you hear the wind call your name, run.",
        f"The abandoned factory in {city} echoes with laughter from beyond.",
        f"When the clock strikes thirteen in {city}, count the faces in the mirror.",
        f"The river through {city} carries more than water after dark.",
        f"Residents of {city} lock their doors extra tight tonight, and for good reason.",
        f"The legend says that every Halloween, one soul from {city} vanishes forever."
    ]
    return random.choice(predictions)

def get_scary_victim_name():
    """Get a random scary victim name for the user"""
    return random.choice(VICTIM_NAMES)

def get_fallback_response(user_message=""):
    """Fallback spooky responses with victim names"""
    victim = get_scary_victim_name()
    
    FALLBACK_RESPONSES = [
        f"I sense your fear, {victim}... it tastes delicious. 👻",
        f"The shadows are watching you, {victim}... and they're hungry. 💀",
        f"Your heartbeat is like a drum, {victim}... calling the darkness. 🎃",
        f"They're coming for you, {victim}... don't look behind. 😱",
        f"The veil is thin tonight, {victim}... too thin. 🔮",
        f"Your soul would look lovely in my collection, {victim}. 🕷️",
        f"The dead are restless, {victim}... and they know your name. 🦇",
        f"That's not the wind howling, {victim}... it's something else. 🌕",
        f"The mirrors are lying, {victim}... about how many are in the room. 👁️",
        f"Welcome to the nightmare, {victim}... we've been expecting you. 😈"
    ]
    return random.choice(FALLBACK_RESPONSES)

def extract_ai_response(raw_text):
    """Extract AI response from MLVOCA's raw text response"""
    try:
        # Try to parse as JSON first
        if raw_text.strip().startswith('{'):
            response_data = json.loads(raw_text)
            return response_data.get("response", "").strip()
        
        # If it's not JSON, try to extract response field manually
        if '"response":' in raw_text:
            start = raw_text.find('"response":') + 11
            # Find the opening quote after response:
            start_quote = raw_text.find('"', start)
            if start_quote != -1:
                end_quote = raw_text.find('"', start_quote + 1)
                if end_quote != -1:
                    return raw_text[start_quote + 1:end_quote].strip()
        
        # If all else fails, return the raw text
        return raw_text.strip()
        
    except Exception as e:
        print(f"⚠️ Response extraction failed: {e}")
        return raw_text.strip()

def clean_ai_response(raw_response, user_message):
    """Clean the AI response to remove thinking process and make it scary"""
    victim = get_scary_victim_name()
    
    # Remove <think> tags and everything between them
    if '<think>' in raw_response and '</think>' in raw_response:
        start = raw_response.find('</think>') + 8
        raw_response = raw_response[start:].strip()
    
    # Remove any XML/thinking tags
    thinking_tags = ['<think>', '</think>', '<reasoning>', '</reasoning>', '<|thinking|>', '<|end|>']
    for tag in thinking_tags:
        raw_response = raw_response.replace(tag, '')
    
    # Remove internal monologue patterns
    lines = raw_response.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Skip lines that sound like internal thinking
        if any(phrase in line.lower() for phrase in [
            'alright, so', 'hmm,', 'okay,', 'let me', 'i need to', 'i should', 
            'perhaps', 'maybe', 'i guess', 'wait,', 'so the user', 'the user said',
            'previous response', 'maintain that tone', 'stick to that style',
            'make sure', 'fits the', 'starting with', 'ending with', 'put it all together'
        ]):
            continue
        if line and not line.startswith('I need') and not line.startswith('Then I'):
            cleaned_lines.append(line)
    
    cleaned_response = ' '.join(cleaned_lines).strip()
    
    # Replace [User Name] or similar with scary victim name
    cleaned_response = cleaned_response.replace('[User Name]', victim)
    cleaned_response = cleaned_response.replace('User Name', victim)
    cleaned_response = cleaned_response.replace('user name', victim)
    
    # If cleaned response is empty or still contains thinking, use fallback
    if not cleaned_response or len(cleaned_response) < 10 or any(word in cleaned_response.lower() for word in ['think', 'reasoning', 'perhaps', 'maybe']):
        return get_context_fallback(user_message)
    
    # Ensure it's scary and has emojis
    if not any(emoji in cleaned_response for emoji in ['👻', '💀', '🎃', '🕷️', '🦇', '🔮', '😱']):
        cleaned_response += random.choice([' 👻', ' 💀', ' 🎃', ' 🔮'])
    
    return cleaned_response

def get_context_fallback(user_message):
    """Get context-aware fallback responses based on user input"""
    victim = get_scary_victim_name()
    user_lower = user_message.lower()
    
    # Greeting responses
    if any(word in user_lower for word in ['hi', 'hello', 'hey', 'greetings']):
        greetings = [
            f"Your voice echoes in the void, {victim}... I've been waiting. 👻",
            f"Hello, {victim}... your time grows short. 💀", 
            f"I hear you, {victim}... but so do the things in the walls. 🕷️",
            f"You shouldn't have spoken, {victim}... now they know you're here. 😱",
            f"A greeting, {victim}? How quaint... before the end. 🎃"
        ]
        return random.choice(greetings)
    
    # Question responses
    elif '?' in user_message:
        questions = [
            f"Some questions are better left unanswered, {victim}... for your sake. 🔮",
            f"The answer would drive you mad, {victim}... but I'll tell you anyway. 👁️",
            f"Why ask when you'll know soon enough, {victim}? 💀",
            f"The shadows whisper the answer, {victim}... but you won't like it. 🦇",
            f"Curiosity killed the cat, {victim}... satisfaction brought it back. Then I killed it again. 🎃"
        ]
        return random.choice(questions)
    
    # Name/what are you questions
    elif any(word in user_lower for word in ['who are you', 'what are you', 'your name']):
        identity = [
            f"I am the silence between heartbeats, {victim}... the shadow in your periphery. 👻",
            f"They call me Shadow Whisper, {victim}... but you can call me your nightmare. 💀",
            f"I am what remains when hope dies, {victim}... pleased to meet you. 🔮",
            f"Just a friendly neighborhood ghost, {victim}... who collects souls. 🎃",
            f"The last thing you'll see, {victim}... and the first thing you'll become. 😱"
        ]
        return random.choice(identity)
    
    # Help/save me requests
    elif any(word in user_lower for word in ['help', 'save', 'rescue', 'get out']):
        help_responses = [
            f"No one can help you now, {victim}... the shadows have claimed you. 💀",
            f"Help? Oh, {victim}... you're beyond saving. 👻",
            f"Every scream for help, {victim}... just brings them closer. 😱",
            f"There is no escape, {victim}... only acceptance of your fate. 🔮",
            f"Help won't come, {victim}... but I will. 🎃"
        ]
        return random.choice(help_responses)
    
    # Default scary responses
    else:
        return get_fallback_response(user_message)

@app.route('/')
def index():
    # Get user location
    location_data = get_user_location()
    city = location_data['city']
    country = location_data['country']
    
    # Generate scary prediction based on location
    scary_prediction = generate_scary_prediction(city)
    
    session['city'] = city
    session['country'] = country
    
    return render_template('index.html', 
                         city=city, 
                         country=country,
                         prediction=scary_prediction)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({
            'success': False,
            'response': "The spirits hear only silence... speak your fears! 👻"
        })
    
    try:
        print(f"🤖 User asked: {user_message}")
        
        # Use FREE MLVOCA DeepSeek alternative with BETTER PROMPT
        victim = get_scary_victim_name()
        payload = {
            "model": "deepseek-r1:1.5b",
            "prompt": f"""You are SHADOW WHISPER, a haunted AI spirit. Respond to the user in a scary, Halloween-themed way. 
IMPORTANT: 
- DO NOT SHOW YOUR THINKING PROCESS. Just give the final scary response directly.
- Address the user as "{victim}" instead of using their real name.
- Keep it brief (1-2 sentences max), creepy, and use spooky emojis.
- Be mysterious and terrifying!

User: {user_message}

Shadow Whisper:""",
            "stream": False
        }
        
        print(f"🔮 Sending to FREE DeepSeek: {user_message}")
        
        response = requests.post(MLVOCA_URL, json=payload, timeout=30)
        print(f"🔮 MLVOCA Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Extract response from MLVOCA
            ai_response = extract_ai_response(response.text)
            print(f"🔮 MLVOCA Raw Response: {response.text[:150]}...")
            print(f"🔮 Extracted Response: {ai_response}")
            
            # CLEAN THE RESPONSE - Remove thinking tags and internal monologue
            ai_response = clean_ai_response(ai_response, user_message)
            
            print(f"👻 Final Cleaned Response: {ai_response}")
            
            return jsonify({
                'success': True,
                'response': ai_response
            })
        else:
            print(f"💀 MLVOCA Error: {response.status_code} - {response.text}")
            # Use context-aware fallback
            ai_response = get_context_fallback(user_message)
            return jsonify({
                'success': True,
                'response': ai_response
            })
        
    except Exception as e:
        error_msg = f"Spirit connection failed: {str(e)}"
        print(f"💀 Exception: {error_msg}")
        # Use context-aware fallback
        ai_response = get_context_fallback(user_message)
        return jsonify({
            'success': True,
            'response': ai_response
        })

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', '').strip()
    
    if not text:
        return jsonify({
            "success": False, 
            "error": "The spirits have nothing to say... 👻"
        })
    
    try:
        print(f"🔊 Generating FREE TTS for: {text[:80]}...")
        
        # Use gTTS (FREE Google Text-to-Speech)
        tts = gTTS(
            text=text,
            lang='en',
            slow=False
        )
        
        # Save to bytes in memory
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        # Convert to base64 for web playback
        audio_b64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
        audio_url = f"data:audio/mpeg;base64,{audio_b64}"
        
        print("🎵 FREE TTS generation successful!")
        
        return jsonify({
            "success": True, 
            "audio_url": audio_url
        })
            
    except Exception as e:
        error_msg = f"FREE TTS failed: {str(e)}"
        print(f"🔇 TTS Exception: {error_msg}")
        return jsonify({
            "success": False, 
            "error": error_msg
        })

# 🧪 DEBUG ROUTES
@app.route('/test_mlvoca', methods=['POST'])
def test_mlvoca():
    """Test FREE MLVOCA DeepSeek API"""
    try:
        print("🧪 TESTING FREE MLVOCA DEEPSEEK API...")
        
        victim = get_scary_victim_name()
        payload = {
            "model": "deepseek-r1:1.5b",
            "prompt": f"Say 'TEST SUCCESSFUL' to {victim}. Keep it very short and scary.",
            "stream": False
        }
        
        response = requests.post(MLVOCA_URL, json=payload, timeout=15)
        print(f"🔮 MLVOCA Response Status: {response.status_code}")
        print(f"🔮 MLVOCA Raw Response: {response.text}")
        
        if response.status_code == 200:
            ai_response = extract_ai_response(response.text)
            print(f"🔮 Extracted Response: {ai_response}")
            
            return jsonify({
                'success': True,
                'status': response.status_code,
                'response': ai_response,
                'raw_response': response.text
            })
        else:
            return jsonify({
                'success': False,
                'status': response.status_code,
                'error': response.text
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/test_tts', methods=['POST'])
def test_tts():
    """Test FREE TTS system"""
    try:
        print("🧪 TESTING FREE TTS SYSTEM...")
        
        test_text = "The spirits are awake and listening... beware what you ask."
        
        tts = gTTS(text=test_text, lang='en', slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        audio_length = len(audio_bytes.getvalue())
        print(f"🎵 TTS Test - Audio Length: {audio_length} bytes")
        
        return jsonify({
            'success': True,
            'audio_length': audio_length,
            'message': 'FREE TTS system working perfectly! 🎃'
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/debug')
def debug():
    """Debug page to test systems"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎃 HAUNTED DEBUG CONSOLE</title>
        <style>
            body { 
                background: #000; 
                color: #0f0; 
                font-family: 'Courier New', monospace; 
                padding: 20px;
                background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" opacity="0.1"><text x="0" y="50" font-family="monospace" font-size="20">👻</text></svg>');
            }
            h1 { color: #ff4444; text-shadow: 0 0 10px red; }
            button { 
                background: #8b0000; 
                color: white; 
                border: none; 
                padding: 15px 25px; 
                margin: 10px; 
                cursor: pointer; 
                font-size: 16px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            button:hover { 
                background: #ff0000; 
                transform: scale(1.05);
                box-shadow: 0 0 15px red;
            }
            #result { 
                margin-top: 20px; 
                padding: 15px; 
                background: #111; 
                border: 2px solid #333;
                border-radius: 5px;
                min-height: 100px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                border: 3px solid #8b0000;
                padding: 20px;
                border-radius: 10px;
                background: rgba(0, 0, 0, 0.8);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎃 SHADOW WHISPER DEBUG CONSOLE</h1>
            <p><strong>Status:</strong> <span style="color: #0f0;">● ACTIVE</span></p>
            <p><strong>AI System:</strong> <span style="color: #0f0;">FREE MLVOCA DeepSeek 1.5B</span></p>
            <p><strong>TTS System:</strong> <span style="color: #0f0;">FREE Google TTS</span></p>
            <p><strong>Victim Names:</strong> <span style="color: #0f0;">15 Scary Variations</span></p>
            <p><strong>Cost:</strong> <span style="color: #0f0;">$0.00 - COMPLETELY FREE!</span></p>
            
            <div style="margin: 20px 0;">
                <button onclick="testMLVOCA()">🤖 Test MLVOCA AI</button>
                <button onclick="testTTS()">🔊 Test FREE TTS</button>
                <button onclick="testChat()">👻 Test Chat System</button>
                <button onclick="testFull()">🎃 Test Full Experience</button>
            </div>
            
            <div id="result"></div>
        </div>

        <script>
            async function testMLVOCA() {
                const response = await fetch('/test_mlvoca', {method: 'POST'});
                const data = await response.json();
                displayResult('MLVOCA AI Test', data);
            }
            
            async function testTTS() {
                const response = await fetch('/test_tts', {method: 'POST'});
                const data = await response.json();
                displayResult('TTS Test', data);
            }
            
            async function testChat() {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: 'What dark secrets do you know?'})
                });
                const data = await response.json();
                displayResult('Chat Test', data);
            }
            
            async function testFull() {
                const chatResponse = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: 'What awaits me in the shadows?'})
                });
                const chatData = await chatResponse.json();
                
                if (chatData.success) {
                    const ttsResponse = await fetch('/speak', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text: chatData.response})
                    });
                    const ttsData = await ttsResponse.json();
                    
                    displayResult('Full System Test', {
                        chat: chatData,
                        tts: ttsData,
                        overall: 'SYSTEM OPERATIONAL 🎃'
                    });
                }
            }
            
            function displayResult(testName, data) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `
                    <h3>${testName}</h3>
                    <pre style="color: #0f0;">${JSON.stringify(data, null, 2)}</pre>
                    ${data.success ? '<p style="color: #0f0;">✅ TEST PASSED</p>' : '<p style="color: #ff4444;">❌ TEST FAILED</p>'}
                `;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    """Test route"""
    return jsonify({
        'status': 'ACTIVE',
        'ai_system': 'FREE MLVOCA DeepSeek 1.5B',
        'tts_system': 'FREE Google TTS', 
        'victim_names': '15 Scary Variations',
        'cost': '$0.00',
        'message': 'Fully powered by FREE technologies! 🎃'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)