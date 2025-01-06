from typing import Optional

from crewai.flow.flow import router, Flow, start, listen
from pydantic import BaseModel

from crewai_poc.reviewer_crew.reviewer_crew import (
    DocumentReviewerCrew,
)
from crewai_poc.rewriter_crew.rewriter_crew import (
    DocumentRewriterCrew,
)

with open("original_doc.txt", "r") as f:
    original_doc_test = f.read()

class DocumentFlowState(BaseModel):
    original_doc: str = original_doc_test
    rewritten_doc: str = ""
    feedback: Optional[str] = None
    valid: bool = False
    retry_count: int = 0


class DocumentFlow(Flow[DocumentFlowState]):

    @start("retry")
    def rewrite_document(self):
        print("Rewriting the original document")
        result = (
            DocumentRewriterCrew()
            .crew()
            .kickoff(inputs={"document": self.state.original_doc, "feedback": self.state.feedback})
        )

        print("Rewritten doc:", result.raw)
        self.state.rewritten_doc = result.raw

    @router(rewrite_document)
    def evaluate_doc(self):
        if self.state.retry_count > 3:
            return "max_retry_exceeded"

        result = DocumentReviewerCrew().crew().kickoff(inputs={"original_doc": self.state.original_doc, "rewritten_doc": self.state.rewritten_doc})
        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]

        print("valid", self.state.valid)
        print("feedback", self.state.feedback)
        self.state.retry_count += 1

        if self.state.valid:
            return "complete"

        return "retry"

    @listen("complete")
    def save_result(self):
        print("Rewritten document is valid")
        print("Rewritten document:", self.state.rewritten_doc)

        # Save the valid X post to a file
        with open("rewritten_doc.txt", "w") as file:
            file.write(self.state.rewritten_doc)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("Rewritten doc:", self.state.rewritten_doc)
        print("Feedback:", self.state.feedback)


def kickoff():
    document_flow = DocumentFlow()
    document_flow.kickoff()


def plot():
    document_flow = DocumentFlow()
    document_flow.plot()


if __name__ == "__main__":
    kickoff()