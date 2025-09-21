# Copyright 2023 Seamus Brady
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#
import os
from typing import Any, Dict, List, Optional, Type

import instructor
from dotenv import load_dotenv
from openai import OpenAI

from src.tallmountain.exceptions.llm_exception import LLMException
from src.tallmountain.llm.llm_client import LLMClient, T
from src.tallmountain.llm.xstructor import XStructor
from src.tallmountain.modes.adaptive_request_mode import AdaptiveRequestMode
from src.tallmountain.util.logging_util import LoggingUtil

# take environment variables from .env.
load_dotenv()

# OpenAI public api
OPENI_API_KEY = os.environ["OPENAI_API_KEY"]


class OpenAIClient(LLMClient):
    """An interface to the OpenAI API. Used only from within the LLM facade parent class."""

    DEFAULT_MODEL = "gpt-4o"

    LOGGER = LoggingUtil.instance("<OpenAIClient>")

    def __init__(self) -> None:
        super().__init__()
        OpenAIClient.LOGGER.info("Initializing OpenAIClient...")
        self._model = self.DEFAULT_MODEL
        self.client = OpenAI(api_key=OPENI_API_KEY)

    def do_xstructor(
        self,
        messages: List[Dict[str, str]],
        xml_example: str,
        xml_schema: str,
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling XStructor xml schema based completions.
        Used for more complex tasks where Instructor is not enough.
        """
        xstructor = XStructor(llm_client=self)
        response = xstructor.do_xstructor_completion(messages, xml_example, xml_schema, mode=mode)
        return response

    def do_instructor(
        self,
        messages: List[Dict[str, str]],
        response_model: Type[T],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Method for calling Instructor completions.
        """
        LLMClient.LOGGER.debug("Starting instructor completion...")
        try:
            patched_client = instructor.from_openai(OpenAI())
            response = patched_client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
                response_model=response_model,
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))

    def do_tool(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Method for calling tool using completions.
        """
        LLMClient.LOGGER.debug("Starting tool completion...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
                tools=tools,
                tool_choice="auto",
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))

    def do_string(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode,
    ) -> str:
        """
        Base method for calling completions.
        Returns a string.
        """
        LLMClient.LOGGER.debug("Starting string completion...")
        try:
            response: Any = self.do_completion(messages=messages, mode=mode)
            return f"{response.choices[0].message.content}"
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))

    def do_completion(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling completions.
        Returns a full completion object.
        """
        LLMClient.LOGGER.debug("Starting completion...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))
