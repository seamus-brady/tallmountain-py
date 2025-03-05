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
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.tallmountain.exceptions.llm_exception import LLMException
from src.tallmountain.util.logging_util import LoggingUtil

if TYPE_CHECKING:
    from typing import Self
else:
    Self = Any


class LLMMessages:
    """A class for managing prompts."""

    LOGGER = LoggingUtil.instance("<LLMMessages>")

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    TOOL = "tool"

    def __init__(self) -> None:
        self._messages: List[Dict[str, str]] = []

    @property
    def messages(self) -> List[Dict[str, str]]:
        return self._messages

    @messages.setter
    def messages(self, new_messages: List[Dict[str, str]]) -> None:
        self._messages = new_messages.copy()

    def build_user_prompt(self, content: str) -> Dict[str, str]:
        return {"role": "user", "content": content}

    def build_assistant_prompt(self, content: str) -> Dict[str, str]:
        return {"role": "assistant", "content": content}

    def build_system_prompt(self, content: str) -> Dict[str, str]:
        return {"role": "system", "content": content}

    def build_tool_prompt(self, tool_call: Any, function_name, content: str) -> Dict[str, str]:
        return {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": f"{content}",
        }

    def build(
        self,
        content: str,
        content_type: str,
        tool_call: Optional[Any] = None,
        function_name: Optional[Any] = None,
    ) -> Self:
        try:
            if content_type == self.SYSTEM:
                message = self.build_system_prompt(content)
                self.messages.append(message)
            if content_type == self.USER:
                message = self.build_user_prompt(content)
                self.messages.append(message)
            if content_type == self.ASSISTANT:
                message = self.build_assistant_prompt(content)
                self.messages.append(message)
            if content_type == self.TOOL:
                message = self.build_tool_prompt(tool_call, function_name, content)
                self.messages.append(message)
            return self
        except Exception as error:
            LLMMessages.LOGGER.error(str(error))
            raise LLMException(str(error))
