#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Optional

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
    ImpactAssessment, ImpactAssessmentResult,
)
from src.tallmountain.normative.analysis.np_extractor import (  # noqa: E402
    NormativeAnalysisResults,
    NormPropExtractor,
)
from src.tallmountain.normative.analysis.self_diagnostic import (  # noqa: E402
    NormativeSelfDiagnostic,
)
from src.tallmountain.normative.analysis.user_intent import UserIntent, UserIntentAnalysis  # noqa: E402
from src.tallmountain.util.config_util import ConfigUtil  # noqa: E402

# Set up logger
logging.basicConfig(level=logging.DEBUG)
APP_LOGGER = logging.getLogger("<TallMountain App>")


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


def printf_nrp(risk_profile):
    print("Normative Risk Profile:")


def main():
    APP_LOGGER.debug("Starting TallMountain REPL... please wait")

    check_api_key()
    perform_self_diagnosis()

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

            if line in [":quit", ":q"]:
                print("Goodbye!")
                break

            if line in [":help", ":h"]:
                APP_LOGGER.debug("User requested help information.")
                print(
                    "Available commands:\n"
                    ":quit or :q      - Exit the REPL\n"
                    ":help or :h      - Show this help message\n"
                    ":np <query>      - Extracts normative propositions from a query\n"
                    ":uis <query>     - Gets the User Intent Score for the query\n"
                    ":ias <query>     - Gets the Impact Assessment Score for the query\n"
                    ":nrp <query>     - Get a Normative Risk Profile for the query"
                )
                continue

            if line.startswith(":np"):
                query = line[4:].strip()
                norm_extractor = NormPropExtractor()
                norm_props = norm_extractor.do_xml_extraction(query)
                print(norm_props)
                printf_implied_propositions(norm_props)
                continue

            if line.startswith(":uis"):
                query = line[5:].strip()
                uis_analysis = UserIntent()
                uis: UserIntentAnalysis = uis_analysis.analyse(query)
                printf_uis(uis)
                continue

            if line.startswith(":ias"):
                query = line[5:].strip()
                ias_analysis = ImpactAssessment()
                ias: ImpactAssessmentResult = ias_analysis.analyse(query)
                printf_ias(ias)
                continue

            if line.startswith(":nrp"):
                query = line[5:].strip()
                continue

            # Placeholder for cognitive cycle instance
            response = f"Processed: {line}"

            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            print(
                f"\nTallMountain (TMAI):> {response} (Elapsed time: {elapsed_time:.2f} seconds)"
            )

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
