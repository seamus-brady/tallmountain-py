#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from configparser import ConfigParser

from src.tallmountain.util.file_path_util import FilePathUtil


# a class for managing a config file
class ConfigUtil:
    APP_CONFIG_FILE: str = "app.ini"

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
            return FilePathUtil.append_path_to_app_path(custom_config_file)
        return FilePathUtil.append_path_to_app_path(ConfigUtil.APP_CONFIG_FILE)
