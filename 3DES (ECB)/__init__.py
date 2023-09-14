import time
import psutil
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def triple_des_encrypt(key, plaintext):
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def record_start_time():
    return time.time()

def record_end_time(start_time):
    return time.time() - start_time

def get_average_cpu_usage(num_samples=10, interval=0.1):
    total_cpu_percent = sum(psutil.cpu_percent(interval=interval) for _ in range(num_samples))
    return total_cpu_percent / num_samples

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
    
    # 3DES encryption
    key = b'sixteenbytekey!x'
    plaintext = b'Hello, world!'
    ciphertext = triple_des_encrypt(key, plaintext)
    print(f"Ciphertext: {ciphertext}")

    # Record the end time
    execution_time = record_end_time(start_time)
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