from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class Coder:
    """Coder crew"""

    agents_config = "./config/agents.yaml"
    tasks_config = "./config/tasks.yaml"

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config["coder"],
            verbose=True,
            allow_code_execution=True,  # This allows the agent to execute code in a safe environment. Learn more: https://docs.crewai.com/concepts/agents#agent-tools
            code_execution_mode="safe",  # This ensures that the code execution is done in a secure environment. Learn more: https://docs.crewai.com/concepts/agents#agent-tools
            max_execution_time=60,  # This limits the maximum execution time for any code snippet to 60 seconds. Learn more: https://docs.crewai.com/concepts/agents#agent-tools
            max_retry_limit=3,  # This limits the number of retries for code execution to 3. Learn more: https://docs.crewai.com/concepts/agents#agent-tools
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config["coding_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Coder crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
