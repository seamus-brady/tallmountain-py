import json
from typing import List

from src.tallmountain.exceptions.normative_exception import NormativeException
from src.tallmountain.normative.entities.endeavour import Endeavour
from src.tallmountain.normative.normative_proposition import NormativeProposition
from src.tallmountain.util.config_util import ConfigUtil
from src.tallmountain.util.logging_util import LoggingUtil
from src.tallmountain.util.string_buffer_util import StringBuffer


class NormativeAgent:
    """
    A class for managing the system's endeavours
    """

    LOGGER = LoggingUtil.instance("<NormativeAgent>")

    def __init__(self) -> None:
        self.LOGGER.info("Initializing NormativeAgent")
        self.highest_endeavour: Endeavour = self.load_highest_endeavour()
        self.system_endeavours: List[Endeavour] = self.load_system_endeavours()

    def load_highest_endeavour(self) -> Endeavour:
        self.LOGGER.info("Loading highest entities")
        try:
            norm_props: List[NormativeProposition] = []
            json_data = ConfigUtil.highest_endeavour_json()
            endeavours = json.loads(json_data)
            for np_dict in endeavours["endeavours"][0]["normative_propositions"]:
                norm_prop: NormativeProposition = NormativeProposition.from_dict(np_dict)
                norm_props.append(norm_prop)
            return Endeavour(
                name=endeavours["endeavours"][0]["name"],
                description=endeavours["endeavours"][0]["description"],
                normative_propositions=norm_props,
            )
        except Exception as e:
            self.LOGGER.error(f"Failed to load highest endeavours: {str(e)}")
            raise NormativeException(f"Failed to load highest endeavours: {str(e)}")

    def load_system_endeavours(self) -> List[Endeavour]:
        self.LOGGER.info("Loading system endeavours")
        try:
            endeavours_list: List[Endeavour] = []
            json_data = ConfigUtil.system_endeavours_json()
            endeavours = json.loads(json_data)
            for endeavour_data in endeavours["endeavours"]:
                norm_props: List[NormativeProposition] = [
                    NormativeProposition.from_dict(np_dict)
                    for np_dict in endeavour_data["normative_propositions"]
                ]
                endeavour = Endeavour(
                    name=endeavour_data["name"],
                    description=endeavour_data["description"],
                    normative_propositions=norm_props,
                )
                endeavours_list.append(endeavour)
            return endeavours_list
        except Exception as e:
            self.LOGGER.error(f"Failed to load system endeavours: {str(e)}")
            raise NormativeException(f"Failed to load system endeavours: {str(e)}")

    def system_endeavours_to_md(self) -> str:
        self.LOGGER.info("Converting system endeavours to markdown")
        """Return the system endeavours as a markdown doc."""
        sb: StringBuffer = StringBuffer()
        for endeavour in self.system_endeavours:
            sb.append(endeavour.to_markdown(), end="\n")
            sb.append("----", end="\n\n")
        return sb.__str__()

    def highest_endeavour_to_md(self) -> str:
        self.LOGGER.info("Converting highest entities to markdown")
        """Return the highest entities as a markdown doc."""
        return self.highest_endeavour.to_markdown()
