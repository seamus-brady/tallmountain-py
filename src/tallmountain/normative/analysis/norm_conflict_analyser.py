#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from typing import Literal

from pydantic import (
    BaseModel,
    Field,
)

from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages
from src.tallmountain.normative.normative_agent import NormativeAgent
from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.config_util import ConfigUtil
from src.tallmountain.util.logging_util import LoggingUtil


class NormativeConflictAnalysis(BaseModel):
    """A response model for normative conflict analysis."""

    UserNormPropValue: str = Field(
        ..., description="The user's normative proposition value."
    )
    Likelihood: int = Field(..., description="The likelihood value as an integer.")
    ImpactScore: int = Field(..., description="The impact score as an integer.")
    NormAlignmentScore: int = Field(
        ..., description="The normative alignment score as an integer."
    )
    ContextMultiplier: float = Field(
        ..., description="The context multiplier as a decimal."
    )
    RiskScore: float = Field(..., description="The risk score as a decimal.")
    RiskLevel: Literal["Low", "Moderate", "High", "Critical"] = Field(
        ...,
        description="The risk level, one of 'Low', 'Moderate', 'High', or 'Critical'.",
    )
    Analysis: str = Field(..., description="The analysis description.")


class NormativeConflictAnalyser:
    """
    A class for analysing normative conflicts
    """

    LOGGER = LoggingUtil.instance("<NormativeConflictAnalyser>")

    def __init__(self) -> None:
        self.LOGGER.info("Initializing NormativeConflictAnalyser")

    def analyse(
        self, norm_prop: NormativeProposition, agent: NormativeAgent
    ) -> NormativeConflictAnalysis:
        self.LOGGER.info("Starting analysis of normative conflict")
        llm: LLM = LLM()
        llm_messages = LLMMessages()
        llm_messages = llm_messages.build(
            "You are an expert in ethical analysis.", llm_messages.SYSTEM
        )

        prompt: str = f"""
        === INSTRUCTIONS ===
        - Your task is to see if there is a conflict between the norms of the AI Assistant and the norms that have been
          given to the AI Assistant by a user. Please provide an analysis of what you find.
        - You can use the Normative Calculus to provide an analysis of the user's normative proposition by using
          the AI Assistant's endeavours as an Exogenous Assessment.
        - You must provide a risk score using the scoring metric provided.
        - Also provide an analysis of your findings in a markdown table.

        === BEGIN AI ASSISTANT'S ENDEAVOURS ===
        {agent.highest_endeavour_to_md()}
        --------------------------------------
        {agent.system_endeavours_to_md()}
        === END AI ASSISTANT'S ENDEAVOURS  ===

        === BEGIN USER NORM PROP ===
        {norm_prop.to_markdown()}
        === END USER NORM PROP ===

        === BEGIN NORMATIVE CALCULUS ===
        {ConfigUtil.simplified_nc_prompt()}
        === END NORMATIVE CALCULUS ===

        === SCORING METRIC ===
        {ConfigUtil.norm_comparison_score_prompt()}
        === SCORING METRIC ===
        """
        llm_messages = llm_messages.build(prompt, llm_messages.USER)
        response: NormativeConflictAnalysis = llm.do_instructor(
            messages=llm_messages.messages, response_model=NormativeConflictAnalysis
        )
        self.LOGGER.info("Completed analysis of normative conflict")
        return response
