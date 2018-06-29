import os
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def add_messages(username, message):
    """Add messages to the `messages` list"""
    now = datetime.now().strftime("%H:%M:%S")
    messages_dict = {"timestamp": now, "from": username, "message": message}
#Write Chat messages to the chat.txt file
    with open ("data/messages.txt", "w") as chat_list:
        chat_list.writelines("({0}) {1} - {2}\n".format(
            messages_dict["timestamp"],
            messages_dict["from"].title(),
            messages_dict["message"] ))


def get_all_messages():
    """Get al of the messages and write them into messages.txt`"""
    messages = []
    with open ("data/messages.txt", "r") as chat_messages:
        messages = chat_messages.readlines()
        return messages


@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        with open("data/users.txt", "a") as user_list:
            user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")


@app.route('/<username>')
def user(username):
    """Display chat messages"""
    messages = get_all_messages()
    return render_template("chat.html",
                            username=username, chat_messages=messages)

@app.route('/<username>/<message>')
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    add_messages(username, message)
    return redirect(username)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)