#  Copyright 2023 seamus@ontal.ai, Corvideon Limited.
#  #
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import os
from pathlib import Path


# a class for handling file paths in the app
class FilePathUtil:
    @staticmethod
    def app_root_path() -> str:
        script_path: Path = Path(__file__)
        return script_path.parent.parent.absolute().__str__()

    @staticmethod
    def repo_root_path() -> str:
        script_path: Path = Path(__file__)
        return script_path.parent.parent.parent.parent.absolute().__str__()

    @staticmethod
    def model_path() -> str:
        return FilePathUtil.append_path_to_repo_path("models/")

    @staticmethod
    def storage_path() -> str:
        return FilePathUtil.append_path_to_repo_path("storage/")

    @staticmethod
    def append_path_to_app_path(path_str: str) -> str:
        app_root: str = FilePathUtil.app_root_path()
        return os.path.join(app_root, path_str)

    @staticmethod
    def append_path_to_repo_path(path_str: str) -> str:
        app_root: str = FilePathUtil.repo_root_path()
        return os.path.join(app_root, path_str)
