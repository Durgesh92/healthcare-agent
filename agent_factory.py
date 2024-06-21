from typing import Optional, Tuple

from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
from vocode.streaming.agent.base_agent import BaseAgent, RespondAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import AgentConfig, AgentType, ChatGPTAgentConfig

from collect_data import DataCollectActionFactory

class HealthAgentFactory(AbstractAgentFactory):
    """Factory class for creating agents based on the provided agent configuration."""

    def create_agent(self, agent_config: AgentConfig) -> BaseAgent:
        """Creates an agent based on the provided agent configuration.

        Args:
            agent_config (AgentConfig): The configuration for the agent to be created.

        Returns:
            BaseAgent: The created agent.

        Raises:
            Exception: If the agent configuration type is not recognized.
        """
        if isinstance(agent_config, ChatGPTAgentConfig):
            return ChatGPTAgent(agent_config=agent_config, action_factory=DataCollectActionFactory())
        # If the agent configuration type is not a ChatGPTAgent, raise an exception
        raise Exception("Invalid agent config")
    