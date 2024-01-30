import time
import psutil
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(public_key, plaintext):
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return ciphertext

def rsa_decrypt(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
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

    print(f"Bytes Sent: {bytes_sent} bytes")
    print(f"Bytes Received: {bytes_received} bytes")

if __name__ == "__main__":
    # Generate RSA key pair
    private_key, public_key = generate_rsa_key_pair()

    # Record the start time
    start_time = record_start_time()

    # Usage
    plaintext = b'THIS_IS_A_HARD_AND_BIG_PLAIN_TEXT_FOR_ENCRYPTION'
    ciphertext = rsa_encrypt(public_key, plaintext)
    print("Ciphertext:", ciphertext.hex())

    decrypted_plaintext = rsa_decrypt(private_key, ciphertext)
    print("Decrypted plaintext:", decrypted_plaintext.decode())

    # Record the end time
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
    monitor_bandwidth_usage()
