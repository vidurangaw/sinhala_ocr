from flask import Flask, render_template, json, request,redirect,session,jsonify, url_for
# from flask.ext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.wsgi import LimitedStream
import uuid
import os
import sinhala_ocr

# mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# Default setting
pageLimit = 5

class StreamConsumingMiddleware(object):

	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		stream = LimitedStream(environ['wsgi.input'],
							   int(environ['CONTENT_LENGTH'] or 0))
		environ['wsgi.input'] = stream
		app_iter = self.app(environ, start_response)
		try:
			stream.exhaust()
			for event in app_iter:
				yield event
		finally:
			if hasattr(app_iter, 'close'):
				app_iter.close()

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)


@app.route('/')
def showIndex():
	# print "ccc"
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		extension = os.path.splitext(file.filename)[1]
		f_name = file.filename

		upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
		#print upload_path
		file.save(upload_path)
		
		output = sinhala_ocr.run(upload_path)
		
		return json.dumps({'text':output[0], 'image':output[1], 'audio':output[2]})


if __name__ == "__main__":
	app.run(debug=True, port=5000)
