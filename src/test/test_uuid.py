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

#
#
import unittest

from src.tallmountain.util.uuid_util import UUIDUtil


class TestUUID(unittest.TestCase):
    def test_uuid_str(self) -> None:
        my_uuid: str = UUIDUtil.get()
        self.assertIsNotNone(my_uuid)

    def test_session_uuid_str(self) -> None:
        my_uuid: str = UUIDUtil.get_session_uuid()
        self.assertIsNotNone(my_uuid)

    def test_cycle_uuid_str(self) -> None:
        my_uuid: str = UUIDUtil.get_cycle_uuid()
        self.assertIsNotNone(my_uuid)


if __name__ == "__main__":
    unittest.main()
