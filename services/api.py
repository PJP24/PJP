from flask import Flask, jsonify, request, Response
import hypercorn
from hypercorn.config import Config
from orchestrator.orchestrator import Orchestrator

app = Flask(__name__)

@app.route('/orchestrate', methods=['POST'])
async def orchestrate() -> Response:
    data = request.json
    if data is None:
        return jsonify({'error': 'Request body must be JSON'}), 400

    user_id = data.get('user_id')
    if user_id is None or user_id == '':
        return jsonify({'error': 'user_id is required'}), 400

    orchestrator = Orchestrator()
    try:
        result = await orchestrator.execute(user_id)
        if 'error' in result:
            return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:5001"]
    hypercorn.run(app, config)
