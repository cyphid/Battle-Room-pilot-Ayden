from flask import Flask, jsonify, request
from game import Game

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({'apiversion': 1})


@app.route('/start', methods=['POST'])
def start():
  request_data = request.json
  global game_state
  game_state = Game(request_data['id'], request_data['ruleset'],
                    request_data['map'], request_data['timeout'],
                    request_data['source'])
  return "Game created"


@app.route('/move')
def move():
  return jsonify({'move': 'up'})


@app.route('/end')
def end():
  return 'Game ended.'


if __name__ == '__main__':
  app.run(host='0.0.0.0')