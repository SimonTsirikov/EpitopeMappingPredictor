import csv
from sys import argv


id = argv[1] 
with open(f'epitope/{id}.csv', 'r') as f:
    test = set(map(lambda x: int(x.rstrip('ABCDEFGH')), filter(lambda x: x != '', ','.join(map(lambda x: x.rstrip('\n'), f.readlines())).split(','))))

pred_pos = set()
pred_neg = set()
total = 0
with open(f'result/{id}.csv', 'r') as f:
    r = csv.DictReader(f)
    for line in r:
        total += 1
        if (line['Prediction'] == 'epitope'):
            pred_pos.add(int(line['Residue_ID']))
        else:
            pred_neg.add(int(line['Residue_ID']))
tp = len(test.intersection(pred_pos))
fp = len(pred_pos.difference(test))
fn = len(pred_neg.intersection(test))
tn = len(pred_neg.difference(test))
if (tp + fp == 0 or tp + fn == 0):
    print('ERROR', tp, fp, fn, tn)
else:
    print(tp/(tp+fp), tp/(tp+fn))
