import time
import psutil
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_blowfish(key, plaintext):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    padded_plaintext = pad(plaintext, Blowfish.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def decrypt_blowfish(key, ciphertext):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, Blowfish.block_size)
    return plaintext

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
    
    # Blowfish encryption
    key = get_random_bytes(16)  # 128-bit key for Blowfish
    plaintext = b'Hello, world!'
    
    ciphertext = encrypt_blowfish(key, plaintext)
    print("Ciphertext:", ciphertext.hex())
    
    decrypted_plaintext = decrypt_blowfish(key, ciphertext)
    print("Decrypted plaintext:", decrypted_plaintext.decode())

    # Record the end time
    end_time = record_end_time(start_time)

    # Calculate and print the execution time
    execution_time = end_time - start_time
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
