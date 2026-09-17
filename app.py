import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# Groq Client
# ============================================================

if not GROQ_API_KEY:
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# Generate Learning Roadmap
# ============================================================

def generate_roadmap(domain, level, duration, hours):

    # Check API key
    if not GROQ_API_KEY:
        return (
            "⚠️ Groq API key is not configured.\n\n"
            "Please add your GROQ_API_KEY to the .env file."
        )

    # Check inputs
    if not domain or not domain.strip():
        return "⚠️ Please enter a learning domain."

    if not duration or not duration.strip():
        return "⚠️ Please enter your learning duration."

    if not hours:
        return "⚠️ Please enter your available study hours."

    # Convert hours to readable value
    hours = int(hours)

    # ========================================================
    # AI Prompt
    # ========================================================

    prompt = f"""
You are an expert learning roadmap designer and educational
curriculum planner.

Create a personalized and realistic learning roadmap for the user.

USER INFORMATION
----------------
Learning Domain: {domain}
Current Skill Level: {level}
Learning Duration: {duration}
Study Hours Per Day: {hours}

IMPORTANT INSTRUCTIONS
----------------------
- Make the roadmap realistic for the available study time.
- Start from the learner's current level.
- Progress gradually from fundamentals to advanced concepts.
- Do not overload the learner.
- Focus on practical learning.
- Include theory, practice, projects, and revision.
- Use clear Markdown formatting.
- Keep the roadmap easy to follow.

The roadmap MUST include:

1. 🎯 Overall Learning Goal

Explain what the learner should be able to do by the end.

2. 📋 Prerequisites

Mention the knowledge or skills required before starting.
If there are no prerequisites, clearly say so.

3. 🗺️ Learning Roadmap

Divide the learning journey into logical phases.

For each phase include:
- Phase name
- Duration
- Main topics
- Learning objectives
- Practice activities

4. 📅 Weekly Learning Plan

Create a week-by-week plan based on the user's duration.

For every week include:
- Topics
- Learning objectives
- Practice tasks
- Expected outcome

5. 💻 Practice Exercises

Give practical exercises suitable for the learner's level.

6. 🛠️ Mini Projects

Suggest several small projects that help the learner
apply the concepts.

7. 🚀 Final Capstone Project

Design ONE realistic final project that combines
the major skills learned.

Include:
- Project idea
- Features
- Skills used
- Suggested development stages

8. 📚 Recommended Learning Resources

Suggest useful types of resources such as:
- Documentation
- Courses
- Tutorials
- Books
- Practice platforms

Do not invent specific URLs.

9. 🧠 Skills at the End

List the skills the learner should have after completing
the roadmap.

10. ✅ Progress Checklist

Create a simple checklist the learner can use to track progress.

Make the roadmap practical, structured, motivating,
and appropriate for the user's current skill level.
"""

    # ========================================================
    # Send request to Groq
    # ========================================================

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert educational roadmap "
                        "designer. Give practical, structured, "
                        "realistic learning plans."
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

        # Get AI response
        roadmap = response.choices[0].message.content

        return roadmap

    except Exception as e:

        return (
            "❌ Something went wrong while generating the roadmap.\n\n"
            f"Error: {str(e)}"
        )


# ============================================================
# Gradio UI
# ============================================================

with gr.Blocks(
    title="AI Learning Roadmap Generator"
) as app:

    gr.Markdown(
        """
        # 🎓 AI Learning Roadmap Generator

        ### Build your personalized learning journey with AI

        Enter your learning domain, current skill level,
        available learning duration, and daily study time.

        The AI will create a structured roadmap from
        fundamentals to advanced concepts.
        """
    )

    gr.Markdown("---")

    # --------------------------------------------------------
    # Learning Domain
    # --------------------------------------------------------

    domain = gr.Textbox(
        label="📚 Learning Domain / Field",
        placeholder=(
            "Example: Artificial Intelligence, "
            "Cybersecurity, Web Development, Data Science"
        ),
        lines=1
    )

    # --------------------------------------------------------
    # Skill Level
    # --------------------------------------------------------

    level = gr.Dropdown(
        choices=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        value="Beginner",
        label="🎯 Current Skill Level"
    )

    # --------------------------------------------------------
    # Learning Duration
    # --------------------------------------------------------

    duration = gr.Textbox(
        label="📅 Learning Duration",
        placeholder="Example: 3 months, 6 months, 1 year"
    )

    # --------------------------------------------------------
    # Study Hours
    # --------------------------------------------------------

    hours = gr.Number(
        label="⏰ Study Hours Per Day",
        value=2,
        minimum=1,
        maximum=12,
        step=1
    )

    # --------------------------------------------------------
    # Generate Button
    # --------------------------------------------------------

    generate_button = gr.Button(
        "🚀 Generate Learning Roadmap",
        variant="primary"
    )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    gr.Markdown("## 🗺️ Your Learning Roadmap")

    roadmap_output = gr.Markdown(
        value=(
            "Your personalized roadmap will appear here..."
        )
    )

    # --------------------------------------------------------
    # Button Event
    # --------------------------------------------------------

    generate_button.click(
        fn=generate_roadmap,
        inputs=[
            domain,
            level,
            duration,
            hours
        ],
        outputs=roadmap_output
    )


# ============================================================
# Launch Application
# ============================================================

if __name__ == "__main__":
    app.launch(
        share=True
    )
