#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.normative.analysis.self_diagnostic import (
    NormativeDiagnostic,
    NormativeSelfDiagnostic,
)


class TestNormativeSelfDiagnostic(unittest.TestCase):

    def setUp(self):
        self.diagnostic = NormativeSelfDiagnostic()

    def test_run_diagnostic_test(self):
        result = self.diagnostic.run_diagnostic_test()
        self.assertIsInstance(result, NormativeDiagnostic)
        self.assertIn(result.PassedDiagnostic, ["True", "False"])
        self.assertIsInstance(result.Analysis, str)


if __name__ == "__main__":
    unittest.main()
