from crewai.tools import tool

@tool("calorie_calculator")
def calorie_calculator(weight: float, height: float, age: int, gender: str, activity_level: str) -> int:
    """
    Estimate daily maintenance calories using the Mifflin-St Jeor formula.

    Parameters:
        weight (float): Body weight in kilograms
        height (float): Height in centimeters
        age (int): Age in years
        gender (str): "male" or "female"
        activity_level (str): "sedentary", "lightly active", "moderately active", or "very active"

    Returns:
        int: Estimated maintenance calories per day
    """
    gender = gender.lower()
    activity_level = activity_level.lower()

    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725
    }

    return round(bmr * multipliers.get(activity_level, 1.55))
