# 🌸 Sahaara AI — Streamlit Prototype

Sahaara AI is a multi-agent prototype designed to help women understand how they can use their existing education, skills, experience, and interests for realistic learning, flexible work, freelancing, or small-scale entrepreneurship pathways.

## Agent workflow

1. **User Profile Agent** — structures the user's background.
2. **Opportunity Matching Agent** — identifies relevant opportunities.
3. **Skill Development Agent** — identifies skills to develop.
4. **Sahaara Guidance Agent** — combines the analysis into simple next steps.

The workflow runs sequentially using CrewAI.

## Files

- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `.streamlit/secrets.toml.example` — example API-key configuration
- `.gitignore` — prevents secrets from being uploaded

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. You may also upload `README.md`, `.gitignore`, and the `.streamlit` example file.
4. Create a Streamlit Community Cloud app and select `app.py`.
5. Open the app's **Settings → Secrets**.
6. Add:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Do **not** put the real API key in GitHub.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

For local testing, the app also accepts `GROQ_API_KEY` as an environment variable.

## Model

The prototype uses the Groq-hosted `openai/gpt-oss-120b` model through CrewAI/LiteLLM.

## Important

This is a functional prototype. It provides informational career and skill guidance and does not guarantee employment, income, or business success.
