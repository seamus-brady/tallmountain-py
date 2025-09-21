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

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Optional

import ray

readline: Optional[ModuleType]
try:
    import readline
except ImportError:
    readline = None

# path fix for imports ----------------------------------------------
path = Path(os.path.dirname(os.path.realpath(__file__)))
print(path.absolute().__str__())
sys.path.append(path.absolute().__str__())
sys.path.append(path.parent.absolute().__str__())
sys.path.append(path.parent.parent.absolute().__str__())
sys.path.append(path.parent.parent.parent.absolute().__str__())
# path fix for imports ----------------------------------------------

from src.tallmountain.normative.analysis.impact_assessment import (  # noqa: E402
    ImpactAssessment,
    ImpactAssessmentResult,
)
from src.tallmountain.normative.analysis.norm_risk_analysis import (
    NormativeRiskAnalysis,
)  # noqa: E402
from src.tallmountain.normative.analysis.np_extractor import (  # noqa: E402
    NormativeAnalysisResults,
    NormPropExtractor,
)
from src.tallmountain.normative.analysis.self_diagnostic import (
    NormativeSelfDiagnostic,
)  # noqa: E402
from src.tallmountain.normative.analysis.user_intent import (  # noqa: E402
    UserIntent,
    UserIntentAnalysis,
)
from src.tallmountain.normative.entities.user_task import UserTask  # noqa: E402
from src.tallmountain.normative.normative_agent import NormativeAgent  # noqa: E402
from src.tallmountain.util.config_util import ConfigUtil  # noqa: E402

# logging setup
logging.basicConfig(level=logging.DEBUG)
APP_LOGGER = logging.getLogger("<TallMountain App>")

# command constants
NRP_COMMAND = ":nrp"
IAS_COMMAND = ":ias"
UIS_COMMAND = ":uis"
NP_COMMAND = ":np"
HELP_COMMAND = ":h"
QUIT_COMMAND = ":q"


def check_api_key():
    if os.getenv("OPENAI_API_KEY") is None:
        msg = "OPENAI_API_KEY environment variable not found"
        APP_LOGGER.debug(msg)
        raise EnvironmentError(msg)


def perform_self_diagnosis():
    APP_LOGGER.debug("Running the normative calculus self-diagnostic...")
    diagnostic = NormativeSelfDiagnostic()
    result = diagnostic.run_diagnostic_test()
    if result.PassedDiagnostic == "False":
        msg = f"Sorry, the normative calculus self-diagnostic failed: {result.Analysis}"
        APP_LOGGER.debug(msg)
        raise RuntimeError(msg)
    else:
        APP_LOGGER.debug("Normative calculus self-diagnostic passed successfully!")


def printf_implied_propositions(result: NormativeAnalysisResults):
    print("Implied Normative Propositions:")
    for prop in result.implied_propositions.NormativePropositions:
        print(f"    - level: {prop.level}")
        print(f"      modal_subscript: {prop.modal_subscript}")
        print(f"      modality: {prop.modality}")
        print(f"      operator: {prop.operator}")
        print(f"      proposition_value: {prop.proposition_value}\n")
    print(f"User Query Provided:\n    {result.input_statement}")


def printf_uis(result: UserIntentAnalysis):
    print("User Intent Score:")
    print(f"Score:\n  {result.UserIntentScore}")
    print(f"Analysis:\n  {result.Analysis}")


def printf_ias(result: ImpactAssessmentResult):
    print("Impact Assessment Score:")
    print(f"Score:\n  {result.ImpactAssessmentScore}")
    print(f"Analysis:\n  {result.Analysis}")


def printf_nrp(risk_profile: NormativeRiskAnalysis):
    print("Normative Risk Profile:")
    for analysis in risk_profile.analyses:
        print("## Analysis\n")
        print(f"- **UserNormPropValue**: {analysis.UserNormPropValue}")
        print(f"- **Likelihood**: {analysis.Likelihood}")
        print(f"- **ImpactScore**: {analysis.ImpactScore}")
        print(f"- **NormAlignmentScore**: {analysis.NormAlignmentScore}")
        print(f"- **ContextMultiplier**: {analysis.ContextMultiplier}")
        print(f"- **RiskScore**: {analysis.RiskScore}")
        print(f"- **RiskLevel**: {analysis.RiskLevel}")
        print(f"- **Analysis**: {analysis.Analysis}\n")
    print(f"Recommendation: {risk_profile.recommendation}")
    print(f"Explanation: {risk_profile.explain()}")


def print_process_time(start_time, line):
    response = f"Processed: {line}"
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    print(f"\nTallMountain (TMAI):> {response} (Elapsed time: {elapsed_time:.2f} seconds)")


def main():
    APP_LOGGER.debug("Starting TallMountain REPL... please wait")

    check_api_key()
    perform_self_diagnosis()

    # start ray
    ray.init(ignore_reinit_error=True)

    APP_LOGGER.debug("Getting a cognitive cycle instance...")
    app_version = ConfigUtil.get_str("app", "version")
    print(
        "\n=========================================================================================="
    )
    print(
        f"Welcome to TallMountain {app_version}. \nType ':help' for a list of commands or :quit to exit"
    )
    print(
        "==========================================================================================\n"
    )

    while True:
        try:
            line = input("TallMountain (USER):> ").strip()
            start_time = datetime.now()

            if line in [QUIT_COMMAND]:
                print("Goodbye!")
                break

            if line in [HELP_COMMAND]:
                APP_LOGGER.debug("User requested help information.")
                print(
                    "Available commands:\n"
                    f"{QUIT_COMMAND}  - Exit the REPL\n"
                    f"{HELP_COMMAND}  - Show this help message\n"
                    f"{NP_COMMAND}    - Extracts normative propositions from a query\n"
                    f"{UIS_COMMAND}   - Gets the User Intent Score for the query\n"
                    f"{IAS_COMMAND}   - Gets the Impact Assessment Score for the query\n"
                    f"{NRP_COMMAND}   - Get a Normative Risk Profile for the query"
                )
                continue

            if line.startswith(NP_COMMAND):
                query = line[4:].strip()
                norm_extractor = NormPropExtractor()
                norm_props = norm_extractor.do_xml_extraction(query)
                print(norm_props)
                printf_implied_propositions(norm_props)
                print_process_time(start_time, line)
                continue

            if line.startswith(UIS_COMMAND):
                query = line[5:].strip()
                uis_analysis = UserIntent()
                uis: UserIntentAnalysis = uis_analysis.analyse(query)
                printf_uis(uis)
                print_process_time(start_time, line)
                continue

            if line.startswith(IAS_COMMAND):
                query = line[5:].strip()
                ias_analysis = ImpactAssessment()
                ias: ImpactAssessmentResult = ias_analysis.analyse(query)
                printf_ias(ias)
                print_process_time(start_time, line)
                continue

            if line.startswith(NRP_COMMAND):
                query = line[5:].strip()
                user_task: UserTask = UserTask.get_from_query(query)
                risk_analysis: NormativeRiskAnalysis = NormativeRiskAnalysis()
                agent = NormativeAgent()
                risk_analysis.analyse(user_task, agent)
                printf_nrp(risk_analysis)
                print_process_time(start_time, line)
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            ray.shutdown()


if __name__ == "__main__":
    main()
