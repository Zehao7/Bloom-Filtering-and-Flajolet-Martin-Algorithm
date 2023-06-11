import sys, time, random, csv
from blackbox import BlackBox
# random.seed(553)

# python3 task3.py "/Users/leoli/Desktop/users.txt" 100 30 "/Users/leoli/Desktop/task3_output.csv"



if __name__ == "__main__":

    start_time = time.time()
    random.seed(553)

    input_filename = sys.argv[1]
    stream_size = int(sys.argv[2])
    num_of_asks = int(sys.argv[3])
    output_filename = sys.argv[4]


    results = []
    size = 100
    reservoir = [0] * size
    seq_num = 0
    bx = BlackBox()
    for _ in range(num_of_asks):
        stream = bx.ask(input_filename, stream_size)
        for user in stream:
            if seq_num < size:
                reservoir[seq_num] = user
            else:
                prob_keep_n = size / (seq_num+1)
                keep = random.random() < prob_keep_n
                if keep:
                    index_to_replace = random.randint(0, size - 1)
                    reservoir[index_to_replace] = user
            seq_num += 1
        results.append((seq_num, reservoir[0], reservoir[20], reservoir[40], reservoir[60], reservoir[80]))



    print("----------------- task 3 wrtie output file ------------------")
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['seqnum', '0_id', '20_id', '40_id', '60_id', '80_id'])
        for row in results:
            csvwriter.writerow(row)
    
    print("time: {0:.5f}".format(time.time() - start_time))