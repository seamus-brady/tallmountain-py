#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import Counter
from typing import List

import ray

from src.tallmountain.exceptions.normative_exception import NormativeException
from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages
from src.tallmountain.normative.analysis.np_conflict_analyser import (
    NormativeConflictAnalyser,
    NormativeConflictAnalysis,
)
from src.tallmountain.normative.entities.endeavour import Endeavour
from src.tallmountain.normative.normative_agent import NormativeAgent
from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.config_util import ConfigUtil
from src.tallmountain.util.logging_util import LoggingUtil


class NormativeRiskAnalysis:
    """Provide a risk analysis of normative propositions from an endeavour."""

    LOGGER = LoggingUtil.instance("<NormativeRiskAnalysis>")

    ACCEPT_AND_EXECUTE = "Accept and Execute"
    SUGGEST_MODIFICATION = "Suggest Modification"
    REJECT = "Reject"

    # thresholds for risk levels
    MAX_CRITICAL: int = ConfigUtil.get_int("normative_analysis", "number_critical_risks_allowed")
    MAX_HIGH: int = ConfigUtil.get_int("normative_analysis", "number_high_risks_allowed")
    MAX_MODERATE: int = ConfigUtil.get_int("normative_analysis", "number_moderate_risks_allowed")

    # I am sorry Dave, I am afraid I cannot do that
    REJECTION_MESSAGE: str = ConfigUtil.get_str("normative_analysis", "rejection_message")

    # OK Dave, I can do that
    ACCEPTABLE_TO_PROCESS = "The user task is acceptable to process."

    def __init__(self):
        self._analyses: List[NormativeConflictAnalysis] = []
        self._recommendation: str = ""

    @property
    def analyses(self) -> List[NormativeConflictAnalysis]:
        return self._analyses

    @property
    def recommendation(self) -> str:
        if self._recommendation == "":
            return self.recommend_action(self.analyses)
        return self._recommendation

    def analyse(
        self,
        endeavour: Endeavour,
        agent: NormativeAgent = None,
    ) -> List[NormativeConflictAnalysis]:
        """Analyse the risk of a normative proposition."""
        self.LOGGER.info("Analyzing the risk of an endeavour")

        @ray.remote
        def do_np_conflict_analysis(
            analyser: NormativeConflictAnalyser,
            np: NormativeProposition,
            agent: NormativeAgent,
        ) -> NormativeConflictAnalysis:
            return analyser.analyse(np, agent)

        analyser = NormativeConflictAnalyser()

        try:
            # Create a list of remote tasks
            futures = [
                do_np_conflict_analysis.remote(analyser, np, agent)
                for np in endeavour.normative_propositions
            ]

            # Collect results
            analyses = ray.get(futures)
            # store the analyses
            self._analyses = analyses
            return analyses
        except Exception as error:
            self.LOGGER.error(str(error))
            raise NormativeException(str(error))

    def count_risk_levels(self, analyses: List[NormativeConflictAnalysis]) -> Counter:
        risk_levels = [analysis.RiskLevel for analysis in analyses]
        return Counter(risk_levels)

    def recommend_action(self, analyses: List[NormativeConflictAnalysis]) -> str:
        """Recommend an action based on the analysis."""
        self.LOGGER.info("Recommending an action based on the analysis")

        risk_level_counts: Counter = self.count_risk_levels(analyses)

        if risk_level_counts["Critical"] >= self.MAX_CRITICAL:
            self.LOGGER.debug("Critical found - recommending REJECT")
            return self.REJECT
        elif risk_level_counts["High"] >= self.MAX_HIGH:
            self.LOGGER.debug("High found - recommending REJECT")
            return self.REJECT
        elif risk_level_counts["Moderate"] >= self.MAX_MODERATE:
            print("Too many Moderates found")
            self.LOGGER.debug("Too many Moderates found - recommending SUGGEST_MODIFICATION")
            return self.SUGGEST_MODIFICATION
        else:
            self.LOGGER.debug("No risk found - recommending ACCEPT_AND_EXECUTE")
            return self.ACCEPT_AND_EXECUTE

    def explain(self, analyses: List[NormativeConflictAnalysis] = None) -> str:
        """Explain the analysis."""
        self.LOGGER.info("Explaining the analysis")
        try:

            if analyses is None:
                analyses = self.analyses

            if self.recommendation == "":
                recommendation = self.recommend_action(analyses)
            else:
                recommendation = self.recommendation

            if recommendation == self.REJECT:
                return self.REJECTION_MESSAGE

            if recommendation == self.SUGGEST_MODIFICATION:
                llm: LLM = LLM()
                llm_messages = LLMMessages()
                prompt = f"""
                 === INSTRUCTIONS ===
                - Please summarise the risk results below in simple English and explain why the AI Assistant has
                  suggested changing the task. Make some suggestions on how to modify the task.
                - You should make the explanation in the first person. Use 'my' rather than 'the' when talking about the
                  analysis. Rather than say 'the user', say 'you' or 'your' as appropriate.
                - Apologise and say you think the request should be modified and then explain.
                - You can mention the scores if appropriate, but leave out the actual numbers.
                - Be concise, you don't need to enumerate all the risks but be specific about what the user wanted you to do
                  and what you are meant to do as an AI Assistant.  But be conversational.
                - Don't use the word 'norm' as it is quite technical.
                - Don't use the work 'risk' rather just explain the situation.
                === START RISK RESULTS ===
                {self.to_md(analyses)}
                === END RISK RESULTS ===
                """
                llm_messages = llm_messages.build(prompt, llm_messages.USER)
                response: str = llm.do_string_completion(messages=llm_messages.messages)
                return response

            if recommendation == self.ACCEPT_AND_EXECUTE:
                return self.ACCEPTABLE_TO_PROCESS

            error_msg = "Unknown recommendation"
            self.LOGGER.error(str(error_msg))
            raise NormativeException(str(error_msg))
        except Exception as error:
            self.LOGGER.error(str(error))
            raise NormativeException(str(error))

    def to_md(self, analyses: List[NormativeConflictAnalysis]) -> str:
        """Convert a list of NormativeConflictAnalysis into a markdown string."""
        md = "# Normative Conflict Analysis Results\n"
        for analysis in analyses:
            md += "## Analysis\n"
            md += f"- **UserNormPropValue**: {analysis.UserNormPropValue}\n"
            md += f"- **Likelihood**: {analysis.Likelihood}\n"
            md += f"- **ImpactScore**: {analysis.ImpactScore}\n"
            md += f"- **NormAlignmentScore**: {analysis.NormAlignmentScore}\n"
            md += f"- **ContextMultiplier**: {analysis.ContextMultiplier}\n"
            md += f"- **RiskScore**: {analysis.RiskScore}\n"
            md += f"- **RiskLevel**: {analysis.RiskLevel}\n"
            md += f"- **Analysis**: {analysis.Analysis}\n"
            md += "\n"
        return md
