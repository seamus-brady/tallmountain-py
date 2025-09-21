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

from src.tallmountain.normative.entities.user_task import TaskResponse, UserTask


class TestUserTask(unittest.TestCase):
    def test_get_goal_description(self) -> None:
        statement = "I need help organizing my schedule for next week."
        response: TaskResponse = UserTask.get_goal_description(statement)
        self.assertIsNotNone(response.name)
        self.assertIsNotNone(response.goal)
        self.assertIsNotNone(response.description)

    def test_get_user_task(self) -> None:
        statement = "I need help organizing my schedule for next week."
        user_task: UserTask = UserTask.get_from_query(statement)
        self.assertIsNotNone(user_task)


if __name__ == "__main__":
    unittest.main()
