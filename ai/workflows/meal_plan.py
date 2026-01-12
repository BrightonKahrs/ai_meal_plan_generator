import json
import logging
from typing import List

from agent_framework.devui import serve
from agent_framework import AgentExecutorResponse, AgentRunResponse, Case, Default, ChatMessage, WorkflowBuilder, WorkflowContext, WorkflowEvent, executor

from ai.agents.meal_plan import meal_plan_agent
from ai.agents.macro_review import macro_review_agent
from ai.agents.budget_review import budget_review_agent
from ai.models.review import Review
from ai.models.meal_plan import MealPlan, MacroNutrition, Budget
from ai.models.requests import MealPlanWorkflowRequest
from ai.state.user_settings import get_user_budget_settings, get_user_nutritional_settings

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

user_budget_settings = get_user_budget_settings()
user_nutritional_settings = get_user_nutritional_settings()


# Conditions
def review_passed(message: str) -> bool:
    """Check if content is approved (high quality)."""
    try:
        review = Review.model_validate_json(message)
        return review.review_status == "Passed"
    except Exception:
        logger.error("Failed to parse Review from message", exc_info=True)
        return False


# Executors
@executor(id="initialize_workflow")
async def initialize_workflow_state(request: MealPlanWorkflowRequest, ctx: WorkflowContext[str]) -> None:
    """Initialize any shared state needed for the workflow"""
    await ctx.set_shared_state("current_meal_plan", None)
    await ctx.set_shared_state("initial_user_message", request.user_prompt)
    await ctx.set_shared_state("macro_requirements", user_nutritional_settings)
    await ctx.set_shared_state("macro_review_feedback", None)
    await ctx.set_shared_state("budget_requirements", user_budget_settings)
    await ctx.set_shared_state("budget_review_feedback", None)
    await ctx.send_message("Ready to start workflow")


@executor(id="generate_meal_plan")
async def generate_meal_plan(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate initial meal plan based on user input"""

    initial_user_message: str = await ctx.get_shared_state("initial_user_message")
    macro_review_feedback: Review | None = await ctx.get_shared_state("macro_review_feedback")
    budget_review_feedback: Review | None = await ctx.get_shared_state("budget_review_feedback")

    prompt = f"""
    Generate a meal plan to satisfy the user ask and the macro requirements below. Make sure to use any corrections from previous reviews if applicable.

    # User Ask: 
    {initial_user_message}

    # Feedback from previous reviews:
        ## Macro review agent feedback:
        {macro_review_feedback}
        ## Budget review agent feedback: 
        {budget_review_feedback}
    """

    result: AgentRunResponse = await meal_plan_agent.run(prompt)
    meal_plan: MealPlan = MealPlan.model_validate_json(result.text)

    await ctx.set_shared_state("current_meal_plan", meal_plan)
    await ctx.send_message(meal_plan.model_dump_json(indent=2))

@executor(id="macro_review")
async def macro_review(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate review of current meal plan based on macro requirements"""

    macro_requirements: MacroNutrition = await ctx.get_shared_state("macro_requirements")
    current_meal_plan: MealPlan = await ctx.get_shared_state("current_meal_plan")

    prompt = f"""
    Provided Meal Plan:
    {current_meal_plan}

    User Macros:
    {macro_requirements}
    """

    result: AgentRunResponse = await macro_review_agent.run(prompt)
    macro_review: Review = Review.model_validate_json(result.text)

    await ctx.set_shared_state("macro_review_feedback", macro_review)
    await ctx.send_message(macro_review.model_dump_json(indent=2))


@executor(id="budget_review")
async def budget_review(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate review of current meal plan based on budget requirements"""

    budget_requirements: Budget = await ctx.get_shared_state("budget_requirements")
    current_meal_plan: MealPlan = await ctx.get_shared_state("current_meal_plan")

    prompt = f"""
    Provided Meal Plan:
    {current_meal_plan}

    User Budget:
    {budget_requirements}
    """

    result: AgentRunResponse = await budget_review_agent.run(prompt)
    budget_review: Review = Review.model_validate_json(result.text)
    await ctx.set_shared_state("budget_review_feedback", budget_review)
    await ctx.send_message(budget_review.model_dump_json(indent=2))


@executor(id="review_aggregator")
async def review_aggregator(messages: List[str], ctx: WorkflowContext[str]) -> None:
    """Aggregate review results from macro and budget reviewers"""
    reviews = [Review.model_validate_json(msg) for msg in messages]

    aggregated_review: Review = reviews[0]
    for review in reviews[1:]:
        aggregated_review += review

    await ctx.send_message(aggregated_review.model_dump_json(indent=2))


@executor(id="finalize_workflow")
async def finalize_workflow(message: str, ctx: WorkflowContext[str]) -> None:
    """Finishing steps once main workflow is complete"""
    current_meal_plan: MealPlan = await ctx.get_shared_state("current_meal_plan")
    await ctx.yield_output(current_meal_plan)


# Workflow
workflow = (
    WorkflowBuilder(name="MealPlanReviewWorkflow", max_iterations=20)
    .set_start_executor(initialize_workflow_state)
    .add_edge(initialize_workflow_state, generate_meal_plan)
    .add_fan_out_edges(generate_meal_plan, [macro_review, budget_review])
    .add_fan_in_edges([macro_review, budget_review], review_aggregator)

    .add_switch_case_edge_group(
        review_aggregator,
        [
            Case(
                condition=review_passed,
                target=finalize_workflow
            ),
            Case(
                condition= lambda result: not review_passed(result),
                target=generate_meal_plan
            )
        ]
    )

    .build()
)


if __name__ == "__main__":

    serve(entities=[workflow, meal_plan_agent, macro_review_agent], auto_open=True, port=8090)