from flask import Flask, request, send_file, render_template
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import io

app = Flask(__name__)

def prepare_key(user_key: str, length: int = 32) -> bytes:
    """Chuyển khóa người dùng sang định dạng 32 byte (AES-256)."""
    return user_key.encode('utf-8').ljust(length, b'0')[:length]

@app.route('/')
def index():
    return render_template('C:\BÀI THỨ 4\BÀI TẬP HTML.HTML')

@app.route('POSTPOST', methods=['POST'])
def process():
    file = request.files['file']
    key = request.form['key']
    mode = request.form['mode']  # encrypt / decrypt
    key_bytes = prepare_key(key)

    data = file.read()

    if mode == 'encrypt':
        iv = get_random_bytes(16)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        encrypted_data = iv + cipher.encrypt(pad(data, AES.block_size))
        filename = 'encrypted_' + file.filename
        result = encrypted_data
    elif mode == 'decrypt':
        iv = data[:16]
        encrypted = data[16:]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        try:
            decrypted_data = unpad(cipher.decrypt(encrypted), AES.block_size)
        except ValueError:
            return "Sai khóa hoặc dữ liệu không hợp lệ", 400
        filename = 'decrypted_' + file.filename
        result = decrypted_data
    else:
        return "Sai chế độ xử lý", 400

    return send_file(
        io.BytesIO(result),
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True)
