from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from network import NetworkManager
from security import SecurityManager
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

security_manager = SecurityManager()
network_manager = NetworkManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discover', methods=['GET'])
def discover_devices():
    devices = network_manager.discover_devices()
    return jsonify(devices)

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Encrypt file
    encryption_key = security_manager.generate_session_key()
    encrypted_data = security_manager.encrypt_file(filepath, encryption_key)
    
    # Store temporarily
    session_id = security_manager.store_session(encrypted_data, encryption_key)
    
    return jsonify({
        'session_id': session_id,
        'key': encryption_key.decode('utf-8')
    })

@app.route('/download/<session_id>', methods=['GET'])
def handle_download(session_id):
    encrypted_data, key = security_manager.retrieve_session(session_id)
    if not encrypted_data:
        return jsonify({'error': 'Invalid session ID'}), 404
    
    decrypted_data = security_manager.decrypt_file(encrypted_data, key)
    return decrypted_data

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    context = ('certificates/server.crt', 'certificates/server.key')
    app.run(ssl_context=context, host='0.0.0.0', port=5000)