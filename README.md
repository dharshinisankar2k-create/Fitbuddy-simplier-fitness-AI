# FitBuddy - AI Fitness Plan Generator

A simple academic project that uses a Flask backend and Gemini to generate
personalized, general fitness plans.

## Project Structure

FitBuddy/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   └── Procfile
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js

## Run Backend

Open a terminal:

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_key_here
```

Start:

```bash
python app.py
```

Backend:
http://127.0.0.1:5000

## Run Frontend

Open `frontend/index.html` in a browser for a simple local test.
For best local development, use the VS Code Live Server extension.

The frontend currently calls:

http://127.0.0.1:5000

After deploying the backend, change `API_URL` in `frontend/script.js`
to the public backend URL.

## Important

Never commit `.env` or expose your Gemini API key in frontend JavaScript.

This application provides general fitness information and is not a substitute
for advice from a qualified healthcare professional.
# Fitbuddy-simplier-fitness-AI
