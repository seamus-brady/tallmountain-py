#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import concurrent.futures
from typing import List

from pydantic import BaseModel, Field

from src.tallmountain.exceptions.normative_exception import NormativeException
from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages
from src.tallmountain.normative.analysis.np_extractor import NormPropExtractor
from src.tallmountain.normative.entities.comprehensiveness import Comprehensiveness
from src.tallmountain.normative.entities.endeavour import Endeavour
from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.logging_util import LoggingUtil

#


class TaskResponse(BaseModel):
    """A response model"""

    name: str = Field(..., description="The name of the task.")
    goal: str = Field(..., description="The goal of the task.")
    description: str = Field(..., description="A description of the task.")


class UserTask(Endeavour):
    """
    A task that the system is doing on behalf of a user.
    Can also call the LLM model to get a goal and description for the user task."""

    LOGGER = LoggingUtil.instance("<UserTask>")

    @staticmethod
    def get_from_query(user_query: str) -> "UserTask":
        try:

            UserTask.LOGGER.info("Getting user task from user query")

            # ---- start internal functions ----
            def extract_norm_props() -> List[NormativeProposition]:
                extractor: NormPropExtractor = NormPropExtractor()
                return extractor.extract_normative_propositions(user_query)

            def extract_goal_description() -> TaskResponse:
                return UserTask.get_goal_description(user_query)

            # ---- end internal functions ----

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_norm_props = executor.submit(extract_norm_props)
                future_goal_description = executor.submit(extract_goal_description)

                extracted_norm_props = future_norm_props.result()
                task_goal_description = future_goal_description.result()

            user_task = UserTask(
                name=task_goal_description.name,
                description=task_goal_description.description,
                comprehensiveness=Comprehensiveness.DEFAULT,
                normative_propositions=extracted_norm_props,
            )

            return user_task
        except Exception as error:
            UserTask.LOGGER.error(str(error))
            raise NormativeException(str(error))

    @staticmethod
    def get_goal_description(statement: str) -> TaskResponse:
        try:
            UserTask.LOGGER.info("Getting user task goal and description")

            llm: LLM = LLM()
            llm_messages = LLMMessages()
            prompt: str = f"""
            
            === INSTRUCTIONS ===
            - Your job is to analyse the user's statement below and formulate a goal and description for the AI assistant task
              to handle this user query.
            - The name should be a short, descriptive name for the task.
            - The goal should be a clear statement of what the user is trying to the AI assistant to do.
            - The description should be a more detailed explanation of the task and the context in which it will be performed.
            === START INPUT STATEMENT ===
            {statement}
            === END INPUT STATEMENT ===
            
            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: TaskResponse = llm.do_instructor(
                messages=llm_messages.messages, response_model=TaskResponse
            )
            return response
        except Exception as error:
            UserTask.LOGGER.error(str(error))
            raise NormativeException(str(error))
