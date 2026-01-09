from typing import Any

from agent_framework.devui import serve
from agent_framework import AgentExecutorResponse, WorkflowBuilder, WorkflowContext, executor

from ai.agents.meal_plan import meal_plan_agent
from ai.agents.macro_review import macro_review_agent
from ai.models.reviews import MacroReview

# Conditions
def review_failed(message: Any) -> bool:
    """Check if content is approved (high quality)."""
    if not isinstance(message, AgentExecutorResponse):
        return True
    try:
        review = MacroReview.model_validate_json(message.agent_run_response.text)
        return review.review_status != "Passed"
    except Exception:
        return True
    

# Executors
@executor(id="user_macro_requirements")
async def user_macro_requirements(message: AgentExecutorResponse, ctx: WorkflowContext[str]) -> None:
    """Send user requirements into chat for the reviewer to use"""
    message = message.agent_run_response.text

    await ctx.send_message(f""" 
        Provided Meal Plan:
        {message}
                
        User Macro Requirements:
        - Calories: 2500cal
        - Protein: 180g
        - Carbohydrates: 200g
        - Fat: 100g          
        """)
    
@executor(id="macro_review_feedback")
async def macro_review_feedback(message: AgentExecutorResponse, ctx: WorkflowContext[str]) -> None:
    """Send feedback from macro review to revise meal plan"""
    message = message.agent_run_response.text

    await ctx.send_message(f"""
                           
        Revise the previously generated meal plan to address the following feedback. We want to ensure all adjustments are accounted for in the new meal plan
                           
        ## Feedback to address
            {message}
        """)

@executor(id="finalize_meal_plan")
async def finalize_meal_plan(message: AgentExecutorResponse, ctx: WorkflowContext[str]) -> None:
    """Finishing steps once main workflow is complete"""
    await ctx.send_message("Meal plan complete")


# Workflow
workflow = (
    WorkflowBuilder(name="MealPlanReviewWorkflow", max_iterations=20)
    .set_start_executor(meal_plan_agent)
    .add_edge(meal_plan_agent, user_macro_requirements)
    .add_edge(user_macro_requirements, macro_review_agent)

    # Path is review failed
    .add_edge(macro_review_agent, macro_review_feedback, condition=review_failed)
    .add_edge(macro_review_feedback, meal_plan_agent)

    # Path is review passed
    .add_edge(macro_review_agent, finalize_meal_plan, condition=lambda message: not review_failed(message))
    .build()
)


if __name__ == "__main__":

    serve(entities=[workflow, meal_plan_agent, macro_review_agent], auto_open=True, port=8090)