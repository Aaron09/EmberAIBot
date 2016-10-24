from flask import Flask
import EmberBot
import os

app = Flask(__name__, static_url_path='index.html')

@app.route("/")
def hello():
	os.system("EmberBot.py")
	return render_template('hello.html', name=name)
	#return app.send_from_directory
	#return app.send_static_file('index.html')
	#return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5005')
