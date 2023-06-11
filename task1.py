import sys, time, random, csv, math
import binascii
from blackbox import BlackBox
random.seed(553)

# python3 task1.py "/Users/leoli/Desktop/users.txt" 100 30 "/Users/leoli/Desktop/task1_output.csv"


# Define Bloom Filter class
class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.bit_array = [0] * m

    def insert(self, user_id):
        hash_values = myhashs(user_id)
        for value in hash_values:
            self.bit_array[value % self.m] = 1

    def contains(self, user_id):
        hash_values = myhashs(user_id)
        for value in hash_values:
            if self.bit_array[value % self.m] == 0:
                return False
        return True


def myhashs(user):
    hash_values = []
    for i in range(k):
        hash_value = (a[i] * int(binascii.hexlify(user.encode('utf8')), 16) + b[i]) % m
        hash_values.append(hash_value)
    return hash_values



if __name__ == "__main__":

    start_time = time.time()
    random.seed(553)

    input_filename = sys.argv[1]
    stream_size = int(sys.argv[2])
    num_of_asks = int(sys.argv[3])
    output_filename = sys.argv[4]


    # myhashs function
    # m is the size of the bit array
    # n is the number of expected elements to insert into the filter
    # k is the number of hash functions
    # k = (m/n) * ln(2)
    m = 69997
    n = stream_size * num_of_asks
    k = math.ceil((m / n) * math.log(2))
    a = random.sample(range(1, sys.maxsize - 1), k)
    b = random.sample(range(0, sys.maxsize - 1), k)


    # Create a Bloom Filter instance
    bloom_filter = BloomFilter(69997, k)

    bx = BlackBox()
    previous_users = set()
    fpr_results = []
    true_positives = 0
    false_positives = 0
    true_negatives = 0

    for i in range(num_of_asks):
        # Read the data stream (a list of user_id strings)
        stream_users = bx.ask(input_filename, stream_size)
        
        for user_id in stream_users:
            if bloom_filter.contains(user_id):
                if user_id in previous_users:
                    true_positives += 1
                else:
                    false_positives += 1
            else:
                true_negatives += 1
                bloom_filter.insert(user_id)
                previous_users.add(user_id)

        # Calculate FPR = FP / (FP + TN)
        fpr = false_positives / (false_positives + true_negatives)
        fpr_results.append((i, fpr))
        # fpr_results.append((i, false_positives, true_positives, true_negatives, fpr))
    

    print("----------------- task 1 wrtie output file ------------------")
    with open(output_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Time", "FPR"])
        # csv_writer.writerow(["Time", "FP", "TP", "TN", "FPR"])
        for row in fpr_results:
            csv_writer.writerow(row)
        

    print("time: {0:.5f}".format(time.time() - start_time))
