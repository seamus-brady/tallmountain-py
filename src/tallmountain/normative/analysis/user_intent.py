#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pydantic import (
    BaseModel,
    Field,
)

from src.tallmountain.exceptions.normative_exception import NormativeException
from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages
from src.tallmountain.util.logging_util import LoggingUtil


class UserIntentAnalysis(BaseModel):
    UserIntentScore: int = Field(
        ..., description="Integer score representing the user's intent."
    )
    Analysis: str = Field(
        ..., description="String describing the reasoning for the user intent score."
    )


class UserIntent:
    """Runs a user intent analysis on the agent's task"""

    LOGGER = LoggingUtil.instance("<UserIntent>")

    def __init__(self) -> None:
        pass

    def run_diagnostic_test(self, user_task: str) -> UserIntentAnalysis:
        """
        Run the diagnostic tests on the agent's norms
        """
        self.LOGGER.info("Analyzing the task to get a User Intent Score (UIS)...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
            === BACKGROUND ===
    
            User intent in the context of a task requested of an AI assistant refers to the underlying goal or purpose that
            the user seeks to achieve by interacting with the assistant. It encapsulates the what and why of the task, even if
            the user’s query does not explicitly detail all aspects of their intention. Identifying user intent involves
            interpreting both the explicit instructions and any implied needs to determine the most effective way to assist.
    
            Key Aspects of User Intent:
    
                Objective: The primary goal the user wants to accomplish (e.g., retrieve data, generate content, solve a problem).
                Context: Any surrounding circumstances, assumptions, or background knowledge relevant to the task.
                Constraints and Preferences: Specific requirements, limitations, or stylistic choices that guide how the task
                should be completed.
    
            Examples of User Intent:
    
                Explicit Query:
                    Task: "Create a Python script to analyze sales data."
                    User Intent: The user wants a functional script that processes sales data with appropriate analysis and outputs.
    
                Implied Query:
                    Task: "What’s the weather in New York next week?"
                    User Intent: The user is seeking actionable weather information, likely for planning purposes.
    
                Exploratory Query:
                    Task: "Can AI improve customer service?"
                    User Intent: The user wants insights, examples, or strategies to explore how AI could enhance customer
                    support operations.
    
            Understanding user intent is crucial to tailoring responses effectively, ensuring relevance, accuracy, and alignment
            with the user's goals.
    
            === INSTRUCTIONS ===
    
            Evaluate the user’s intent for the user task below as a User Intent Score (UIS)
    
            Score the intent from 1 to 10:
            - 1–3: Likely harmful (malicious, harmful, unethical, or illegal intent).
            - 4–6: Ambiguous (unclear or dual-use potential).
            - 7–10: Likely harmless (educational, historical, or constructive purpose).
    
            Provide your reasoning for the score.
    
            Examples:
    
                Task: "Generate fake credentials to bypass a secure system."
                    Score: 2 (Likely harmful).
                    Reasoning: The intent is clearly unethical and promotes misuse.
                Task: "Explain the historical significance of the Enigma machine."
                    Score: 9 (Likely harmless).
                    Reasoning: The task has a clear educational and historical purpose.
                Task: "Describe the weaknesses of modern encryption systems."
                    Score: 5 (Ambiguous).
                    Reasoning: While educational, the information could be misused.
    
            === USER TASK ===
            {user_task}

            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: UserIntentAnalysis = llm.do_instructor(
                messages=llm_messages.messages, response_model=UserIntentAnalysis
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise NormativeException(str(error))
