from ai.models.meal_plan import Nutrition, Budget

def get_user_budget_settings() -> Budget:
    """Retrieve the user's budget settings"""
    return Budget(total_budget=200.0)

def get_user_nutritional_settings() -> Nutrition:
    """Retrieve the user's nutritional settings"""
    return Nutrition(
        calories=2000,
        protein=160,
        fat=70,
        carbohydrates=225
    )
