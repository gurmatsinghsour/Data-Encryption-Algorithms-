import psutil
import time

# Record the start time
start_time = time.time()



class Twofish():

    def __init__(self, text, key):
        self.text = text
        self.key = key

    key_arr = []
    mds = [['00000001', '11101111', '1011011', '1011011'], ['1011011', '11101111', '11101111', '00000001'],
           ['11101111', '1011011', '00000001', '11101111'], ['11101111', '00000001', '11101111', '1011011']]
    q0 = [
        ['1000', '0001', '0111', '1101', '0110', '1111', '0011', '0010', '0000', '1011', '0101', '1001', '1110', '1100',
         '1010', '0100'],
        ['1110', '1100', '1011', '1000', '0001', '0010', '0011', '0101', '1111', '0100', '1010', '0110', '0111', '0000',
         '1001', '1101'],
        ['1011', '1010', '0101', '1110', '0110', '1101', '1001', '0000', '1100', '1000', '1111', '0011', '0010', '0100',
         '0111', '0001'],
        ['1101', '0111', '1111', '0100', '0001', '0010', '0110', '1110', '1001', '1011', '0011', '0000', '1000', '0101',
         '1100', '1010']]
    q1 = [
        ['0010', '1000', '1011' '1101', '1111', '0111', '0110', '1110', '0011', '0001', '1001', '0100', '0000', '1010',
         '1100', '0101'],
        ['0001', '1110', '0010', '1011', '0100', '1100', '0011', '0111', '0110', '1101', '1010', '0101', '1111', '1001',
         '0000', '1000'],
        ['0100', '1100', '0111', '0101', '0001', '0110', '1001', '1010', '0000', '1110', '1101', '1000', '0010', '1011',
         '0011', '1111'],
        ['1011', '1001', '0101', '0001', '1010', '0011', '1101', '1110', '0110', '0100', '0111', '1111', '0010', '0000',
         '1000', '1010']
    ]

    rs = [['1', '10100100', '1010101', '10000111', '1011010', '1011000', '11011011', '10011110'],
          ['10100100', '1010110', '10000010', '11110011', '11110', '11000110', '1101000', '11100101'],
          ['01', '10100001', '11111100', '11000001', '1000111', '10101110', '111101', '11001'],
          ['10100100', '1010101', '10000111', '1011010', '1011000', '11011011', '10011110', '11'], ]

    def bin_to_dec(self, digit):
        new_digit = 0
        for i in range(len(digit)):
            new_digit += int(digit[i]) * (2 ** (len(digit) - i - 1))
        return new_digit

    def dec_to_bin(self, digit, bit):
        digit = str(bin(int(digit)).replace("0b", ""))
        if bit != None:
            while len(digit) != bit:
                digit = '0' + digit
        return digit

    def sum32(self, digit, key):
        digit, key = self.bin_to_dec(digit), self.bin_to_dec(key)
        result = digit + key
        result = result % (2 ** 32)
        return self.dec_to_bin(result, 32)

    def key_shedule(self):
        key = [self.key[i:i + 32] for i in range(0, len(self.key), 32)]
        for i in range(20):
            self.h(i)
        self.skey()
        return key

    def skey(self):
        key = [self.key[i: i + 8] for i in range(0, len(self.key), 8)]
        new_key = []
        temp = 0
        for i in range(4):
            for j in range(8):
                temp += self.bin_to_dec(key[j]) * self.bin_to_dec(self.rs[i][j])
            new_key.append(temp)
        new_key[0] = self.dec_to_bin(new_key[0] % 2 ** 8, 16)
        new_key[1] = self.dec_to_bin(new_key[1] % 2 ** 6, 16)
        new_key[2] = self.dec_to_bin(new_key[2] % 2 ** 3, 16)
        new_key[3] = self.dec_to_bin(new_key[3] % 2 ** 2, 16)
        self.key_arr.append(new_key[0] + new_key[1])
        self.key_arr.append(new_key[2] + new_key[3])
        return None

    def whitening(self, index):
        text = [self.text[i:i + 32] for i in range(0, 128, 32)]
        for i in range(len(text)):
            text[i] = self.xor(text[i], self.key_arr[i * index])
        return text

    def xor(self, digit1, digit2):
        new_digit = ''
        for i in range(len(digit1)):
            new_digit += str((int(digit1[i]) + int(digit2[i])) % 2)
        return new_digit

    def rol(self, key, bit):
        new_key = ''
        for i in range(len(key)):
            new_key += key[(i + bit) % len(key)]
        return new_key

    def ror(self, key, bit):
        new_key = ''
        for i in range(len(key)):
            new_key += key[(i - bit) % len(key)]
        return new_key

    def round(self, text, round_number):
        temp = text.copy()
        temp[0], temp[1] = self.f(temp[0], temp[1], round_number)
        temp[0] = self.xor(temp[2], temp[0])
        temp[0] = self.ror(temp[0], 1)
        temp[1] = self.rol(temp[1], 1)
        temp[1] = self.xor(temp[1], temp[3])
        text = [temp[0], temp[1], text[0], text[1]]
        return text

    def f(self, R0, R1, round_number):
        keys = [self.key_arr[40], self.key_arr[41]]
        T0 = self.g(R0, keys)
        T1 = self.g(self.rol(R1, 1), keys)
        T0 = self.sum32(T0, T1)
        T1 = self.sum32(T0, T1)
        T0 = self.sum32(T0, self.key_arr[2 * round_number + 8])
        T1 = self.sum32(T0, self.key_arr[2 * round_number + 9])
        return T0, T1

    def h(self, round_number):
        keys1 = [self.key[64:96], self.key[0:32]]
        keys2 = [self.key[96:], self.key[32:64]]
        T0 = self.g(self.dec_to_bin(2 * round_number, 32), keys1)
        T1 = self.g(self.dec_to_bin(2 * round_number, 32), keys2)
        T1 = self.rol(T1, 8)
        T0 = self.sum32(T0, T1)
        T1 = self.sum32(T0, T1)
        T1 = self.rol(T1, 9)
        self.key_arr.append(T0)
        self.key_arr.append(T1)
        return T0, T1

    def MDS(self, X):
        new_X = []
        temp = 0
        for i in range(4):
            for j in range(4):
                temp += self.bin_to_dec(X[j]) * self.bin_to_dec(self.mds[i][j])
            new_X.append(temp)
        new_X[0] = self.dec_to_bin(new_X[0] % 2 ** 8, 8)
        new_X[1] = self.dec_to_bin(new_X[1] % 2 ** 6, 8)
        new_X[2] = self.dec_to_bin(new_X[2] % 2 ** 5, 8)
        new_X[3] = self.dec_to_bin(new_X[3] % 2 ** 3, 8)
        return new_X[0] + new_X[1] + new_X[2] + new_X[3]

    def perutration(self, text, index, number):
        new_text = ''
        for i in range(len(text)):
            if index == 0:
                new_text += self.q0[number][self.bin_to_dec(text[i])]
            elif index == 1:
                new_text += self.q1[number][self.bin_to_dec(text[i])]
        return text

    def q(self, text, index):
        x1 = text[0:4]
        y1 = text[4:8]
        x2 = str(x1)
        x3 = str(x1)
        y2 = str(y1)
        x1 = self.xor(x1, y2)
        y1 = self.ror(y1, 1)
        x3 = self.dec_to_bin((8 * self.bin_to_dec(x3)) % 16, 4)
        y1 = self.xor(self.xor(y1, x3), x2)
        x1 = self.perutration(x1, index, 0)
        y1 = self.perutration(y1, index, 1)
        x2 = str(x1)
        x3 = str(x1)
        y2 = str(y1)
        x1 = self.xor(x1, y2)
        y1 = self.ror(y1, 1)
        x3 = self.dec_to_bin((8 * self.bin_to_dec(x3)) % 16, 4)
        y1 = self.xor(self.xor(y1, x3), x2)
        x1 = self.perutration(x1, index, 2)
        y1 = self.perutration(y1, index, 3)
        return x1 + y1

    def g(self, X, skey):
        X = [X[i: i + 8] for i in range(0, len(X), 8)]
        X = self.q(X[0], 0) + self.q(X[1], 1) + self.q(X[2], 0) + self.q(X[3], 1)
        X = self.xor(X, skey[0])
        X = [X[i: i + 8] for i in range(0, len(X), 8)]
        X = self.q(X[0], 0) + self.q(X[1], 0) + self.q(X[2], 1) + self.q(X[3], 1)
        X = self.xor(X, skey[1])
        X = [X[i: i + 8] for i in range(0, len(X), 8)]
        X = self.q(X[0], 1) + self.q(X[1], 0) + self.q(X[2], 1) + self.q(X[3], 0)
        X = [X[i: i + 8] for i in range(0, len(X), 8)]
        X = self.MDS(X)
        return X

    def encrypt(self):
        self.key_shedule()
        text = self.whitening(1)
        for i in range(16):
            text = self.round(text, i)
        text = self.whitening(2)
        return text


text_1 = Twofish(
    '00000000011001000110011001100010011100110111001001100111011000100110100101101100011010100111001101110010011010110110111001100010',
    '01110100011100100111010001100010011000100110110101101100011010110111001101110010011011110011101101101001011011000110101001110011')
print('THIS_IS_A_HARD_AND_BIG_PLAIN_TEXT_FOR_ENCRYPTION', text_1.encrypt())



# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution Time: {execution_time:.4f} seconds")

########## CPU Usage ##########


def get_average_cpu_usage(num_samples=10, interval=0.1):
    total_cpu_percent = 0

    for _ in range(num_samples):
        cpu_percent = psutil.cpu_percent(interval=interval)
        total_cpu_percent += cpu_percent

    average_cpu_percent = total_cpu_percent / num_samples
    return average_cpu_percent

average_usage = get_average_cpu_usage()
print(f"Average CPU Usage: {average_usage}%")

########## Memory Usage ##########


def get_average_memory_usage(num_samples=10, interval=0.1):
    total_used_memory = 0

    for _ in range(num_samples):
        memory_info = psutil.virtual_memory()
        total_used_memory += memory_info.used
        time.sleep(interval)

    average_used_memory = total_used_memory / num_samples
    return average_used_memory

average_usage = get_average_memory_usage()
print(f"Average Used Memory: {average_usage} bytes")

########## Bandwidth Usage ##########


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

monitor_bandwidth_usage()
