from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal

class Adjustment(BaseModel):
    """Represents a single adjustment suggestion"""
    model_config = ConfigDict(extra='forbid')

    criticality: Literal['Low', 'Medium', 'High'] = Field(..., description="Indicates the criticality level of the adjustment")
    suggestion: str = Field(..., description="Textual suggestion for the adjustment")

class MacroReview(BaseModel):
    """Represents a macro and budget review result"""
    model_config = ConfigDict(extra='forbid')

    review_status: Literal['Passed', 'Failed'] = Field(..., description="Demonstrates whether or not the review passed or failed")
    adjustments: List[Adjustment] = Field(..., description="List of feedback adjustment suggestions for macro review")