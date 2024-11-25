from flask import Flask, render_template, request, jsonify
from utils.encryption import aes_encrypt, aes_decrypt, rsa_encrypt, rsa_decrypt, sha256_hash, aes_encrypt_file, adjust_key_length, aes_decrypt_file
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Crypto.Random import get_random_bytes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def send_email(subject, body, to_email, file_path, from_email, password):
    # Tạo đối tượng email kiểu MIMEMultipart để hỗ trợ nhiều phần (nội dung và tệp đính kèm)
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Chuyển body thành MIMEText và đính kèm vào email
    msg.attach(MIMEText(body, 'plain'))

    # Tạo tệp đính kèm
    attachment = MIMEBase('application', 'octet-stream')
    with open(file_path, 'rb') as file:
        attachment.set_payload(file.read())
    
    # Mã hóa tệp đính kèm bằng base64
    encoders.encode_base64(attachment)
    
    # Lấy tên tệp từ đường dẫn file_path
    filename = os.path.basename(file_path)
    
    # Thêm header cho tệp đính kèm
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    
    # Đính kèm tệp vào email
    msg.attach(attachment)

    # Gửi email qua SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Khởi động kết nối bảo mật TLS
        server.login(from_email, password)  # Đăng nhập với email và mật khẩu
        server.sendmail(from_email, to_email, msg.as_string())  # Gửi email

    print(f"Email đã được gửi đến {to_email}")

@app.route("/process_cryption", methods=["POST"])
def process_cryption():
    text = request.form.get('text')
    algorithm = request.form.get('algorithm')
    action = request.form.get('action')
    key_string = request.form.get('key_string')
    file_cryption = request.form.get('file_crypt')

    print(file_cryption)

    result = ""
    if algorithm == "AES":
        if action == "encrypt":
            result = aes_encrypt(text, key_string)
        elif action == "decrypt":
            result = aes_decrypt(text, key_string)
        elif action == "encrypt_file":
            result = aes_encrypt_file(file_cryption, key_string)
    
    elif algorithm == "RSA":
        if action == "encrypt":
            result = rsa_encrypt(text)
        elif action == "decrypt":
            result = rsa_decrypt(text)
    
    elif algorithm == "SHA-256":
        if action == "encrypt":
            result = sha256_hash(text)
        elif action == "decrypt":
            result = "SHA-256 is a hashing algorithm and cannot be decrypted."
    
    return jsonify({'result': result})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'Không có tệp được tải lên'}), 400

    file = request.files['file']
    email = request.form['email']
    key_input = request.form['key_string']
    key = adjust_key_length(key_input)
    check = request.form['check']
    print(check)

    # key = get_random_bytes(16)
    
    if file:
        # Lưu tệp gốc vào thư mục uploads
        uploads_dir = 'uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Lưu tệp gốc vào thư mục uploads
        input_file_path = os.path.join(uploads_dir, file.filename)
        encrypted_file_path = os.path.join(uploads_dir, f'encrypted_{file.filename}')
        
        # Lưu tệp gốc
        file.save(input_file_path)
        
        # Mã hóa tệp
        if check == 'encrypt':
            aes_encrypt_file(input_file_path, encrypted_file_path, key)
        elif check == 'decrypt':
            aes_decrypt_file(input_file_path, encrypted_file_path, key)
        
        # Gửi email với tệp mã hóa
        from_email = 'dinhluc79pq@gmail.com'
        password = 'blpn jvbz xajo elzy'
        subject = 'Encrypted File'
        body = 'Please find the encrypted file attached.'
        send_email(subject, body, email, encrypted_file_path, from_email, password)
        
        # Xóa tệp đã tải lên và tệp mã hóa sau khi gửi email
        os.remove(input_file_path)
        os.remove(encrypted_file_path)
        
        return jsonify({'message': 'Tệp đã được mã hóa và gửi thành công qua email!'}), 200

if __name__ == "__main__":
    app.run(debug=True)
