#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import threading
import queue
import time

app = Flask(__name__)
api = Api(app)

# Thread-safe queue for communication
message_queue = queue.Queue()
response_queue = queue.Queue()


# Background task to process messages
def background_task():
    while True:
        try:
            # Retrieve a message from the queue
            message = message_queue.get(timeout=1)  # Waits 1 second if no message is available
            print(f"Background thread received: {message}")

            # Simulate processing
            time.sleep(2)
            processed_response = f"Processed: {message}"

            # Put the processed response into the response queue
            response_queue.put(processed_response)
        except queue.Empty:
            # No message received; continue waiting
            pass


# Chat resource
class Chat(Resource):
    def post(self):
        user_message = request.json.get('message', '')
        if not user_message:
            return {'error': 'Message content is required'}, 400

        # Send user message to the background thread
        message_queue.put(user_message)

        # Wait for a response from the background thread
        try:
            bot_response = response_queue.get(timeout=5)  # Wait for up to 5 seconds
            return {'bot': bot_response}, 200
        except queue.Empty:
            return {'error': 'No response from background task'}, 504


# Add resources to the API
api.add_resource(Chat, '/chat')

if __name__ == '__main__':
    # Start the background thread
    bg_thread = threading.Thread(target=background_task, daemon=True)
    bg_thread.start()

    # Run the Flask server
    app.run(debug=True, threaded=True, port=10000)
