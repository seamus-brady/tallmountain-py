#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.tallmountain.llm.llm_messages import LLMMessages
from src.tallmountain.llm.xstructor import XStructor

xml_schema_str = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="family">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="parent" type="xs:string" maxOccurs="2"/>
        <xs:element name="child" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="name" type="xs:string"/>
              <xs:element name="age" type="xs:integer"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""

xml_example_str = """
<family>
    <parent>John Doe</parent>
    <parent>Jane Doe</parent>
    <child>
        <name>Alice</name>
        <age>10</age>
    </child>
    <child>
        <name>Bob</name>
        <age>7</age>
    </child>
</family>
"""

xml_invalid_example_str = """
<family>
    <parent>John Doe</parent>
    <parent>Jane Doe</parent>
    <child>
        <name>Alice</name>
        <age>10</age>
        <hobbies>Basketball, Reading</hobbies>
    </child>
    <child>
        <name>Bob</name>
        <age>7</age>
    </child>
</family>
"""

not_xml_str = """
<fomolu>
    <parent>John Doe</parent>
    <parent>Jane Doe</parent>
    
    </child>
    <child>
        <name>Bob</name>
        <age>7</age>
    </child>
</family>
"""


class TextXStructor(unittest.TestCase):
    def test_is_valid_xml(self):
        xstructor = XStructor()
        self.assertTrue(xstructor.is_valid_xml(xml_example_str, xml_schema_str))

    def test_is_invalid_xml(self):
        xstructor = XStructor()
        self.assertFalse(xstructor.is_valid_xml(xml_invalid_example_str, xml_schema_str))

    def test_is_not_xml(self):
        xstructor = XStructor()
        self.assertFalse(xstructor.is_valid_xml(not_xml_str, xml_schema_str))

    def test_xstructor_completion(self):
        xstructor = XStructor()
        llm_messages = LLMMessages()
        llm_messages = llm_messages.build(
            "Mary has two children, Tom and Laura, 10 and 2 respectively.",
            llm_messages.USER)
        response = xstructor.do_xstructor_completion(
            llm_messages.messages,
            xml_example_str,
            xml_schema_str)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
