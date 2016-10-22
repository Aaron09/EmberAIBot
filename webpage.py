from flask import Flask
app = Flask(__name__)
import EmberBot
import os

@app.route("/")
def hello():
	os.system("EmberBot.py")
	return app.send_static_file('index.html')
	return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5005')
