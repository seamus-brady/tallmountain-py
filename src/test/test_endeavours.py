#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.normative.entities.comprehensiveness import Comprehensiveness
from src.tallmountain.normative.entities.endeavour import Endeavour
from src.tallmountain.normative.normative_proposition import NormativeProposition


class TestEndeavours(unittest.TestCase):

    def setUp(self):
        self.norm_props = [
            NormativeProposition(
                proposition_value="People should act with honesty in all interactions."
            ),
            NormativeProposition(proposition_value="Respect for others is essential."),
        ]
        self.endeavour = Endeavour(
            name="Test Endeavour",
            description="A test endeavour",
            comprehensiveness=Comprehensiveness.HIGH,
            normative_propositions=self.norm_props,
        )

    def test_create_endeavour(self):
        endeavour = Endeavour.create(
            name="New Endeavour",
            description="A new endeavour",
            comprehensiveness=Comprehensiveness.LOW,
        )
        self.assertEqual(endeavour.name, "New Endeavour")
        self.assertEqual(endeavour.description, "A new endeavour")
        self.assertEqual(endeavour.comprehensiveness, Comprehensiveness.LOW)
        self.assertEqual(len(endeavour.normative_propositions), 0)

    def test_endeavour_str(self):
        expected_str = (
            "----\n"
            "Endeavour name: Test Endeavour\n"
            "description: A test endeavour\n"
            "comprehensiveness: Comprehensiveness.HIGH\n"
            "normative_propositions:\n"
            f"{self.norm_props[0]}\n"
            f"{self.norm_props[1]}\n"
            "----"
        )
        self.assertEqual(str(self.endeavour), expected_str)

    def test_to_markdown(self):
        print(self.endeavour.to_markdown())
        self.assertIsNotNone(self.endeavour.to_markdown())


if __name__ == "__main__":
    unittest.main()
