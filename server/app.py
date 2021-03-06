from extractKeywords import getKeywords
from flask import Flask, request, jsonify
from random import randint
import json

try:
	getKeywords("")
except Exception as e:
	import nltk
	nltk.download('punkt')
	nltk.download('averaged_perceptron_tagger')

class Search:
	def __init__(self):
		with open('emojis.json', 'r') as f:
			self.emojis = json.loads(f.read())
		try:
			for k,v in self.emojis.iteritems():
				self.emojis[k]['keywords'].append(k)
		except:
			for k,v in self.emojis.items():
				self.emojis[k]['keywords'].append(k)

	def query(self, word=''):
		matches = []
		for v in self.emojis.values():
			for kw in v.get('keywords', None):
				word = " ".join(word.split('_'))
				if word.lower() in kw and (withinone(kw, word, 1) or len(kw) == len(word)):
					a = v.get('char', None)
					if a:
						matches.append(a)

		return matches

def withinone(a, b, c):
	return len(a)-c == len(b) or len(a)+c == len(b)

emoji_search = Search()

app = Flask(__name__)

app.debug = False

@app.route('/')
def index():
	return jsonify({})

@app.route('/text_to_emoji')
def text_to_emoji():
	query_string = request.args
	text = query_string.get('query', '')
	emojis = []
	if "stars" in text:
		text = text.replace("stars", "star")
	if "shirts" in text:
		text = text.replace("shirts", "shirt")
	kwds = getKeywords(text)
	for wrd in kwds:
		emoj = emoji_search.query(wrd)
		[emojis.append(e) for e in emoj]
	return jsonify({'success': True, 'emojis': emojis})


@app.after_request
def add_ua_compat(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
	return response

if __name__ == '__main__':
	app.run(port=5000)