from flask import Flask, send_from_directory
#import EmberBot
import os

app = Flask(__name__, static_url_path='')

@app.route('/res/<path:path>')
def send_res(path):
    return send_from_directory('static/website/public', path)

@app.route("/")
def root():
	#os.system("EmberBot.py")
	#return app.render_template('index.html', name=name)
	#return app.send_from_directory('index.html')
	return app.send_static_file('website/public/index.html')
	#return "Hello World!"

@app.route("/update/<path:user>")
def update(user):
	print user
	# makes a file called user
	open("new_signups/{}".format(user), 'a').close()
	return "made file: {}".format(user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5005')

#app.run(host='0.0.0.0', port='5005')
