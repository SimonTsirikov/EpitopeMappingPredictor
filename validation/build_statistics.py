import numpy as np
import matplotlib.pyplot as plt


with open('statistics.txt', 'r') as f:
    data = list(map(lambda x: x.rstrip('\n').split(), filter(lambda x: not x.startswith('ERROR'), f.readlines())))
    precision = np.array(list(map(lambda x: float(x[0]), data)))
    recall = np.array(list(map(lambda x: float(x[1]), data)))
    
    print(np.min(precision), np.percentile(precision, 95), np.max(precision), np.average(precision), np.std(precision))
    print(np.min(recall), np.percentile(recall, 95), np.max(recall), np.average(recall), np.std(recall))

    plt.hist(precision, bins=20)
    plt.title('precision')
    plt.savefig('precision')

    plt.clf()

    plt.hist(recall, bins=20)
    plt.title('recall')
    plt.savefig('recall')
     