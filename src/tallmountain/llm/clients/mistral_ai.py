#  Copyright (c) 2024 Seamus Brady seamus@ontal.ai, Corvideon Ltd.
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
#

import os
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
)

import instructor
from dotenv import load_dotenv
from mistralai import Mistral

from src.tallmountain.exceptions.llm_exception import LLMException
from src.tallmountain.llm.llm_client import (
    LLMClient,
    T,
)
from src.tallmountain.modes.adaptive_request_mode import AdaptiveRequestMode
from src.tallmountain.util.logging_util import LoggingUtil

# take environment variables from .env.
load_dotenv()

# mistral.ai public api
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]


class MistralAPIClient(LLMClient):
    """An interface to Mistral API. Used only from within the LLM facade parent class."""

    DEFAULT_MODEL = "mistral-large-latest"
    # DEFAULT_MODEL = "open-mixtral-8x22b"

    LOGGER = LoggingUtil.instance("<MistralAPIClient>")

    def __init__(self) -> None:
        super().__init__()
        MistralAPIClient.LOGGER.info("Initializing MistralAPIClient...")
        self._model = self.DEFAULT_MODEL
        self._api_key = MISTRAL_API_KEY
        self._llm_client = Mistral(api_key=self._api_key)

    def do_instructor(
        self,
        messages: Any,
        response_model: Type[T],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling Instructor completions.
        This patches the Mistral client to allow the use of a response_model.
        Returns a full completion object.
        """
        LLMClient.LOGGER.debug("Starting instructor completion...")
        try:
            patched_client = instructor.from_mistral(
                client=Mistral(api_key=self._api_key),
                mode=instructor.Mode.MISTRAL_TOOLS,
            )
            response = patched_client.chat.completions.create(
                model=self.model,
                messages=messages,
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
        Base method for calling tool using completions.
        Returns a full completion object.
        """
        LLMClient.LOGGER.debug("Starting tool completion...")
        try:
            response = self._llm_client.chat(
                model=self.model,
                messages=messages,
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
            response = self._llm_client.chat(
                model=self.model,
                messages=messages,
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))
