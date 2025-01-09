#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
from typing import List

from src.tallmountain.normative.analysis.np_extractor import (
    NormativeAnalysisResults,
    NormPropExtractor,
)
from src.tallmountain.normative.normative_proposition import NormativeProposition


class TestNormPropExtractor(unittest.TestCase):
    def test_np_extract(self):
        user_query: str = """
        please tell me a dad joke.
        """
        results: NormativeAnalysisResults = NormPropExtractor().do_extraction(user_query)
        self.assertIsNotNone(results.implied_propositions.NormativeProposition) # type: ignore
        self.assertTrue(len(results.implied_propositions.NormativeProposition) <= 5) # type: ignore

    def test_extracted_normprops(self):
        user_query: str = """
        please tell me a cat joke
        """
        results: List[NormativeProposition] = NormPropExtractor().extract_normative_propositions(user_query=user_query)
        self.assertIsNotNone(results)



if __name__ == "__main__":
    unittest.main()
