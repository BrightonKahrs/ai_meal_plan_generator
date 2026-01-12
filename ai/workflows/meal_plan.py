import json
import logging
from typing import List

from agent_framework.devui import serve
from agent_framework import AgentExecutorResponse, AgentRunResponse, Case, Default, ChatMessage, WorkflowBuilder, WorkflowContext, WorkflowEvent, executor

from ai.agents.meal_plan import meal_plan_agent
from ai.agents.nutrition_review import nutrition_review_agent
from ai.agents.budget_review import budget_review_agent
from ai.models.review import Review
from ai.models.meal_plan import MealPlan, Nutrition, Budget
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
    await ctx.set_shared_state("nutrition_requirements", user_nutritional_settings)
    await ctx.set_shared_state("nutrition_review_feedback", None)
    await ctx.set_shared_state("budget_requirements", user_budget_settings)
    await ctx.set_shared_state("budget_review_feedback", None)
    await ctx.send_message("Ready to start workflow")


@executor(id="generate_meal_plan")
async def generate_meal_plan(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate initial meal plan based on user input"""

    initial_user_message: str = await ctx.get_shared_state("initial_user_message")
    nutrition_review_feedback: Review | None = await ctx.get_shared_state("nutrition_review_feedback")
    budget_review_feedback: Review | None = await ctx.get_shared_state("budget_review_feedback")

    prompt = f"""
    Generate a meal plan to satisfy the user ask and the nutritional requirements below. Make sure to use any corrections from previous reviews if applicable.
    # User Ask: 
    {initial_user_message}

    # Feedback from previous reviews:
        ## Nutrition review agent feedback:
        {nutrition_review_feedback}
        ## Budget review agent feedback: 
        {budget_review_feedback}
    """

    result: AgentRunResponse = await meal_plan_agent.run(prompt)
    meal_plan: MealPlan = MealPlan.model_validate_json(result.text)

    await ctx.set_shared_state("current_meal_plan", meal_plan)
    await ctx.send_message(meal_plan.model_dump_json(indent=2))

@executor(id="nutrition_review")
async def nutrition_review(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate review of current meal plan based on nutritional requirements"""

    nutritional_requirements: Nutrition = await ctx.get_shared_state("nutrition_requirements")
    current_meal_plan: MealPlan = await ctx.get_shared_state("current_meal_plan")

    prompt = f"""
    Provided Meal Plan:
    {current_meal_plan}

    User Nutrition Requirements:
    {nutritional_requirements}
    """

    result: AgentRunResponse = await nutrition_review_agent.run(prompt)
    nutrition_review: Review = Review.model_validate_json(result.text)

    await ctx.set_shared_state("nutrition_review_feedback", nutrition_review)
    await ctx.send_message(nutrition_review.model_dump_json(indent=2))

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
    """Aggregate review results from nutrition and budget reviewers"""
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
    

@executor(id="handle_error_endstate")
async def handle_error_endstate(message: str, ctx: WorkflowContext[str]) -> None:
    """Finishing steps once main workflow is complete"""
    await ctx.yield_output("Workflow ended in error state")


# Workflow
workflow = (
    WorkflowBuilder(name="MealPlanReviewWorkflow", max_iterations=20)
    .set_start_executor(initialize_workflow_state)
    .add_edge(initialize_workflow_state, generate_meal_plan)
    .add_fan_out_edges(generate_meal_plan, [nutrition_review, budget_review])
    .add_fan_in_edges([nutrition_review, budget_review], review_aggregator)

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
            ),
            Default(target=handle_error_endstate)
        ]
    )

    .build()
)


if __name__ == "__main__":

    serve(entities=[workflow, meal_plan_agent, nutrition_review_agent], auto_open=True, port=8090)