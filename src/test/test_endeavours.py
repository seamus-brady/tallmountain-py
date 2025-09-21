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

    def test_to_markdown(self):
        print(self.endeavour.to_markdown())
        self.assertIsNotNone(self.endeavour.to_markdown())


if __name__ == "__main__":
    unittest.main()
