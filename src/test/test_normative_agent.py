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

import unittest

from src.tallmountain.normative.entities.endeavour import Endeavour
from src.tallmountain.normative.normative_agent import NormativeAgent
from src.tallmountain.normative.normative_proposition import NormativeProposition


class TestNormativeAgent(unittest.TestCase):

    def test_load_highest_endeavour(self):
        agent = NormativeAgent()
        self.assertIsInstance(agent.highest_endeavour, Endeavour)
        self.assertTrue(len(agent.highest_endeavour.normative_propositions) > 0)
        for proposition in agent.highest_endeavour.normative_propositions:
            self.assertIsInstance(proposition, NormativeProposition)

    def test_load_system_endeavours(self):
        agent = NormativeAgent()
        self.assertIsInstance(agent.system_endeavours, list)
        self.assertTrue(len(agent.system_endeavours) > 0)
        for endeavour in agent.system_endeavours:
            self.assertIsInstance(endeavour, Endeavour)
            self.assertTrue(len(endeavour.normative_propositions) > 0)
            for proposition in endeavour.normative_propositions:
                self.assertIsInstance(proposition, NormativeProposition)
        self.assertIsNotNone(agent.highest_endeavour_to_md())

    def test_highest_endeavour_md(self):
        agent = NormativeAgent()
        print(agent.highest_endeavour_to_md())
        self.assertIsNotNone(agent.highest_endeavour_to_md())

    def test_system_endeavours_md(self):
        agent = NormativeAgent()
        print(agent.system_endeavours_to_md())
        self.assertIsNotNone(agent.system_endeavours_to_md())


if __name__ == "__main__":
    unittest.main()
