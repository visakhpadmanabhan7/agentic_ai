def generate_summary_intro(goal: str, location: str, avoid: str, likes: str, workout_pref: str, days_per_week: int, supplements: list) -> str:
    supplement_note = "no supplements" if not supplements or "None" in supplements else ", ".join(supplements)

    return f"""
###  Nutrition Strategy Based on Your Inputs:

Based on your provided details and your goal of **{goal}**, we’ve calculated your **daily maintenance calories** and optimized your **macronutrient targets** as follows:

- ** Goal:** {goal.capitalize()}  


To support your journey, this plan is tailored to:
- Respect your preferences (e.g. avoiding: {avoid or 'none'}, enjoys: {likes or 'any'})
- Fit your **workout routine**: {workout_pref or 'not specified'}, {days_per_week} days/week
- Align with local ingredient availability in **{location or 'your region'}**
- Include use of **{supplement_note}**

 Scroll down to view your personalized plan!
""".strip()