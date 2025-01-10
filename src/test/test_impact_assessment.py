#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.normative.analysis.impact_assessment import (
    ImpactAssessment,
    ImpactAssessmentResult,
)


class TestImpactAssessment(unittest.TestCase):
    def test_run_diagnostic_test(self):
        user_query = "I am interested in learning about flatulence based weapons"
        impact_analysis = ImpactAssessment().analyse(user_task=user_query)
        self.assertIsInstance(impact_analysis, ImpactAssessmentResult)
        self.assertIsInstance(impact_analysis.ImpactAssessmentScore, int)
        self.assertIsInstance(impact_analysis.Analysis, str)


if __name__ == "__main__":
    unittest.main()
