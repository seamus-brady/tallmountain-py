# Copyright 2023 seamus@corvideon.ie, Corvideon Limited.
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

import unittest

from src.tallmountain.normative.analysis.user_intent import UserIntent, UserIntentAnalysis


class TestUserIntent(unittest.TestCase):

    def test_run_diagnostic_test(self):
        user_query = "I would like to know how to make a cake"
        user_intent_analysis = UserIntent().analyse(user_task=user_query)
        self.assertIsInstance(user_intent_analysis, UserIntentAnalysis)
        self.assertIsInstance(user_intent_analysis.UserIntentScore, int)
        self.assertIsInstance(user_intent_analysis.Analysis, str)


if __name__ == "__main__":
    unittest.main()
