from agent_framework.devui import serve

from ..agents.meal_plan import meal_plan_agent
from ..agents.macro_review import macro_review_agent


if __name__ == "__main__":

    serve(entities=[meal_plan_agent, macro_review_agent], auto_open=True)