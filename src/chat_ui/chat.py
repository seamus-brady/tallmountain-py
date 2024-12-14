#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import sys
from pathlib import Path

# path fix for imports ----------------------------------------------
path = Path(os.path.dirname(os.path.realpath(__file__)))
print(path.absolute().__str__())
sys.path.append(path.absolute().__str__())
sys.path.append(path.parent.absolute().__str__())
sys.path.append(path.parent.parent.absolute().__str__())
sys.path.append(path.parent.parent.parent.absolute().__str__())
# path fix for imports ----------------------------------------------

from flask import (  # noqa: E402
    Flask,
    render_template_string,
    request,
)

from src.tallmountain.util.file_path_util import FilePathUtil  # noqa: E402

app = Flask(__name__)

# Load the HTML content from the provided file
WEB_UI_TEMPLATE: str = "chat_ui.html"
WEB_ROOT: str = os.path.join(FilePathUtil.www_root_path(), WEB_UI_TEMPLATE)

with open(WEB_ROOT, "r") as file:
    chat_ui_html = file.read()


@app.route("/")
def index():
    return render_template_string(chat_ui_html)


@app.route("/chat", methods=["POST"])
def chat() -> str:
    user_message = request.form.get("message", "")
    bot_response = get_bot_response(user_message)
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


def get_bot_response(user_message: str) -> str:
    import requests

    url = "http://127.0.0.1:10000/chat"
    data = {"message": user_message}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("bot")
    else:
        return f"Error: {response.json()}"


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=10001)
