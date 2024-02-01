import time
import psutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def encrypt_blowfish(key, plaintext):
    cipher = Cipher(algorithms.Blowfish(key), mode=modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.Blowfish.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext

def decrypt_blowfish(key, ciphertext):
    cipher = Cipher(algorithms.Blowfish(key), mode=modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.Blowfish.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    # plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def record_start_time():
    return time.time()

def record_end_time(start_time):
    return time.time() - start_time

def get_average_cpu_usage(num_samples=10, interval=0.1):
    total_cpu_percent = sum(psutil.cpu_percent(interval=interval) for _ in range(num_samples))
    average_cpu_percent = total_cpu_percent / num_samples
    return min(100, average_cpu_percent)

def get_average_memory_usage(num_samples=10, interval=0.1):
    total_used_memory = sum(psutil.virtual_memory().used for _ in range(num_samples))
    return total_used_memory / num_samples

def monitor_bandwidth_usage():
    before_network_stats = psutil.net_io_counters()

    # Perform encryption/decryption operations here
    # For example, simulate by sleeping for a brief interval
    time.sleep(5)  # Simulate 5 seconds of activity

    after_network_stats = psutil.net_io_counters()

    bytes_sent = after_network_stats.bytes_sent - before_network_stats.bytes_sent
    bytes_received = after_network_stats.bytes_recv - before_network_stats.bytes_recv

    return bytes_sent, bytes_received

if __name__ == "__main__":
    # Record the start time
    start_time = record_start_time()

    # KEY 1

    # key = b'sixteenbytekey!!'
    # plaintext = b'TCETMUMBAI_GD'

    # Key 2

    # key = b's!xt33n|3y|3k3y@'
    # plaintext = b'THIS_IS_A_HARD_AND_BIG_PLAIN_TEXT_FOR_ENCRYPTION'

    # Key 3 

    # key = b's!xt33n|3y|3k3y@' 
    # plaintext = b'A@J#!K@J#BB$J@!J#BKJJB@#!K'

    ciphertext = encrypt_blowfish(key, plaintext)
    print("Ciphertext:", ciphertext.hex())

    decrypted_plaintext = decrypt_blowfish(key, ciphertext)
    print("Decrypted plaintext:", decrypted_plaintext.decode())

    # Record the end time after the encryption and decryption operations
    end_time = record_end_time(start_time)

    # Calculate and print the execution time
    execution_time = end_time
    print(f"Execution Time: {execution_time:.4f} seconds")

    # CPU Usage
    average_cpu_usage = get_average_cpu_usage()
    print(f"Average CPU Usage: {average_cpu_usage}%")

    # Memory Usage
    average_memory_usage = get_average_memory_usage()
    print(f"Average Used Memory: {average_memory_usage} bytes")

    # Bandwidth Usage
    bytes_sent, bytes_received = monitor_bandwidth_usage()
    print(f"Bytes Sent: {bytes_sent} bytes")
    print(f"Bytes Received: {bytes_received} bytes")
