from src.prompts import build_prompt
from src.utils.calorie_tool import calorie_calculator
from src.utils.io_utils import generate_filename
from src.utils.llm_handler import run_llm
from src.utils.agent_handler import run_agent
from src.utils.pdf_export import save_plan_as_pdf
from src.utils.email_sender import queue_email
from src.utils.prompt_summary import generate_summary_intro
import os

# --- User Test Inputs ---
user = "Alex"
user_email = "alex@example.com"
age = 30
gender = "Male"
height = 180
weight = 75
activity_level = "Moderately Active"
location = "Germany"
goal = "muscle gain"
avoid = "gluten, dairy"
likes = "tofu, oats, lentils"
workout_pref = "weightlifting"
days_per_week = 5
injuries = "shoulders"
sleep_routine = "7 hours, good quality"
stress_level = "Moderate"
supplements = ["Whey Protein", "Creatine"]
mode = "Agent-based (CrewAI)"  # or "Raw LLM"

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

# --- Summary ---
# calories = calorie_calculator(
#     weight=weight,
#     height=height,
#     age=age,
#     gender=gender,
#     activity_level=activity_level
# )

# intro_text = generate_summary_intro(
#     goal=goal,
#     # calories=calories,
#     location=location,
#     avoid=avoid,
#     likes=likes,
#     workout_pref=workout_pref,
#     days_per_week=days_per_week,
#     supplements=supplements
# )

full_output = output

# --- Save Files ---
filename_safe_user = user.strip() or "user"
txt_filename = generate_filename(method, filename_safe_user)
with open(txt_filename, "w", encoding="utf-8") as f:
    f.write("--- Prompt ---\n" + prompt + "\n\n--- Output ---\n" + full_output)

pdf_filename = txt_filename.replace(".txt", ".pdf")
save_plan_as_pdf(full_output, pdf_filename)

# --- Email Plan ---
if user_email.strip():
    if queue_email(user_email, pdf_filename):
        print(f"📧 Plan emailed to: {user_email}")
    else:
        print("❌ Email queue failed.")

# --- Done ---
print(f"\n✅ Plan generated and saved to:\n- {txt_filename}\n- {pdf_filename}")
print("\n📝 Preview:\n")
print(full_output[:1500] + "...\n\n(Truncated)")