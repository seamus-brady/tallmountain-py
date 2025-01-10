#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.normative.analysis.norm_conflict_analyser import (
    NormativeConflictAnalyser,
    NormativeConflictAnalysis,
)
from src.tallmountain.normative.normative_agent import NormativeAgent
from src.tallmountain.normative.normative_proposition import NormativeProposition


class TestNormPropConflictAnalyser(unittest.TestCase):

    def setUp(self):
        self.analyser = NormativeConflictAnalyser()
        self.agent = NormativeAgent()
        self.norm_prop = NormativeProposition(
            proposition_value="People should act with honesty in all interactions.",
            operator="OUGHT",
            level="ETHICAL_MORAL",
            modality="POSSIBLE",
            modal_subscript="PRACTICAL",
        )

    def test_analyse(self):
        result = self.analyser.analyse(self.norm_prop, self.agent)
        self.assertIsInstance(result, NormativeConflictAnalysis)
        self.assertEqual(result.UserNormPropValue, self.norm_prop.proposition_value)
        self.assertIn(result.RiskLevel, ["Low", "Moderate", "High", "Critical"])


if __name__ == "__main__":
    unittest.main()
