import logging

from agent_framework.devui import serve
from agent_framework import AgentExecutorResponse, AgentRunResponse, Case, Default, ChatMessage, WorkflowBuilder, WorkflowContext, executor

from ai.agents.meal_plan import meal_plan_agent
from ai.agents.macro_review import macro_review_agent
from ai.models.reviews import MacroReview
from ai.models.meal_plan import MealPlan

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

MACRO_REQUIREMENTS = {
    "calories": 2500,
    "protein": 180,
    "carbs": 200,
    "fat": 100
}

# Conditions
def review_passed(message: str) -> bool:
    """Check if content is approved (high quality)."""
    try:
        review = MacroReview.model_validate_json(message)
        return review.review_status == "Passed"
    except Exception:
        logger.error("Failed to parse MacroReview from message", exc_info=True)
        return False


# Executors
@executor(id="initialize_workflow")
async def initialize_workflow_state(message: str, ctx: WorkflowContext[str]) -> None:
    """Initialize any shared state needed for the workflow"""
    await ctx.set_shared_state("current_meal_plan", None)
    await ctx.set_shared_state("initial_user_message", message)
    await ctx.set_shared_state("macro_requirements", MACRO_REQUIREMENTS)
    await ctx.set_shared_state("macro_review_feedback", None)
    await ctx.send_message("Ready to start workflow")


@executor(id="generate_meal_plan")
async def generate_meal_plan(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate initial meal plan based on user input"""

    macro_requirements = await ctx.get_shared_state("macro_requirements")
    initial_user_message = await ctx.get_shared_state("initial_user_message")

    macro_review_feedback = await ctx.get_shared_state("macro_review_feedback")

    prompt = f"""
    Generate a meal plan to satisfy the user ask and the macro requirements below. Make sure to use any corrections from previous reviews if applicable.
    User Ask: {initial_user_message}

    Feedback from previous reviews:
    Macro review agent feedback: {macro_review_feedback}
    """

    result: MealPlan = await meal_plan_agent.run(prompt)

    await ctx.set_shared_state("current_meal_plan", result)
    await ctx.send_message("Meal plan generated, proceeding to review")


@executor(id="macro_review")
async def macro_review(message: str, ctx: WorkflowContext[str]) -> None:
    """Generate review of current meal plan based on macro requirements"""

    macro_requirements = await ctx.get_shared_state("macro_requirements")
    current_meal_plan: MealPlan = await ctx.get_shared_state("current_meal_plan")

    prompt = f"""
    Provided Meal Plan:
    {current_meal_plan}

    User Macros:
    {macro_requirements}
    """

    result: AgentRunResponse = await macro_review_agent.run(prompt)

    await ctx.set_shared_state("macro_review_feedback", result.text)
    await ctx.send_message(result.text)


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
    .add_edge(generate_meal_plan, macro_review)

    .add_switch_case_edge_group(
        macro_review,
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

    serve(entities=[workflow, meal_plan_agent, macro_review_agent], auto_open=True, port=8090)