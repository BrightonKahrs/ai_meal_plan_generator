import os
from dotenv import load_dotenv

from agent_framework.azure import AzureAIAgentClient

load_dotenv()

class Config:

    def __init__(self):
        # Azure AI Configuration
        self.azure_ai_project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self.azure_ai_model_deployment_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        self.azure_ai_api_key = os.getenv("AZURE_AI_API_KEY")

        # Initialize client to be used across AI Agents
        self.client = AzureAIAgentClient(
                api_key=self.azure_ai_api_key,
                project_endpoint=self.azure_ai_project_endpoint,
                model_deployment_name=self.azure_ai_model_deployment_name
            )


config = Config()