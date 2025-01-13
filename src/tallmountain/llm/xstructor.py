#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import re
from typing import List, Dict

from src.tallmountain.exceptions.llm_exception import LLMException
from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages
from src.tallmountain.modes.adaptive_request_mode import AdaptiveRequestMode
from src.tallmountain.util.logging_util import LoggingUtil
from lxml import etree


class XStructor:
    """Returns xml structured data from an LLM"""

    LOGGER = LoggingUtil.instance("<XStructor>")

    def do_xstructor_completion(self,
                                messages: List[Dict[str, str]],
                                xml_example: str,
                                xml_schema: str,
                                mode: AdaptiveRequestMode = AdaptiveRequestMode.balanced_mode()) -> str:
        """Returns xml structured data from an LLM"""

        if not self.is_valid_xml(xml_example, xml_schema):
            error_msg = "Invalid XML supplied for schema!"
            self.LOGGER.error(error_msg)
            raise LLMException(error_msg)

        allowed_attempts = 3
        attempts = 0

        while attempts < allowed_attempts:
            self.LOGGER.debug(f"do xstructor_completion starting attempt number {attempts}...")
            prompt = self.get_completion_prompt(
                messages=messages,
                xml_schema=xml_schema,
                xml_example=xml_example)
            llm: LLM = LLM()
            llm_messages = LLMMessages()
            llm_messages = llm_messages.build(
                "You are an expert in xml data extraction.", llm_messages.SYSTEM
            )
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            xml_response: str = llm.do_string_completion(messages=llm_messages.messages, mode=mode)
            cleaned_xml_response = self.remove_code_block_markers(xml_response)
            cleaned_xml_response = self.strip_xml_declaration(cleaned_xml_response)
            if self.is_valid_xml(xml_string=cleaned_xml_response, xml_schema=xml_schema):
                return cleaned_xml_response
            attempts += 1

        error_msg = f"Failed to generate valid XML after {allowed_attempts} attempts!"
        self.LOGGER.error(error_msg)
        raise LLMException(error_msg)

    def is_valid_xml(self, xml_string: str, xml_schema: str) -> bool:
        self.LOGGER.debug("Checking if the XML is valid")
        try:
            schema = etree.XMLSchema(etree.XML(xml_schema))
            doc = etree.XML(xml_string)
            return schema.validate(doc)
        except Exception as e:
            self.LOGGER.error(f"Exception caught: {e}")
            return False

    def get_completion_prompt(self,
                              messages: List[Dict[str, str]],
                              xml_schema: str,
                              xml_example: str) -> str:
        """Formats the completion prompt for structured output"""

        conversation_context = "\n".join(message['content'] for message in messages)
        prompt_string = f"""
        === TASK ===

        - Your task is to extract the correct information from the conversation context below.
        - You must provide the structured output in XML format using the XML schema provided.
        - You are also provided with an example of the expected output in XML.
        - You must escape any strings embedded in the XML output as follows:
            ' is replaced with &apos;
            " is replaced with &quot;
            & is replaced with &amp;
            < is replaced with &lt;
            > is replaced with &gt;
        - Your output must be valid XML.

        === START CONVERSATION CONTEXT ===
        {conversation_context}
        === END CONVERSATION CONTEXT ===

        === START XML SCHEMA ===
        {xml_schema}
        === END XML SCHEMA ===

        === START XML EXAMPLE ===
        {xml_example}
        === END XML EXAMPLE ===
        """
        return prompt_string.strip()

    def remove_code_block_markers(self, llm_response_text: str) -> str:
        cleaned_text = "\n".join(
            line for line in llm_response_text.splitlines() if not line.strip().startswith("```")
        )
        # Remove single or double quotes around the XML string
        cleaned_text = re.sub(r'^[\'"]|[\'"]$', '', cleaned_text)
        return cleaned_text

    def strip_xml_declaration(self, xml_string: str) -> str:
        import re
        cleaned_xml_string = re.sub(r'^\s*<\?xml.*?\?>\s*', '', xml_string, flags=re.DOTALL)
        return cleaned_xml_string
