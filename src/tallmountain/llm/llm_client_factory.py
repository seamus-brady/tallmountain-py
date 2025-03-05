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
from src.tallmountain.exceptions.llm_exception import LLMException
from src.tallmountain.llm.clients.openai import OpenAIClient
from src.tallmountain.llm.llm_client import LLMClient
from src.tallmountain.util.config_util import ConfigUtil


class LLMClientFactory:
    """
    Instantiates the correct LLMClient based on config.
    """

    OPENAI_PROVIDER_STRING = "OpenAIClient"

    @staticmethod
    def llm_client() -> LLMClient:
        try:
            default_llm_provider: str = ConfigUtil.get_str("llm", "default_llm_provider")
            if default_llm_provider is None:
                raise LLMException("No default_llm_provider found!")
            elif default_llm_provider == LLMClientFactory.OPENAI_PROVIDER_STRING:
                return OpenAIClient()
            else:
                raise LLMException("No default_llm_provider found!")
        except Exception as error:
            raise LLMException(str(error))
