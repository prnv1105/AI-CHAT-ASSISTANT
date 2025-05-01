from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("Missing OPENROUTER_API_KEY in .env file")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    print("\n=== Incoming Request ===")
    print("Headers:", request.headers)
    try:
        data = request.get_json()
        print("Request Data:", data)

        # Ensure data structure is correct
        if not data or 'messages' not in data or not data['messages']:
            return jsonify({'error': 'Invalid request format'}), 400

        # Safely get the last message
        last_message = data['messages'][-1]
        user_message = last_message.get('content', '').lower()  # Safely get content

        creator_questions = [
            "who made you",
            "who created you", 
            "who built you",
            "who developed you",
            "who is your creator",
            "who is your developer",
            "who programmed you",
            "who build you",
            "who is your creator",
            "who made you", "who created you", "who build you", "who developed you",
            "who is your creator", "who is your developer", "who programmed you",
            "who designed you", "who owns you", "who is behind you", "who is your dev",
            "who is your father", "who is your maker", "tell me about your creator",
            "who built this ai", "who made this chatbot", "who is pranav",
            "who are you made by", "who are you created by", "who are you developed by",
            "who is responsible for you", "who can i thank for you", "who gets credit for you"

        ]
        
        if any(question in user_message for question in creator_questions):
            return jsonify({'content': "I am developed by Pranav"})
        
        response = client.chat.completions.create(
            model=data.get('model', 'mistralai/mistral-7b-instruct'),
            messages=data['messages']
        )
        
        result = response.choices[0].message.content
        print("Response:", result[:100] + "...")
        return jsonify({'content': result})
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)