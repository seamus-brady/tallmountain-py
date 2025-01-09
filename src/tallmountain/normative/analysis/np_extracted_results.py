#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from src.tallmountain.util.config_util import ConfigUtil
from src.tallmountain.util.logging_util import LoggingUtil


class NormPropExtractionResults:
    """Results of normative proposition extraction."""

    LOGGER = LoggingUtil.instance("<NormPropExtractionResults>")

    MAX_EXTRACTED_NORMS: int = ConfigUtil.get_int(
        "norm_prop_extractor", "max_extracted_norms"
    )

    def new_from(self, user_query: str) -> None:
        for j in range(NormPropExtractionResults.MAX_EXTRACTED_NORMS):
            self.LOGGER.info(f"Extracted norm {j} from user query: {user_query}")
