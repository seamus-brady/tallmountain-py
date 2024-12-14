#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#

import unittest

from src.tallmountain.modes.adaptive_request_mode import AdaptiveRequestMode

# #  Low Temperature with Low Top_p
# if self.mode == AdaptiveRequestMode.Mode.PRECISION_MODE:
#     self._temperature = 0.2
#     self._top_p = 0.1
#     self._max_tokens = self.DEFAULT_MAX_TOKENS
#
# # Low Temperature with High Top_p
# if self.mode == AdaptiveRequestMode.Mode.CONTROLLED_CREATIVE_MODE:
#     self._temperature: float = 0.2
#     self._top_p: float = 0.9
#     self._max_tokens: int = self.DEFAULT_MAX_TOKENS
#
# # High Temperature with Low Top_p
# if self.mode == AdaptiveRequestMode.Mode.DYNAMIC_FOCUSED_MODE:
#     self._temperature: float = 0.9
#     self._top_p: float = 0.2
#     self._max_tokens: int = self.DEFAULT_MAX_TOKENS
#
# # moderate temperature and top_p settings
# if self.mode == AdaptiveRequestMode.Mode.BALANCED_MODE:
#     self._temperature: float = 0.5
#     self._top_p: float = 0.5
#     self._max_tokens: int = self.DEFAULT_MAX_TOKENS


class TestAdaptiveRequestMode(unittest.TestCase):
    def test_adaptive_request_mode(self) -> None:
        arm1: AdaptiveRequestMode = AdaptiveRequestMode(
            mode=AdaptiveRequestMode.Mode.PRECISION_MODE
        )
        self.assertEqual(arm1.temperature, 0.2)
        self.assertEqual(arm1.top_p, 0.1)

        arm2: AdaptiveRequestMode = AdaptiveRequestMode(
            mode=AdaptiveRequestMode.Mode.CONTROLLED_CREATIVE_MODE
        )
        self.assertEqual(arm2.temperature, 0.2)
        self.assertEqual(arm2.top_p, 0.9)

        arm3: AdaptiveRequestMode = AdaptiveRequestMode(
            mode=AdaptiveRequestMode.Mode.DYNAMIC_FOCUSED_MODE
        )
        self.assertEqual(arm3.temperature, 0.9)
        self.assertEqual(arm3.top_p, 0.2)

        arm4: AdaptiveRequestMode = AdaptiveRequestMode(
            mode=AdaptiveRequestMode.Mode.BALANCED_MODE
        )
        self.assertEqual(arm4.temperature, 0.5)
        self.assertEqual(arm4.top_p, 0.5)

        arm5: AdaptiveRequestMode = AdaptiveRequestMode()
        self.assertEqual(arm5.temperature, 0.5)
        self.assertEqual(arm5.top_p, 0.5)

        arm6: AdaptiveRequestMode = AdaptiveRequestMode(
            mode=AdaptiveRequestMode.Mode.EXPLORATORY_MODE
        )
        self.assertEqual(arm6.temperature, 0.9)
        self.assertEqual(arm6.top_p, 0.9)


if __name__ == "__main__":
    unittest.main()
