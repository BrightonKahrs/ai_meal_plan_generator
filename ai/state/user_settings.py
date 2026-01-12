from ai.models.meal_plan import MacroNutrition, Budget

def get_user_budget_settings() -> Budget:
    """Retrieve the user's budget settings"""
    return Budget(total_budget=150.0)

def get_user_nutritional_settings() -> MacroNutrition:
    """Retrieve the user's nutritional settings"""
    return MacroNutrition(
        calories=2500,
        protein=180,
        fat=90,
        carbohydrates=250
    )
