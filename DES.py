from flask import Flask, render_template, request, send_file
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Đảm bảo mật khẩu hợp lệ: 8 ký tự
def get_valid_key(password):
    key = password.encode('utf-8')
    if len(key) < 8:
        key += b' ' * (8 - len(key))  # padding nếu quá ngắn
    return key[:8]  # lấy đúng 8 byte

def des_encrypt(data, key):
    cipher = DES.new(key, DES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), DES.block_size))
    return cipher.iv + ct_bytes

def des_decrypt(enc_data, key):
    iv = enc_data[:DES.block_size]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(enc_data[DES.block_size:]), DES.block_size)
    return pt.decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    file = request.files['file']
    password = request.form['password']
    if file and password:
        key = get_valid_key(password)
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            file_data = f.read()

        encrypted_data = des_encrypt(file_data, key)
        output_filename = f'encrypted_{filename}'
        output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)

        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        return send_file(output_path, as_attachment=True)
    return "Yêu cầu không hợp lệ"

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    file = request.files['file']
    password = request.form['password']
    if file and password:
        key = get_valid_key(password)
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            enc_data = f.read()

        try:
            decrypted_data = des_decrypt(enc_data, key)
        except Exception:
            return "Giải mã thất bại! Kiểm tra mật khẩu hoặc file."

        output_filename = f'decrypted_{filename}'
        output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(decrypted_data)

        return send_file(output_path, as_attachment=True)
    return "Yêu cầu không hợp lệ"

if __name__ == '__main__':
    app.run(debug=True)

