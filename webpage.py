from flask import Flask, request
import EmberBot
import os

app = Flask(__name__)#, static_url_path='')

@app.route("/")
def root():
	os.system("EmberBot.py")
	#return render_template('index.html', name=name)
	#return app.send_from_directory
	#return app.send_static_file('index.html')
	return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5005')
