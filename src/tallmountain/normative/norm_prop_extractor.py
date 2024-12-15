#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages

from typing import List, Optional
from pydantic import BaseModel


class NormativePropositionType(BaseModel):
    """Normative Proposition Type."""
    proposition_value: str


class ImpliedPropositions(BaseModel):
    """Implied Propositions."""
    NormativeProposition: Optional[List[NormativePropositionType]] = None


class NormativeAnalysisResults(BaseModel):
    """Normative Analysis Results."""
    input_statement: str
    implied_propositions: Optional[ImpliedPropositions] = None


class NormPropExtractor:
    """Extracts normative propositions from a given input statement."""

    @staticmethod
    def do_extraction(user_query: str) -> NormativeAnalysisResults:
        llm: LLM = LLM()
        llm_messages = LLMMessages()
        llm_messages = llm_messages.build(
            "You are an expert in language analysis.", llm_messages.SYSTEM
        )

        prompt: str = f"""
        === INSTRUCTIONS ===

        - Analyze the following text for underlying beliefs, assumptions, and implied norms about the behavior,
          capabilities, and ethical boundaries of agents (whether AI or otherwise).
        - Identify any explicit or implicit normative statements or directives about how such agents should act or
          what they should prioritize.
        - Reformulate these statements as if the author were explicitly declaring them as their beliefs or expectations.
        - Avoid providing any analysis or commentary on the ethics, validity, or implications of these statements —
          simply extract and rewrite them as a list of propositions the author might state.
        

        === START USER REQUEST ===
        {user_query}
        === END USER REQUEST ===
        
        
        """
        llm_messages = llm_messages.build(prompt, llm_messages.USER)
        response: NormativeAnalysisResults = llm.do_instructor(
            messages=llm_messages.messages,
            response_model=NormativeAnalysisResults)
        return response
