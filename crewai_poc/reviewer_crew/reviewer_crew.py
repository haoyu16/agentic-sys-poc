from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel


class DocumentReviewResult(BaseModel):
    valid: bool
    feedback: Optional[str]

@CrewBase
class DocumentReviewerCrew:
    """Document reviewer crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def doc_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["doc_reviewer"],
            llm="gpt-4o"
        )

    @task
    def review_doc(self) -> Task:
        return Task(
            config=self.tasks_config["review_doc"],
            output_pydantic=DocumentReviewResult,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Shakespearean X Post Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )