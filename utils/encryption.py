from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
import hashlib
import base64
import os

# AES Encryption and Decryption
def aes_encrypt(text, key_string):
    key = hashlib.sha256(key_string.encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()


def aes_decrypt(text, key_string):
    data = base64.b64decode(text)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    key = hashlib.sha256(key_string.encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode()

# RSA Encryption and Decryption
def rsa_encrypt(text):
    key = RSA.generate(2048)
    public_key = key.publickey()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher_rsa.encrypt(text.encode())
    return base64.b64encode(encrypted_data).decode()

def rsa_decrypt(text):
    key = RSA.generate(2048)
    private_key = key
    encrypted_data = base64.b64decode(text)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data.decode()

# SHA-256 Hashing
def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def aes_encrypt_file(input_file_path, encrypted_file_path, key):
    # Đọc nội dung tệp cần mã hóa
    with open(input_file_path, 'rb') as infile:
        file_data = infile.read()

    # Tạo một vector khởi tạo (IV) ngẫu nhiên
    iv = get_random_bytes(AES.block_size)

    # Khởi tạo đối tượng AES với chế độ mã hóa CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Thực hiện padding để dữ liệu có kích thước là bội số của block size
    padded_data = pad(file_data, AES.block_size)

    # Mã hóa dữ liệu
    encrypted_data = cipher.encrypt(padded_data)

    # Lưu dữ liệu mã hóa vào tệp
    with open(encrypted_file_path, 'wb') as outfile:
        # Ghi IV vào đầu tệp mã hóa, vì IV không bí mật và cần thiết để giải mã sau
        outfile.write(iv)
        # Ghi dữ liệu mã hóa vào tệp
        outfile.write(encrypted_data)

def aes_decrypt_file(encrypted_file_path, decrypted_file_path, key):
    # Đọc dữ liệu mã hóa từ tệp
    with open(encrypted_file_path, 'rb') as infile:
        # Đọc IV từ đầu tệp (IV có độ dài bằng block_size của AES)
        iv = infile.read(AES.block_size)
        
        # Đọc phần dữ liệu mã hóa còn lại
        encrypted_data = infile.read()

    # Khởi tạo đối tượng AES với chế độ CBC và IV đã đọc
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Giải mã dữ liệu
    decrypted_data = cipher.decrypt(encrypted_data)

    # Loại bỏ padding sau khi giải mã
    try:
        unpadded_data = unpad(decrypted_data, AES.block_size)
    except ValueError as e:
        raise ValueError("Dữ liệu bị lỗi hoặc không hợp lệ (có thể padding không đúng).")

    # Lưu dữ liệu giải mã vào tệp
    with open(decrypted_file_path, 'wb') as outfile:
        outfile.write(unpadded_data)

def adjust_key_length(key, length=16):
    """
    Điều chỉnh độ dài khóa đầu vào cho phù hợp với độ dài mong muốn bằng cách sử dụng padding.

    :param key: Khóa đầu vào (chuỗi hoặc bytes).
    :param length: Độ dài mong muốn của khóa (mặc định 16 byte).
    
    :return: Khóa đã điều chỉnh có độ dài phù hợp.
    """
    # Kiểm tra nếu khóa là kiểu chuỗi và chuyển thành bytes nếu cần
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Nếu khóa dài hơn độ dài yêu cầu, cắt bớt
    if len(key) > length:
        key = key[:length]
    
    # Nếu khóa ngắn hơn độ dài yêu cầu, sử dụng padding
    if len(key) < length:
        key = pad(key, length)  # Sử dụng padding từ Crypto để làm đủ độ dài
    
    return key
