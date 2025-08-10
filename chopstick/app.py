from flask import Flask, request, render_template, jsonify, session
from Game import Game
from AI import AI
import uuid
import json

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = 'j4cob1sS3XY'
games = {}

@app.route('/')
def index():
    if 'game_id' not in session:
        game_id = str(uuid.uuid4())
        session['game_id'] = game_id
        games[game_id] = Game()
        games[game_id].start_game()

    game_id = session['game_id']

    if len(games) > 100:
        oldest_ids = list(games.keys())[:len(games)-100]
        for old_id in oldest_ids:
            if old_id != game_id:
                del games[old_id]

    game = games.get(game_id)
    if not game:
        games[game_id] = Game()
        games[game_id].start_game()
        game = games[game_id]

    game_state = game.get_game_state()
    valid_moves = game.valid_moves() if game_state['winner'] is None else []

    data = {
        'title': 'chopped',
        'game_id': game_id,
        'game_state': game_state,
        'valid_moves': valid_moves,
        'current_player': game_state['current_player'],
        'winner': game_state['winner'],
        'players': game_state['players']
    }

    return render_template('index-new.html', **data)

@app.route('/game', methods=['GET', 'POST'])
def game():
    game_id = session.get('game_id')

    if not game_id or game_id not in games:
        if request.method == 'GET' and request.headers.get('Content-Type') == 'application/json':
            return jsonify({'error': 'no active game found'}), 404
        else:
            return index()

    game_obj = games[game_id]

    if request.method == 'POST':
        action = request.form.get('action') or request.json.get('action') if request.is_json else None

        if action == 'move':
            if request.is_json:
                move_data = request.json.get('move')
            else:
                move_type = request.form.get('move_type')
                if move_type == 'attack':
                    move_data = {
                        'type': 'attack',
                        'from_hand': request.form.get('from_hand'),
                        'to_player': int(request.form.get('to_player')),
                        'to_hand': request.form.get('to_hand')
                    }
                elif move_type == 'split':
                    move_data = {
                        'type': 'split',
                        'left_to_right': request.form.get('left_to_right') == 'true',
                        'amount': int(request.form.get('amount'))
                    }
                else:
                    move_data = None

            if move_data:
                success = game_obj.make_move(move_data)
                if request.is_json:
                    game_state = game_obj.get_game_state()
                    valid_moves = game_obj.valid_moves() if game_state['winner'] is None else []
                    return jsonify({
                        'success': success,
                        'game_state': game_state,
                        'valid_moves': valid_moves,
                        'current_player': game_state['current_player'],
                        'winner': game_state['winner'],
                        'players': game_state['players']
                    })
            else:
                if request.is_json:
                    return jsonify({'error': 'invalid move data'}), 400

        elif action == 'reset':
            game_obj.start_game()
            if request.is_json:
                game_state = game_obj.get_game_state()
                valid_moves = game_obj.valid_moves()
                return jsonify({
                    'success': True,
                    'game_state': game_state,
                    'valid_moves': valid_moves,
                    'current_player': game_state['current_player'],
                    'winner': game_state['winner'],
                    'players': game_state['players']
                })

        elif action == 'get_moves':
            if request.is_json:
                return jsonify({
                    'valid_moves': game_obj.valid_moves(),
                    'current_player': game_obj.current_player
                })

        elif action == 'get_hint':
            if request.is_json:
                ai = AI()
                analysis = ai.analyze_position(game_obj)
                return jsonify({
                    'success': True,
                    'analysis': analysis,
                    'best_move': analysis['best_move'],
                    'description': analysis['description'],
                    'evaluation': analysis['evaluation'],
                    'winning': analysis['winning'],
                    'explanation': analysis['explanation']
                })

    game_state = game_obj.get_game_state()
    valid_moves = game_obj.valid_moves() if game_state['winner'] is None else []

    response_data = {
        'game_id': game_id,
        'game_state': game_state,
        'valid_moves': valid_moves,
        'current_player': game_state['current_player'],
        'winner': game_state['winner'],
        'players': game_state['players'],
        'move_count': len(valid_moves)
    }

    if request.headers.get('Content-Type') == 'application/json' or request.is_json:
        return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
