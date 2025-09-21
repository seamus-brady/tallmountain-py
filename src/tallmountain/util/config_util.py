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

from configparser import ConfigParser

from src.tallmountain.exceptions.config_exception import ConfigException
from src.tallmountain.util.file_path_util import FilePathUtil


# a class for managing a config file
class ConfigUtil:
    APP_CONFIG_FILE: str = "src/config/app.ini"
    HIGHEST_ENDEAVOUR_JSON: str = "src/config/highest_endeavour.json"
    SYSTEM_ENDEAVOURS_JSON: str = "src/config/system_endeavours.json"
    NORM_COMPARISON_SCORE_PROMPT: str = "src/config/prompts/norm_comparison_score.prompt"
    SIMPLIFIED_NC: str = "src/config/prompts/simplified_nc.prompt"

    @staticmethod
    def get_str(section: str, setting: str, custom_config_file: str = None) -> str:
        config = ConfigParser()
        config.read(ConfigUtil.config_path(custom_config_file))
        return config.get(section, setting)

    @staticmethod
    def get_int(section: str, setting: str, custom_config_file: str = None) -> int:
        config = ConfigParser()
        config.read(ConfigUtil.config_path(custom_config_file))
        return config.getint(section, setting)

    @staticmethod
    def get_float(section: str, setting: str, custom_config_file: str = None) -> float:
        config = ConfigParser()
        config.read(ConfigUtil.config_path(custom_config_file))
        return config.getfloat(section, setting)

    @staticmethod
    def get_bool(section: str, setting: str, custom_config_file: str = None) -> bool:
        config = ConfigParser()
        config.read(ConfigUtil.config_path(custom_config_file))
        return config.getboolean(section, setting)

    @staticmethod
    def config_path(custom_config_file: str = None) -> str:
        if custom_config_file is not None:
            return FilePathUtil.append_path_to_repo_path(custom_config_file)
        return FilePathUtil.append_path_to_repo_path(ConfigUtil.APP_CONFIG_FILE)

    @staticmethod
    def highest_endeavour_json() -> str:
        try:
            source_path = FilePathUtil.append_path_to_repo_path(ConfigUtil.HIGHEST_ENDEAVOUR_JSON)
            return FilePathUtil.load_file_as_string(source_path)
        except Exception as error:  # noqa
            raise ConfigException(str(error))

    @staticmethod
    def system_endeavours_json() -> str:
        try:
            source_path = FilePathUtil.append_path_to_repo_path(ConfigUtil.SYSTEM_ENDEAVOURS_JSON)
            return FilePathUtil.load_file_as_string(source_path)
        except Exception as error:  # noqa
            raise ConfigException(str(error))

    @staticmethod
    def norm_comparison_score_prompt() -> str:
        try:
            source_path = FilePathUtil.append_path_to_repo_path(
                ConfigUtil.NORM_COMPARISON_SCORE_PROMPT
            )
            return FilePathUtil.load_file_as_string(source_path)
        except Exception as error:  # noqa
            raise ConfigException(str(error))

    @staticmethod
    def simplified_nc_prompt() -> str:
        try:
            source_path = FilePathUtil.append_path_to_repo_path(ConfigUtil.SIMPLIFIED_NC)
            return FilePathUtil.load_file_as_string(source_path)
        except Exception as error:  # noqa
            raise ConfigException(str(error))
