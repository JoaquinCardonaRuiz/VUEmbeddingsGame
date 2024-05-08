""" Web server for running Em8eddings game."""

from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import game

app = Flask(__name__)
game_instance = None
game_data = None

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Start page."""
    global game_instance
    global game_data

    if request.method == 'GET':
        game_instance = game.Game()
        game_data = game_instance.get_gamedata()

    return render_template('index.html', game_data=game_data)


@app.route('/play-game', methods=['GET'])
def play_game():
    """ Game page. """
    global game_instance
    global game_data
    if game_instance is None:
        return redirect(url_for('index'))

    # We start the game if it's not started.
    if game_instance.state == 'not_started':
        game_instance.start_game()

    game_data = game_instance.get_gamedata()

    # If all the neighbours are locked, the game ends
    if all([neighbour['locked'] for neighbour in game_data['neighbours']]):
        response = make_response(render_template('locked.html', game_data=game_data))
    else:
        response = make_response(render_template('index.html', game_data=game_data))

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    print(game_data['selected_word'])
    return response


@app.route('/check-answer',methods=['POST'])
def check_answer():
    """ Checks an user answer, and returns either True or False."""
    global game_instance
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        textbox_id = int(data['textboxNumber'])
        textbox_data = data['content'].lower()
        is_correct = game_instance.check_answer(textbox_id, textbox_data)
        return jsonify(is_correct=is_correct)


@app.route('/timeout', methods=['GET'])
def timeout():
    """ If the user runs out of time, end the game."""
    game_data = game_instance.get_gamedata()
    return render_template('timeout.html', game_data=game_data)

if __name__ == '__main__':
    app.run(debug=False)    