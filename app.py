from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import time

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# FLASK SETUP
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# GEMINI SETUP
# =========================================================

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "FitBuddy Backend is running!",
        "ai_configured": bool(API_KEY)
    })


# =========================================================
# GENERATE FITNESS PLAN
# =========================================================

@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    # -----------------------------------------------------
    # Check API key
    # -----------------------------------------------------

    if not client:

        return jsonify({
            "success": False,
            "error": "Gemini API key is not configured."
        }), 500


    # -----------------------------------------------------
    # Get JSON data
    # -----------------------------------------------------

    data = request.get_json(silent=True) or {}


    # -----------------------------------------------------
    # Read user information
    # -----------------------------------------------------

    age = data.get("age")
    height = data.get("height")
    weight = data.get("weight")
    goal = data.get("goal")
    fitness_level = data.get("fitness_level")


    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if not all([
        age,
        height,
        weight,
        goal,
        fitness_level
    ]):

        return jsonify({
            "success": False,
            "error": "Please fill in all fitness details."
        }), 400


    # =====================================================
    # AI PROMPT
    # =====================================================

    prompt = f"""
You are FitBuddy, a friendly AI fitness planning assistant.

Create a simple and practical fitness plan for this user.

USER INFORMATION
----------------
Age: {age}
Height: {height} cm
Weight: {weight} kg
Fitness Goal: {goal}
Fitness Level: {fitness_level}

Create the plan using these sections:

1. GOAL SUMMARY

Explain the user's selected fitness goal briefly.

2. 7-DAY WORKOUT PLAN

Monday:
Tuesday:
Wednesday:
Thursday:
Friday:
Saturday:
Sunday:

Keep the exercises appropriate for the user's fitness level.

3. HEALTHY FOOD SUGGESTIONS

Give simple healthy food suggestions.

4. WATER AND REST

Give basic hydration and sleep/rest suggestions.

5. SAFETY TIPS

Give simple safety advice.

IMPORTANT:
- Keep the answer simple.
- Do not recommend medication.
- Do not recommend extreme dieting.
- Do not recommend dangerous exercises.
- Do not make medical diagnoses.
- This is general fitness information.
- Tell users with medical conditions to consult a qualified healthcare professional.
"""


    # =====================================================
    # GEMINI MODELS
    # =====================================================

    models = [
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.8-flash"
    ]


    last_error = None


    # =====================================================
    # TRY GEMINI MODELS
    # =====================================================

    for model_name in models:

        print("----------------------------------------")
        print("Trying model:", model_name)
        print("----------------------------------------")

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )


            # ------------------------------------------------
            # Check response
            # ------------------------------------------------

            if response and response.text:

                print("SUCCESS:", model_name)

                return jsonify({
                    "success": True,
                    "model": model_name,
                    "plan": response.text
                })


        except Exception as error:

            last_error = str(error)

            print("FAILED:", model_name)
            print(last_error)

            # Small delay before next model
            time.sleep(1)

            continue


    # =====================================================
    # ALL MODELS FAILED
    # =====================================================

    print("All Gemini models failed.")

    return jsonify({
        "success": False,
        "error": "Gemini is currently unavailable. Please try again.",
        "details": last_error
    }), 503


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )