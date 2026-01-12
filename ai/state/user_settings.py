from ai.models.meal_plan import Nutrition, Budget

def get_user_budget_settings() -> Budget:
    """Retrieve the user's budget settings"""
    return Budget(total_budget=150.0)

def get_user_nutritional_settings() -> Nutrition:
    """Retrieve the user's nutritional settings"""
    return Nutrition(
        calories=2500,
        protein=180,
        fat=90,
        carbohydrates=250
    )
