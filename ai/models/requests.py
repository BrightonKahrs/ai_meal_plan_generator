from typing import Optional
from pydantic import BaseModel

from ai.models.meal_plan import Nutrition, Budget

class MealPlanWorkflowRequest(BaseModel):
    """Represents a meal plan request with nutritional requirements"""
    user_prompt: str
    # nutritional_requirements: Optional[Nutrition]
    # budget: Optional[Budget]