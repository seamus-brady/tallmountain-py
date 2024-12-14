#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from flask import Flask, request, render_template_string, jsonify
import time

from src.tallmountain.llm.llm_facade import LLM
from src.tallmountain.llm.llm_messages import LLMMessages

app = Flask(__name__)

# Load the HTML content from the provided file
with open('/home/seamus/GitHub/pbi/tallmountain-prototype/src/chat_ui/www/chat_ui.html', 'r') as file:
    chat_ui_html = file.read()

@app.route('/')
def index():
    return render_template_string(chat_ui_html)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message', '')
    llm: LLM = LLM()
    llm_messages = LLMMessages()
    llm_messages = llm_messages.build(user_message, llm_messages.USER)
    bot_response: str = llm.do_string_completion(messages=llm_messages.messages)
    response_html = f"""
    <div class="message-container user-message-container">
        <img src="https://img.icons8.com/color/48/000000/user.png" class="icon" alt="User Icon">
        <span>{user_message}</span>
    </div>
    <div class="message-container bot-message-container">
        <img src="https://img.icons8.com/ios-filled/50/4a90e2/mountain.png" class="icon" alt="Bot Icon">
        <span class="bot-message markdown">{bot_response}</span>
    </div>
    """
    return response_html

if __name__ == '__main__':
    app.run(debug=True)
