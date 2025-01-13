#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from instructor import Partial
from pydantic import BaseModel

from src.tallmountain.modes.adaptive_request_mode import AdaptiveRequestMode
from src.tallmountain.util.logging_util import LoggingUtil

# based on T in instructor.client.Instructor
T = TypeVar("T", bound=Union[BaseModel, Iterable, Partial])


class LLMClient:
    """Base LLM client class."""

    LOGGER = LoggingUtil.instance("<LLMClient>")

    def __init__(self) -> None:
        self._model: Optional[str] = None

    @property
    def model(self) -> Optional[str]:
        return self._model

    def do_instructor(
        self,
        messages: List[Dict[str, str]],
        response_model: Type[T],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling Instructor completions.
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def do_string(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode,
    ) -> str:
        """
        Base method for calling completions.
        Returns a string.
        """
        raise NotImplementedError

    def do_completion(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling completions.
        Returns a full completion object.
        """
        raise NotImplementedError
