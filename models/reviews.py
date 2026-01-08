from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal

class MacroBudgetReview(BaseModel):
    """Represents a macro and budget review result"""
    model_config = ConfigDict(extra='forbid')

    review_status: Literal['Passed', 'Failed'] = Field(..., description="Demonstrates whether or not the review passed or failed")
    adjustments: List[str] = Field(..., description="List of feedback adjustment for budget review")