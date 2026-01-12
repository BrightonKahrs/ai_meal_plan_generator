import os
from dotenv import load_dotenv

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential

load_dotenv()

class AIConfig:

    def __init__(self):
        # Azure AI Configuration
        self._azure_ai_project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self._azure_ai_model_deployment_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")

        # Initialize client to be used across AI Agents
        self._credential = DefaultAzureCredential()

        self.client = AzureAIAgentClient(
            credential=self._credential,
            project_endpoint=self._azure_ai_project_endpoint,
            model_deployment_name=self._azure_ai_model_deployment_name
        )


ai_config = AIConfig()