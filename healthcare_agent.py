from typing import Optional, Tuple

from vocode.streaming.agent.abstract_factory import AbstractAgentFactory
from vocode.streaming.agent.base_agent import BaseAgent, RespondAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import AgentConfig, AgentType, ChatGPTAgentConfig


class HealthAgentConfig(AgentConfig, type="agent_chat_gpt"):
    """Configuration for SpellerAgent. Inherits from AgentConfig."""

    pass


class HealthAgent(RespondAgent[HealthAgentConfig]):
    def __init__(self, agent_config: HealthAgentConfig):
        """Initializes SpellerAgent with the given configuration.

        Args:
            agent_config (SpellerAgentConfig): The configuration for this agent.
        """
        super().__init__(agent_config=agent_config)

    async def respond(
        self,
        human_input: str,
        conversation_id: str,
        is_interrupt: bool = False,
    ) -> Tuple[Optional[str], bool]:
        """Generates a response from the HealthAgent.

        Args:
            human_input (str): The input from the human user.
            conversation_id (str): The ID of the conversation.
            is_interrupt (bool): A flag indicating whether the agent was interrupted.

        Returns:
            Tuple[Optional[str], bool]: The generated response and a flag indicating whether to stop.
        """
        return "".join(c + " " for c in human_input), False


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
        # If the agent configuration type is not a HealthAgentConfig, raise an exception
        if isinstance(agent_config, HealthAgentConfig):
            return ChatGPTAgent(agent_config=agent_config)
        raise Exception("Invalid agent config")