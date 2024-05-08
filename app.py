from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import game

app = Flask(__name__)
game_instance = None
game_data = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global game_instance
    global game_data

    if request.method == 'GET':
        game_instance = game.Game()
        game_data = game_instance.get_gamedata()

    return render_template('index.html', game_data=game_data)


@app.route('/play-game', methods=['GET'])
def play_game():
    global game_instance
    global game_data
    if game_instance is None:
        return redirect(url_for('index'))

    if game_instance.state == 'not_started':
        game_instance.start_game()

    game_data = game_instance.get_gamedata()
    response = make_response(render_template('index.html', game_data=game_data))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    print(game_data['selected_word'])
    return response


@app.route('/check-answer',methods=['POST'])
def check_answer():
    global game_instance
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        textbox_id = int(data['textboxNumber'])
        textbox_data = data['content'].lower()
        is_correct = game_instance.check_answer(textbox_id, textbox_data)
        return jsonify(is_correct=is_correct)


if __name__ == '__main__':
    app.run(debug=True)    

if __name__ == '__main__':
    app.run(debug=True)