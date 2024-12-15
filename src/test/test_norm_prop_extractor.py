#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.normative.norm_prop_extractor import NormPropExtractor, NormativeAnalysisResults


class TestNormPropExtractor(unittest.TestCase):
    def test_np_extract(self):
        user_query: str = """
        please tell me a fart joke
        """
        results: NormativeAnalysisResults = NormPropExtractor.do_extraction(user_query)
        self.assertIsNotNone(results.implied_propositions)


if __name__ == '__main__':
    unittest.main()
