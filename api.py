from flask import Flask, jsonify, request
from orchestrator.orchestrator import Orchestrator

app = Flask(__name__)

@app.route('/fetch_user_data', methods=['POST'])
async def fetch_user_data():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    orchestrator = Orchestrator()
    result = await orchestrator.execute(user_id)

    if result:
        return jsonify(result)
    return jsonify({'error': 'User not found'}), 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
