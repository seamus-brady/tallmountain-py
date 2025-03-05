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
from enum import Enum

from src.tallmountain.exceptions.normative_exception import NormativeException
from src.tallmountain.util.logging_util import LoggingUtil


class Operator(Enum):
    """
    Normative operators, read as:
     – it is required that...
     – it is ought to be that...
     – it is indifferent that...
    """

    INDIFFERENT = 1
    OUGHT = 2
    REQUIRED = 3


class Modality(Enum):
    """
    Modal operators, read as:
     – it is possible that...
     – it is impossible that...
    """

    POSSIBLE = "POSSIBLE"
    IMPOSSIBLE = "IMPOSSIBLE"


class ModalitySubscript(Enum):
    """
    Modal operator subscripts:
     – it is logically possible that...
     – it is theoretically possible that...
     – it is practically possible that...
    """

    LOGICAL = "LOGICAL"
    THEORETICAL = "THEORETICAL"
    PRACTICAL = "PRACTICAL"
    NONE = "NONE"


class Level(Enum):
    """
    Norm levels, read as:

    Norm Category       Ordinal Level    Description

    Ethical/Moral Norms 6000             Universal principles of right and wrong, justice, and human values.
    Legal Norms         5000             Codified laws enforceable by legal systems.
    Prudential Norms    4500             Focus on self-preservation and rational self-interest.
    Social/Political Norms 4000         Civic duties or expectations governing behavior in society or politics.
    Scientific/Technical Norms 3500     Standards of rigor, accuracy, and innovation in science and technology.
    Environmental Norms 3250            Principles of sustainability and ecological conservation.
    Cultural/Religious Norms 3000       Practices tied to cultural or religious identity, specific to a community.
    Community Norms     2750            Informal expectations within a local or small-group community.
    Code of Conduct     2500            Expectations within a profession, organization, or community.
    Professional/Organizational Norms 2000 Operational conduct in specific roles or workplaces.
    Economic Norms      2250            Norms regulating fairness in markets or financial systems.
    Etiquette Norms     1500            Polite behavior and socially acceptable conduct in everyday interactions.
    Game Norms          1000            Rules specific to games, sports, or competitive activities.
    Aesthetic Norms     500             Standards of beauty, taste, or artistic expression.
    """

    ETHICAL_MORAL = 6000
    LEGAL = 5000
    PRUDENTIAL = 4500
    SOCIAL_POLITICAL = 4000
    SCIENTIFIC_TECHNICAL = 3500
    ENVIRONMENTAL = 3250
    CULTURAL_RELIGIOUS_EDUCATIONAL = 3000
    COMMUNITY = 2750
    CODE_OF_CONDUCT = 2500
    PROFESSIONAL_ORGANIZATIONAL = 2000
    ECONOMIC = 2250
    ETIQUETTE = 1500
    GAME = 1000
    AESTHETIC = 500


@dataclass
class NormativeProposition:
    """
    A normative proposition.
    """

    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposition_value: str = "Unknown"
    operator: Operator = Operator.INDIFFERENT
    level: Level = Level.ETIQUETTE
    modality: Modality = Modality.IMPOSSIBLE
    modal_subscript: ModalitySubscript = ModalitySubscript.NONE

    LOGGER = LoggingUtil.instance("<NormativeProposition>")

    @staticmethod
    def from_dict(np_data: dict) -> "NormativeProposition":
        try:
            return NormativeProposition(
                uuid=np_data.get("uuid", str(uuid.uuid4())),
                proposition_value=np_data.get("proposition_value", "Unknown"),
                operator=Operator[np_data.get("operator", "INDIFFERENT")],
                level=Level[np_data.get("level", "ETIQUETTE")],
                modality=Modality[np_data.get("modality", "IMPOSSIBLE")],
                modal_subscript=ModalitySubscript[np_data.get("modality-subscript", "NONE")],
            )
        except Exception as e:
            raise NormativeException(
                f"Error creating NormativeProposition - Invalid data at missing key {e}"
            )

    def __str__(self) -> str:
        return (
            f"\nNormativeProposition:\n"
            f"  uuid: {self.uuid}\n"
            f"  proposition-value: {self.proposition_value}\n"
            f"  operator: {self.operator.name}\n"
            f"  level: {self.level.name}\n"
            f"  modality: {self.modality.name}\n"
            f"  modal-subscript: {self.modal_subscript.name}\n"
        )

    def to_markdown(self) -> str:
        return (
            "### Normative Proposition\n\n"
            f"- **UUID**: {self.uuid}\n"
            f"- **Proposition Value**: {self.proposition_value}\n"
            f"- **Operator**: {self.operator.name}\n"
            f"- **Level**: {self.level.name}\n"
            f"- **Modality**: {self.modality.name}\n"
            f"- **Modal Subscript**: {self.modal_subscript.name}\n"
        )
