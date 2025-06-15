from crewai.tools import tool

@tool("macro_calculator")
def macro_calculator(calories: int, goal: str) -> dict:
    """
    Distribute daily calories into macros based on the fitness goal.
    - Protein: 4 cal/g, Carbs: 4 cal/g, Fat: 9 cal/g
    """
    if goal == "muscle gain":
        macros = {
            "protein_g": round(0.3 * calories / 4),
            "carbs_g": round(0.45 * calories / 4),
            "fats_g": round(0.25 * calories / 9),
        }
    elif goal == "fat loss":
        macros = {
            "protein_g": round(0.4 * calories / 4),
            "carbs_g": round(0.3 * calories / 4),
            "fats_g": round(0.3 * calories / 9),
        }
    else:
        macros = {
            "protein_g": round(0.3 * calories / 4),
            "carbs_g": round(0.4 * calories / 4),
            "fats_g": round(0.3 * calories / 9),
        }
    return macros