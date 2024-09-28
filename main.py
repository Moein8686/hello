from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')
    return jsonify({'status': 'success', 'message': f'Received message from {name}: {message}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
