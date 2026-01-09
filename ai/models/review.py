from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal


class Adjustment(BaseModel):
    """Represents a single adjustment suggestion"""
    model_config = ConfigDict(extra='forbid')

    criticality: Literal['Low', 'Medium', 'High'] = Field(..., description="Indicates the criticality level of the adjustment")
    suggestion: str = Field(..., description="Textual suggestion for the adjustment")


class Review(BaseModel):
    """Represents a macro and budget review result"""
    model_config = ConfigDict(extra='forbid')

    review_status: Literal['Passed', 'Failed'] = Field(..., description="Demonstrates whether or not the review passed or failed")
    adjustments: List[Adjustment] = Field(..., description="List of feedback adjustment suggestions for macro review")

    def __add__(self, other: Review) -> Review:
        """Combine two reviews using the + operator.
        
        The combined review fails if either review fails.
        Adjustments from both reviews are merged.
        """
        combined_status = 'Failed' if self.review_status == 'Failed' or other.review_status == 'Failed' else 'Passed'
        combined_adjustments = self.adjustments + other.adjustments
        
        return Review(
            review_status=combined_status,
            adjustments=combined_adjustments
        )