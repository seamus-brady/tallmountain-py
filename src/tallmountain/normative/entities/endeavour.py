#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import uuid
from dataclasses import dataclass, field
from typing import List

from src.tallmountain.normative.entities.comprehensiveness import Comprehensiveness
from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.logging_util import LoggingUtil
from src.tallmountain.util.string_buffer_util import StringBuffer
from src.tallmountain.util.uuid_util import UUIDUtil


@dataclass
class Endeavour:
    """
    A base class for an entities of an agent. Manages a set of NormProps.
    """

    LOGGER = LoggingUtil.instance("<UserTask>")

    name: str
    description: str
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    comprehensiveness: Comprehensiveness = Comprehensiveness.DEFAULT
    normative_propositions: List[NormativeProposition] = field(default_factory=list)

    @staticmethod
    def create(
        name: str,
        description: str,
        uuid: str = None,
        comprehensiveness=Comprehensiveness.DEFAULT,
        normative_propositions: List[NormativeProposition] = None,
    ):
        Endeavour.LOGGER.info(f"Creating Endeavour: {name}")
        return Endeavour(
            name=name,
            description=description,
            uuid=uuid or str(UUIDUtil.get()),
            comprehensiveness=comprehensiveness,
            normative_propositions=normative_propositions or [],
        )

    def __str__(self) -> str:
        propositions_gist = "\n".join([np.__str__() for np in self.normative_propositions])
        return (
            f"----\n"
            f"Endeavour name: {self.name}\n"
            f"Endeavour UUID: {self.uuid}\n"
            f"description: {self.description}\n"
            f"comprehensiveness: {self.comprehensiveness}\n"
            f"normative_propositions:\n{propositions_gist}\n"
            f"----"
        )

    def to_markdown(self) -> str:
        sb: StringBuffer = StringBuffer()

        endeavour_heading = f"# Endeavour: {self.name or 'Unnamed Endeavour'}\n"
        sb.append(endeavour_heading)

        endeavour_table = (
            "| **Property**         | **Value**                         |\n"
            "|-----------------------|-----------------------------------|\n"
            f"| Name                 | {self.name}   |\n"
            f"| Description          | {self.description} |\n"
            f"| UUID                 | {self.uuid or 'Unknown UUID'}                         |\n"
            f"| Comprehensiveness    | {self.comprehensiveness}            |\n"
        )
        sb.append(endeavour_table)

        propositions_heading = (
            f"## Normative Propositions for Endeavour: {self.name or 'Unnamed Endeavour'}\n"
        )
        sb.append(propositions_heading)

        propositions_table = (
            "| **UUID** | **Proposition** | **Operator** | **Level** | **Modality** | **Modal Subscript** |\n"
            "|----------|------------------|--------------|-----------|--------------|--------------------|\n"
        )
        sb.append(propositions_table)

        for np in self.normative_propositions:
            sb.append(
                f"| {np.uuid or 'Unknown'} "
                f"| {np.proposition_value or 'Unknown'} "
                f"| {np.operator or 'Unknown'} "
                f"| {np.level or 'Unknown'} "
                f"| {np.modality or 'Unknown'} "
                f"| {np.modal_subscript or 'Unknown'} |\n"
            )

        return sb.__str__()
