def build_prompt(
    goal: str,
    avoid: str,
    likes: str,
    age: int,
    gender: str,
    height: float,
    weight: float,
    activity_level: str,
    location: str,
    workout_pref: str,
    days_per_week: int,
    injuries: str,
    sleep_routine: str,
    stress_level: str,
    supplements: list,
) -> str:
    prompt = f"""
You are a certified sports nutritionist.

Create a 3-day personalized meal plan for a client based on their profile below.

User Profile:
- Goal: {goal}
- Age: {age}, Gender: {gender}
- Height: {height} cm, Weight: {weight} kg
- Activity Level: {activity_level}
- Location: {location}
- Sleep: {sleep_routine}, Stress: {stress_level}
- Workout: {workout_pref}, {days_per_week} days/week
- Injuries: {injuries}
- Foods to Avoid: {avoid or 'None'}
- Food Preferences: {likes or 'None'}
- Supplements: {', '.join(supplements) if supplements and 'None' not in supplements else 'None'}

Instructions:
1. Use ONLY the `calorie_calculator` tool to estimate daily calorie needs.
2. Do all other tasks (macronutrient targets, meal generation) using your internal knowledge.
3. Do NOT call any other tools. Tools like `macros_calculator`, `meal_generator`, etc., DO NOT exist.
4. Build a meal plan for 3 days:
   - Each day should include 3 meals and 1 snack.
   - Include estimated daily **macros (Protein, Carbs, Fats)** and **total calories**.
   - Respect dietary restrictions and preferred ingredients.
5. Use practical ingredients available in {location}.
6. Present the result in a section labeled: **Final Answer**.
"""
    return prompt
