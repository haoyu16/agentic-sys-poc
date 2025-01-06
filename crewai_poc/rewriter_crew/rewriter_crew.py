from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class DocumentRewriterCrew:
    """Document rewriter crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def doc_rewriter(self) -> Agent:
        return Agent(
            config=self.agents_config["doc_rewriter"],
            llm=LLM(
                model="gpt-4o",
            )
        )

    @task
    def rewrite_document(self) -> Task:
        return Task(
            config=self.tasks_config["rewrite_document"],
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