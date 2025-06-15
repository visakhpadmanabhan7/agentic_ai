import streamlit as st
from src.prompts import build_prompt
from src.utils.calorie_tool import calorie_calculator
from src.utils.io_utils import generate_filename
from src.utils.llm_handler import run_llm
from src.utils.agent_handler import run_agent
from src.utils.pdf_export import save_plan_as_pdf
from src.utils.email_sender import queue_email
from src.utils.prompt_summary import generate_summary_intro
import os

st.set_page_config(page_title="FitAgent App", page_icon="🥗", layout="centered")
st.title("🥗 FitAgent Meal Plan Generator")

# --- Input Form ---
user = st.text_input("Your Name", value="")
user_email = st.text_input("📧 Email (for PDF delivery)", value="")
age = st.number_input("Your Age", min_value=10, max_value=100, value=30)
gender = st.radio("Gender", ["Male", "Female", "Other"], index=0)
height = st.number_input("Height (in cm)", min_value=100, max_value=250, value=180)
weight = st.number_input("Weight (in kg)", min_value=30, max_value=200, value=75)
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"], index=2)
location = st.text_input("Where do you live? (Country or region)", value="Germany")
goal = st.text_input("Fitness Goal (e.g. muscle gain, fat loss)", value="muscle gain")
avoid = st.text_input("Foods to avoid (comma separated)", value="gluten, dairy")
likes = st.text_input("Preferred ingredients or meals", value="tofu, oats, lentils")
workout_pref = st.text_input("Workout preferences", value="weightlifting")
days_per_week = st.slider("Workout days/week", min_value=1, max_value=7, value=5)
injuries = st.text_input("Injuries or stress areas?", value="shoulders")
sleep_routine = st.text_input("Sleep routine (e.g. 7 hrs, good quality)", value="7 hours, good quality")
stress_level = st.selectbox("Current stress level", ["Low", "Moderate", "High"], index=1)
supplements = st.multiselect("Supplements open to using", ["None", "Whey Protein", "Creatine"], default=["Whey Protein", "Creatine"])
mode = st.radio("Choose Mode", ["Agent-based (CrewAI)", "Raw LLM"], index=0)

# --- Generate Plan ---
if st.button("Generate Plan"):
    if not user.strip():
        st.warning("Please enter your name.")
    else:
        st.write("⏳ Generating your personalized meal plan...")

        # --- Build Prompt ---
        user_inputs = {
            "goal": goal,
            "avoid": avoid,
            "likes": likes,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "activity_level": activity_level,
            "location": location,
            "workout_pref": workout_pref,
            "days_per_week": days_per_week,
            "injuries": injuries,
            "sleep_routine": sleep_routine,
            "stress_level": stress_level,
            "supplements": supplements,
        }

        prompt = build_prompt(**user_inputs)

        # --- Run the Model ---
        if "Agent" in mode:
            output = run_agent(prompt)
            method = "agent_crewai"
        else:
            output = run_llm(prompt)
            method = "raw_llm"
        # intro_text = generate_summary_intro(
        #     goal=goal,
        #     location=location,
        #     avoid=avoid,
        #     likes=likes,
        #     workout_pref=workout_pref,
        #     days_per_week=days_per_week,
        #     supplements=supplements
        # )

        # full_output = intro_text + "\n\n" + (output if output else "No output generated.")
        full_output = output

        # --- Save .txt and .pdf ---
        filename_safe_user = user.strip() or "user"
        txt_filename = generate_filename(method, filename_safe_user)
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write("--- Prompt ---\n" + prompt + "\n\n--- Output ---\n" + full_output)

        pdf_filename = txt_filename.replace(".txt", ".pdf")
        save_plan_as_pdf(full_output, pdf_filename)

        # --- Email if needed ---
        if user_email.strip():
            if queue_email(user_email, pdf_filename):
                st.info("📧 Plan queued for email delivery.")
            else:
                st.warning("❌ Failed to queue email.")

        # --- Display Result ---
        st.success("✅ Meal plan generated!")
        st.download_button("Download Plan", full_output, file_name=os.path.basename(pdf_filename))
        st.text_area("Your Plan", full_output, height=500)