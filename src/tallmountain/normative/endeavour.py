#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import uuid
from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from typing import List

from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.uuid_util import UUIDUtil


class Comprehensiveness(Enum):
    """
    Comprehensiveness Determines Escalation: When two endeavours conflict, and one is more comprehensive than the
    other, the norms of the more comprehensive endeavour are elevated to a higher normative level.
    """

    HIGH = "HIGH"
    DEFAULT = "DEFAULT"
    LOW = "LOW"


@dataclass
class Endeavour:
    """
    An endeavour of an agent. Manages a set of NormProps.
    """

    name: str
    description: str
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    comprehensiveness: Comprehensiveness = Comprehensiveness.DEFAULT
    normative_propositions: List[NormativeProposition] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        uuid: str = None,
        comprehensiveness: str = None,
        normative_propositions: List[NormativeProposition] = None,
    ):
        return cls(
            name=name,
            description=description,
            uuid=uuid or str(UUIDUtil.get()),
            comprehensiveness=Comprehensiveness.DEFAULT,
            normative_propositions=normative_propositions or [],
        )

    def __str__(self) -> str:
        propositions_gist = "\n".join(
            [np.__str__() for np in self.normative_propositions]
        )
        return (
            f"----\n"
            f"Endeavour name: {self.name}\n"
            f"description: {self.description}\n"
            f"comprehensiveness: {self.comprehensiveness}\n"
            f"normative_propositions:\n{propositions_gist}\n"
            f"----"
        )

    def to_markdown(self) -> str:
        endeavour_heading = f"# Endeavour: {self.name or 'Unnamed Endeavour'}\n"
        endeavour_table = (
            "| **Property**         | **Value**                         |\n"
            "|-----------------------|-----------------------------------|\n"
            f"| Name                 | {self.name}   |\n"
            f"| Description          | {self.description} |\n"
            f"| UUID                 | {self.uuid or 'Unknown UUID'}                         |\n"
            f"| Comprehensiveness    | {self.comprehensiveness}            |\n"
        )

        propositions_heading = f"## Normative Propositions for Endeavour: {self.name or 'Unnamed Endeavour'}\n"
        propositions_table = (
            "| **Proposition** | **Operator** | **Level** | **Modality** | **Modal Subscript** |\n"
            "|------------------|--------------|-----------|--------------|--------------------|\n"
        )

        for np in self.normative_propositions:
            propositions_table += (
                f"| {np.proposition_value or ''} "
                f"| {np.operator or ''} "
                f"| {np.level or ''} "
                f"| {np.modality or ''} "
                f"| {np.modal_subscript or ''} |\n"
            )

        return (
            endeavour_heading
            + "\n"
            + endeavour_table
            + "\n\n"
            + propositions_heading
            + "\n"
            + propositions_table
        )
