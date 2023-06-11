import sys, time, random, csv, math
import binascii
from blackbox import BlackBox
random.seed(553)

# python3 task2.py "/Users/leoli/Desktop/users.txt" 300 30 "/Users/leoli/Desktop/task2_output.csv"


# Define the myhashs function
def myhashs(user):
    hash_values = []
    for i in range(num_hash_functions):
        hash_values.append((a[i] * int(binascii.hexlify(user.encode("utf8")), 16) + b[i]) % sys.maxsize)
    return hash_values



if __name__ == "__main__":

    start_time = time.time()
    random.seed(553)

    input_filename = sys.argv[1]
    stream_size = int(sys.argv[2])
    num_of_asks = int(sys.argv[3])
    output_filename = sys.argv[4]


    num_hash_functions = 10
    a = [random.randint(1, sys.maxsize) for _ in range(num_hash_functions)]
    b = [random.randint(0, sys.maxsize) for _ in range(num_hash_functions)]
    num_groups = 5
    group_size = math.ceil(num_hash_functions / num_groups)


    # Function to get the position of the rightmost 0-bit
    def count_trailing_zero(num):
        return len(bin(num)) - len(bin(num).rstrip('0'))


    # Flajolet-Martin algorithm
    results = []
    bx = BlackBox()
    for ask_index in range(num_of_asks):
        stream_users = bx.ask(input_filename, stream_size)
        unique_users = len(set(stream_users))  # Ground truth

        longest_trailing_zeros = [0] * num_hash_functions
        for user in stream_users:
            hash_values = myhashs(user)
            trailing_zeros = [count_trailing_zero(x) for x in hash_values]
            longest_trailing_zeros = [max(a, b) for a, b in zip(longest_trailing_zeros, trailing_zeros)]
        #     print("trailing_zeros: ", trailing_zeros)
        #     print("longest_trailing_zeros: ", longest_trailing_zeros)
        #     print("---------------------------------------------------")
        # print("***************************************************")

        count_list = sorted([2 ** r for r in longest_trailing_zeros])
        count_list_group = [count_list[group_size * i : group_size * (i + 1)] for i in range(num_groups)]
        count_list_avg_group = list(map(lambda x: sum(x) / len(x), count_list_group))
        median_idx = int(len(count_list_avg_group) / 2)
        estimation = round(count_list_avg_group[median_idx])
        results.append((ask_index, unique_users, estimation))
    
    

    print("----------------- task 2 wrtie output file ------------------")
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Time', 'Ground Truth', 'Estimation'])
        for row in results:
            csvwriter.writerow(row)

    sum_of_estimations = 0
    sum_of_ground_truths = 0
    for i in range(num_of_asks):
        sum_of_estimations += results[i][2]
        sum_of_ground_truths += results[i][1]
    print("Estimation: ", sum_of_estimations / sum_of_ground_truths)
        

    print("time: {0:.5f}".format(time.time() - start_time))
