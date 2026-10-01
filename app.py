import os

import streamlit as st
import os

import streamlit as st

# Fix CrewAI + Groq cache_breakpoint compatibility
try:
    import crewai.llms.cache as crew_cache
    crew_cache.mark_cache_breakpoint = lambda msg: msg
except Exception:
    pass

from crewai import Agent, Crew, LLM, Process, Task


st.set_page_config(
    page_title="Sahaara AI",
    page_icon="🌸",
    layout="wide",
)

st.title("🌸 Sahaara AI")
st.subheader("AI Career & Skill Guidance for Women")
st.write(
    "Turn your existing education, skills, experience, and interests into "
    "realistic learning, work, freelancing, or small-scale entrepreneurship pathways."
)


# -----------------------------
# API key
# -----------------------------
api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "GROQ_API_KEY is not configured. Add it in Streamlit → Settings → Secrets."
    )
    st.stop()


# -----------------------------
# LLM
# -----------------------------
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0.3,
    max_tokens=600,
)


def build_crew():
    """Create the four-agent Sahaara AI workflow."""

    # -------------------------
    # Agents
    # -------------------------
    profile_agent = Agent(
        role="User Profile Analyst",
        goal=(
            "Convert a woman's education, skills, experience, interests, "
            "and goals into a concise profile for career guidance."
        ),
        backstory=(
            "You are a practical career-guidance analyst. "
            "Use only information supplied by the user. "
            "Never guarantee employment or income."
        ),
        llm=llm,
        verbose=False,
    )

    opportunity_agent = Agent(
        role="Opportunity Matching Specialist",
        goal=(
            "Identify realistic learning, employment, freelancing, and "
            "small-scale entrepreneurship opportunities that fit the profile."
        ),
        backstory=(
            "You match existing abilities with practical opportunities, "
            "especially flexible and work-from-home options where appropriate."
        ),
        llm=llm,
        verbose=False,
    )

    skill_agent = Agent(
        role="Skill Development Advisor",
        goal=(
            "Identify the most useful skills to develop for the recommended "
            "opportunities and create a practical learning sequence."
        ),
        backstory=(
            "You design simple, beginner-friendly skill-development plans "
            "with practical activities."
        ),
        llm=llm,
        verbose=False,
    )

    guidance_agent = Agent(
        role="Sahaara AI Guidance Advisor",
        goal=(
            "Combine the profile, opportunities, and skill plan into concise, "
            "actionable guidance that a general user can understand."
        ),
        backstory=(
            "You transform career information into simple next steps. "
            "Do not guarantee employment or income and avoid unrealistic claims."
        ),
        llm=llm,
        verbose=False,
    )

    # -------------------------
    # Tasks
    # -------------------------
    profile_task = Task(
        description="""
Create a concise structured profile from the user's information below.

USER INFORMATION:
{user_profile}

Return only:
- Education/background
- Current skills
- Experience/interests
- Goal
- Relevant constraints/preferences

Do not invent information.
""",
        expected_output=(
            "A concise structured user profile containing only information "
            "supported by the user's input."
        ),
        agent=profile_agent,
    )

    opportunity_task = Task(
        description="""
Using the Profile Task result, identify realistic opportunities that fit the user.

Provide 3 to 5 opportunities. For each give:
1. Opportunity
2. Why it fits
3. Basic skills needed
4. How to start

Prioritize flexible work, online work, freelancing, learning pathways, "
"or small-scale entrepreneurship when appropriate.

Do not guarantee employment or income.
Do not invent qualifications.
""",
        expected_output=(
            "A concise list of 3–5 realistic opportunities with fit, skills, "
            "and starting steps."
        ),
        agent=opportunity_agent,
        context=[profile_task],
    )

    skill_task = Task(
        description="""
Using the opportunity analysis, identify the 3 to 5 highest-priority skills
the user should develop.

For each skill provide:
1. Skill
2. Why it is needed
3. What to learn
4. One simple practice activity

Keep it realistic for the user's current level.
Do not guarantee employment or income.
""",
        expected_output=(
            "A concise skill-development roadmap with priority skills, reasons, "
            "learning steps, and practice activities."
        ),
        agent=skill_agent,
        context=[opportunity_task],
    )

    guidance_task = Task(
        description="""
Create the final Sahaara AI guidance using the previous analyses.

Use this exact structure:

## Your Profile
Brief summary.

## Suitable Opportunities
List 3–5 options with one-line explanations.

## Skills to Develop
List the most important skills and what to learn.

## Your Next 3 Steps
Give three practical actions the user can take next.

## Start Here
Give ONE clear first action.

Rules:
- Keep the answer concise and easy to understand.
- Use plain language.
- Do not guarantee employment or income.
- Do not make unrealistic earning claims or timelines.
- Do not ask the user for more information.
- Do not invent facts that are absent from the profile.
""",
        expected_output=(
            "A concise, practical final guidance response containing profile, "
            "opportunities, skills, three next steps, and one first action."
        ),
        agent=guidance_agent,
        context=[profile_task, opportunity_task, skill_task],
    )

    return Crew(
        agents=[
            profile_agent,
            opportunity_agent,
            skill_agent,
            guidance_agent,
        ],
        tasks=[
            profile_task,
            opportunity_task,
            skill_task,
            guidance_task,
        ],
        process=Process.sequential,
        verbose=False,
    )


# -----------------------------
# User interface
# -----------------------------
with st.form("sahaara_form"):
    st.markdown("### Tell Sahaara AI about yourself")

    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox(
            "Education",
            [
                "No formal education",
                "Primary",
                "Middle",
                "Matric / Secondary",
                "Intermediate",
                "Bachelor's",
                "Master's or above",
                "Vocational / technical training",
                "Other",
            ],
        )

        location = st.text_input(
            "City / area (optional)",
            placeholder="e.g., Multan",
        )

        skills = st.text_area(
            "What skills do you already have?",
            placeholder=(
                "e.g., typing, teaching children, sewing, cooking, "
                "Excel, social media"
            ),
            height=100,
        )

    with col2:
        experience = st.text_area(
            "Work or practical experience (optional)",
            placeholder=(
                "e.g., school teaching, home-based stitching, office work"
            ),
            height=100,
        )

        interests = st.text_area(
            "What do you enjoy or want to learn?",
            placeholder=(
                "e.g., online teaching, writing, crafts, digital work"
            ),
            height=100,
        )

        goal = st.text_area(
            "What would you like to achieve?",
            placeholder=(
                "e.g., learn a skill, find flexible work, start freelancing"
            ),
            height=100,
        )

    submitted = st.form_submit_button(
        "🌸 Generate My Sahaara Guidance",
        use_container_width=True,
    )


if submitted:
    if not skills.strip() and not experience.strip() and not interests.strip():
        st.warning("Please enter at least one skill, experience, or interest.")
        st.stop()

    user_profile = f"""
Education: {education}
Location: {location.strip() or "Not provided"}
Skills: {skills.strip() or "Not provided"}
Experience: {experience.strip() or "Not provided"}
Interests: {interests.strip() or "Not provided"}
Goal: {goal.strip() or "Not provided"}
"""

    with st.spinner(
        "Sahaara AI is analysing your profile and preparing guidance..."
    ):
        try:
            crew = build_crew()
            result = crew.kickoff(inputs={"user_profile": user_profile})

            st.success("Your personalized guidance is ready.")
            st.markdown("### 🌸 Your Sahaara Guidance")
            st.markdown(str(result))

        except Exception as exc:
            error_text = str(exc)

            if "RateLimit" in error_text or "rate_limit" in error_text.lower():
                st.error(
                    "The AI provider's temporary token limit was reached. "
                    "Please wait briefly and try again."
                )
            else:
                st.error("The application encountered an error.")
                with st.expander("Technical details"):
                    st.code(error_text)


st.divider()
st.caption(
    "Sahaara AI is a prototype for educational and career guidance. "
    "Recommendations are informational and do not guarantee employment or income."
)
