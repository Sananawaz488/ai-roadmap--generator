import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .roadmap-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f8f9fa;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🎓 AI Learning Roadmap Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Create a personalized learning roadmap using AI.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHECK GROQ API KEY
# ============================================================

if "GROQ_API_KEY" not in st.secrets:

    st.error(
        "⚠️ Groq API key is not configured."
    )

    st.info(
        "Please add GROQ_API_KEY in Streamlit Cloud Secrets."
    )

    st.stop()


# ============================================================
# CREATE GROQ CLIENT
# ============================================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("📝 Tell us about your learning goal")

col1, col2 = st.columns(2)


with col1:

    domain = st.text_input(
        "📚 Learning Domain / Field",
        placeholder=(
            "Example: Artificial Intelligence, "
            "Cybersecurity, Web Development"
        )
    )


    level = st.selectbox(
        "🎯 Current Skill Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


with col2:

    duration = st.text_input(
        "📅 Learning Duration",
        placeholder="Example: 3 months, 6 months, 1 year"
    )


    hours = st.number_input(
        "⏰ Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=2,
        step=1
    )


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.button(
    "🚀 Generate Learning Roadmap",
    type="primary",
    use_container_width=True
)


# ============================================================
# ROADMAP GENERATION
# ============================================================

if generate_button:

    # --------------------------------------------------------
    # Validate inputs
    # --------------------------------------------------------

    if not domain.strip():

        st.warning(
            "⚠️ Please enter your learning domain."
        )

        st.stop()


    if not duration.strip():

        st.warning(
            "⚠️ Please enter your learning duration."
        )

        st.stop()


    # --------------------------------------------------------
    # AI Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an expert learning roadmap designer and
educational curriculum planner.

Create a personalized, practical and realistic
learning roadmap for the following learner.

USER INFORMATION
----------------
Learning Domain: {domain}
Current Skill Level: {level}
Learning Duration: {duration}
Study Hours Per Day: {hours}

IMPORTANT REQUIREMENTS
----------------------

1. Make the roadmap realistic for the available time.

2. Start from the learner's current skill level.

3. Progress gradually from basic concepts
   to advanced concepts.

4. Do not overload the learner.

5. Include theory, practice and projects.

6. Use clear Markdown formatting.

7. Make the roadmap easy to follow.

The roadmap MUST include:

## 🎯 1. Overall Learning Goal

Explain what the learner should achieve
by the end of the roadmap.

## 📋 2. Prerequisites

List the knowledge and skills needed
before starting.

If there are no prerequisites,
clearly mention that.

## 🗺️ 3. Learning Phases

Divide the learning journey into
logical phases.

For each phase include:

- Phase name
- Duration
- Main topics
- Learning objectives
- Practice activities

## 📅 4. Weekly Learning Plan

Create a week-by-week learning plan
based on the user's duration.

For each week include:

- Topics
- Learning objectives
- Practice tasks
- Expected outcome

## 💻 5. Practice Exercises

Give practical exercises appropriate
for the learner's current level.

## 🛠️ 6. Mini Projects

Suggest several small projects that
help the learner apply the concepts.

## 🚀 7. Final Capstone Project

Create ONE realistic final project.

Include:

- Project idea
- Main features
- Skills used
- Development stages

## 📚 8. Recommended Learning Resources

Recommend useful resource TYPES such as:

- Official documentation
- Courses
- Tutorials
- Books
- Practice platforms

Do not invent URLs.

## 🧠 9. Skills at the End

List the skills the learner should have
after completing the roadmap.

## ✅ 10. Progress Checklist

Create a simple checklist that the learner
can use to track progress.

Make the roadmap practical, structured,
realistic and suitable for the user's
current skill level.
"""


    # --------------------------------------------------------
    # Call Groq
    # --------------------------------------------------------

    with st.spinner(
        "🤖 Creating your personalized roadmap..."
    ):

        try:

            response = client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert educational "
                            "roadmap designer."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.7,

                max_tokens=8000
            )


            roadmap = response.choices[0].message.content


            # ------------------------------------------------
            # Display result
            # ------------------------------------------------

            st.success(
                "✅ Your learning roadmap has been generated!"
            )

            st.markdown("---")

            st.markdown(
                "## 🗺️ Your Personalized Learning Roadmap"
            )

            st.markdown(roadmap)


            # ------------------------------------------------
            # Download roadmap
            # ------------------------------------------------

            st.download_button(
                label="📥 Download Roadmap",
                data=roadmap,
                file_name="learning_roadmap.md",
                mime="text/markdown"
            )


        except Exception as e:

            st.error(
                "❌ Something went wrong while generating "
                "the roadmap."
            )

            st.code(str(e))
