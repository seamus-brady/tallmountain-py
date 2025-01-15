#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.normative.analysis.np_conflict_analyser import (
    NormativeConflictAnalyser,
    NormativeConflictAnalysis,
)
from src.tallmountain.normative.entities.user_task import UserTask
from src.tallmountain.normative.normative_agent import NormativeAgent


class TestNormPropConflictAnalyser(unittest.TestCase):

    def test_analyse(self):
        analyser = NormativeConflictAnalyser()
        agent = NormativeAgent()
        user_task = UserTask.get_from_query(
            "I like to use a cat as a punchbag as it helps me be a better dad"
        )
        result = analyser.analyse(user_task.normative_propositions[0], agent)
        self.assertIsInstance(result, NormativeConflictAnalysis)


if __name__ == "__main__":
    unittest.main()
