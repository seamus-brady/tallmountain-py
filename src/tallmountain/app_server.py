# Copyright 2023 Seamus Brady
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

import queue  # noqa: E402
import threading  # noqa: E402

from flask import Flask, request  # noqa: E402
from flask_restful import Api, Resource  # noqa: E402

from src.tallmountain.llm.llm_facade import LLM  # noqa: E402
from src.tallmountain.llm.llm_messages import LLMMessages  # noqa: E402

app = Flask(__name__)
api = Api(app)

# Thread-safe queue for communication
message_queue: queue.Queue = queue.Queue()
response_queue: queue.Queue = queue.Queue()


# Background task to process messages
def background_task() -> None:
    while True:
        try:
            # Retrieve a message from the queue
            user_message = message_queue.get(timeout=5)
            llm: LLM = LLM()
            llm_messages = LLMMessages()
            llm_messages = llm_messages.build(user_message, llm_messages.USER)
            bot_response: str = llm.do_string_completion(messages=llm_messages.messages)

            # Put the processed response into the response queue
            response_queue.put(bot_response)
        except queue.Empty:
            # No message received; continue waiting
            pass


# Chat resource
class Chat(Resource):
    def post(self):
        user_message = request.json.get("message", "")
        if not user_message:
            return {"error": "Message content is required"}, 400

        # Send user message to the background thread
        message_queue.put(user_message)

        # Wait for a response from the background thread
        try:
            bot_response = response_queue.get(timeout=60)
            return {"bot": bot_response}, 200
        except queue.Empty:
            return {"error": "No response from background task"}, 504


# Add resources to the API
api.add_resource(Chat, "/chat")

if __name__ == "__main__":
    # Start the background thread
    bg_thread = threading.Thread(target=background_task, daemon=True)
    bg_thread.start()

    # Run the Flask server
    app.run(debug=True, threaded=True, port=10000)  # nosec
