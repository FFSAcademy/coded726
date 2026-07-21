#THIS SOFTWARE IS PROTECTED BY COPYRIGHT. UNAUTHORIZED USE, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED AND MAY RESULT IN LEGAL ACTION.


from flask import Flask, render_template, jsonify, request
import mimetypes

from chat_bot import ChatAgent


mimetypes.add_type('application/wasm', '.wasm')


app = Flask(__name__)


# Create the student's AI assistant
agent = ChatAgent()


# Students customize their chatbot here
agent.set_primary_directive(
    "You are an A.I. assistant that wants to help users."
)

agent.add_context(
    "You are a friendly robot."
)

# Optional: add a knowledge file
# Make sure chat_bot_knowledge.txt exists
agent.add_context_document(
    "chat_bot_knowledge.txt"
)



@app.route('/chat', methods=['POST'])
def chat():

    print("CHAT TRIGGERED")

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "error": "Missing 'message' in request"
        }), 400


    response = agent.chat(
        data["message"]
    )


    return jsonify({
        "response": response
    })



@app.route('/')
def index():

    return render_template(
        "index.html"
    )



@app.route('/robot_sim')
def robot_sim():

    return render_template(
        "robot_sim.html"
    )



if __name__ == '__main__':

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )




