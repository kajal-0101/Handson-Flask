from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path

app = Flask(__name__)
app.secret_key = ''

@app.route('/')
def index():
	return render_template('index.html', codes=session.keys())
	# return render_template('index.html', wish="Have a good day!")

# code variable is equal to request.args
# args is a dictionary for different parameters that could be passed in as parameters
@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
	if request.method == 'POST':
		urls = {}
		if os.path.exists('urls.json'):
			with open('urls.json') as urls_file:
				urls = json.load(urls_file)

		if request.form['code'] in urls.keys():
			flash("The short name has already been taken. Please use another name")
			return redirect(url_for('index'))
		
		urls[request.form['code']] = {'url': request.form['url']}
		
		with open('urls.json', 'w') as url_file:
			json.dump(urls, url_file)
			session[request.form['code']]=True
		return render_template('your_url.html', code=request.form['code'])
	else:
		return redirect(url_for('index'))

@app.route('/<string:code>')
def redirect_to_url(code):
	if os.path.exists('urls.json'):
		with open('urls.json') as urls_file:
			urls = json.load(urls_file)
			if code in urls.keys():
				if 'url' in urls[code].keys():
					return redirect(urls[code]['url'])
	return abort(404)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
	return jsonify(list(session.keys()))


# @app.route('/about')
# def about():
# 	return '<h1>This is a URL shortener</h1>'