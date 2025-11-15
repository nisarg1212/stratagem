import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables (for Replit Secrets)
load_dotenv()

app = Flask(__name__)

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except AttributeError:
    print("----------------------------------------")
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please add your API key to Replit Secrets.")
    print("It should be named 'GEMINI_API_KEY'")
    print("----------------------------------------")
    model = None
except Exception as e:
    print(f"Error configuring AI: {e}")
    model = None

# --- AI Genius Prompts ---

GENIUS_PROMPTS = {
    "flaw": """
    You are a skeptical professor and a master of critical thinking.
    Your task is to analyze the following text and find its weaknesses.
    Do NOT summarize the text.
    Instead, identify the 3-5 weakest arguments, logical fallacies, hidden assumptions, or unanswered questions.
    Present your analysis in a clear, numbered list.

    TEXT TO ANALYZE:
    {text}
    """,
    "quiz": """
    You are a Socratic tutor. Your goal is to make a student think, not just recall facts.
    Based on the following text, generate a 5-question quiz.
    Do NOT ask simple fact-recall questions (e.g., "What is...?").
    Ask "Why," "How," and "What if" questions that test deep, conceptual understanding.

    Example Good Question: "How might the author's primary assumption lead to an incorrect conclusion in a different context?"
    Example Bad Question: "What year did the event take place?"

    TEXT TO ANALYZE:
    {text}
    """,
    "connect": """
    You are a creative polymath, a master of connecting disparate ideas.
    Your task is to read the following text and connect its main idea to a completely different, seemingly unrelated field
    (e.g., connect biology to economics, or history to computer science).
    Explain the connection in a compelling, "aha!" moment paragraph.

    TEXT TO ANALYZE:
    {text}
    """
}

# --- Flask Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """The API endpoint for AI analysis."""
    if not model:
        return jsonify({"error": "AI model is not configured. Check API key."}), 500
        
    try:
        data = request.get_json()
        user_text = data.get('text')
        analysis_mode = data.get('mode')

        if not user_text or not analysis_mode:
            return jsonify({"error": "Missing 'text' or 'mode'"}), 400

        if analysis_mode not in GENIUS_PROMPTS:
            return jsonify({"error": "Invalid 'mode'"}), 400

        # Format the chosen prompt with the user's text
        prompt_template = GENIUS_PROMPTS[analysis_mode]
        final_prompt = prompt_template.format(text=user_text)
        
        # Send to Gemini
        response = model.generate_content(final_prompt)
        
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error during analysis: {e}")
        return jsonify({"error": f"An internal error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
