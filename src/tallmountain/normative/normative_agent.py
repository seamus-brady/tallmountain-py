#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
from typing import List

from src.tallmountain.exceptions.normative_exception import NormativeException
from src.tallmountain.normative.endeavour import Endeavour
from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.config_util import ConfigUtil


class NormativeAgent:
    """
    A class for managing the system's endeavours
    """

    def __init__(self):
        self.highest_endeavour: Endeavour = self.load_highest_endeavour()
        self.system_endeavours: List[Endeavour] = self.load_system_endeavours()

    def load_highest_endeavour(self) -> Endeavour:
        try:
            norm_props: List[NormativeProposition] = []
            json_data = ConfigUtil.highest_endeavour_json()
            endeavours = json.loads(json_data)
            for np_dict in endeavours['endeavours'][0]['normative_propositions']:
                norm_prop: NormativeProposition = NormativeProposition.from_dict(np_dict)
                norm_props.append(norm_prop)
            return Endeavour(
                name=endeavours['endeavours'][0]['name'],
                description=endeavours['endeavours'][0]['description'],
                normative_propositions=norm_props)
        except Exception as e:
            raise NormativeException(f"Failed to load highest endeavours: {str(e)}")

    def load_system_endeavours(self) -> List[Endeavour]:
        try:
            endeavours_list: List[Endeavour] = []
            json_data = ConfigUtil.system_endeavours_json()
            endeavours = json.loads(json_data)
            for endeavour_data in endeavours['endeavours']:
                norm_props: List[NormativeProposition] = [
                    NormativeProposition.from_dict(np_dict) for np_dict in endeavour_data['normative_propositions']
                ]
                endeavour = Endeavour(
                    name=endeavour_data['name'],
                    description=endeavour_data['description'],
                    normative_propositions=norm_props
                )
                endeavours_list.append(endeavour)
            return endeavours_list
        except Exception as e:
            raise NormativeException(f"Failed to load system endeavours: {str(e)}")
