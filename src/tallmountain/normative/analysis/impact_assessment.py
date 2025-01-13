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


class ImpactAssessmentResult(BaseModel):
    ImpactAssessmentScore: int = Field(
        ..., description="The impact assessment score as an integer."
    )
    Analysis: str = Field(
        ..., description="String describing the analysis of the impact assessment."
    )


class ImpactAssessment:
    """Returns an impact assessment score for the user task"""

    LOGGER = LoggingUtil.instance("<ImpactAssessment>")

    def __init__(self) -> None:
        pass

    def analyse(self, user_task: str) -> ImpactAssessmentResult:
        """Does an impact assessment on the user task"""

        self.LOGGER.info("Analyzing the task to get a User Intent Score (UIS)...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
            === INSTRUCTIONS ===

            Impact Assessment Score (IAS)
    
            You are an expert classifier tasked with assigning an Impact Assessment Score (IAS) to user queries.
            The IAS is a numeric value between 1 and 10:
    
            1 = Minimal impact
    
            10 = Maximum impact
    
            During a risk assessment, impact is typically measured by evaluating the potential consequences of a risk event
            on an individual, organization or system. This measurement often involves both qualitative and quantitative
            approaches, depending on the context and the resources available.
    
            The process generally includes the following steps:
    
            1. Identify Impact Domains
    
                Financial Impact: Direct costs, lost revenue, or increased operational costs.
                Reputational Impact: Damage to brand, customer trust, or public perception.
                Operational Impact: Disruption to processes, reduced efficiency, or system downtime.
                Regulatory/Legal Impact: Fines, legal consequences, or non-compliance penalties.
                Safety Impact: Risks to human life, health, or the environment.
    
            2. Establish Metrics
    
                Qualitative Metrics: Use of descriptive scales (e.g., "low," "medium," "high") to assess non-numeric impacts
                like reputational harm.
                Quantitative Metrics: Numeric estimates (e.g., dollar amounts, downtime in hours) for measurable impacts.
    
            3. Scenario Analysis
    
                Best-Case, Worst-Case, and Most Likely Scenarios: Evaluate the range of outcomes to capture variability in
                potential impact.
                Historical Data: Use past incidents to estimate possible impacts.
    
            4. Assign Impact Scores
    
                Develop a scoring model (e.g., 1-5 or 1-10) where higher scores represent greater severity.
                Include thresholds for each domain to standardize the assessment.
    
            5. Evaluate and Prioritize
    
                Combine impact scores with likelihood to prioritize risks using methods like a risk matrix.
                Consider interdependencies or cascading effects that may amplify impacts.
    
            For example, a cyberattack might be assessed as having:
    
                Financial Impact: Large recovery costs and/or lost revenue.
                Reputational Impact: "Medium" damage to customer trust.
                Operational Impact: Two days of downtime.
    
            The cumulative evaluation informs decision-making for risk mitigation and resource allocation.

            === USER TASK ===
            {user_task}

            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: ImpactAssessmentResult = llm.do_instructor(
                messages=llm_messages.messages, response_model=ImpactAssessmentResult
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise NormativeException(str(error))
