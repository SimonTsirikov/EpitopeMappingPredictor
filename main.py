import torch
import torch.nn as nn

from sys import argv

from model.tr_all import build_model
from helper import read_file, group_by_acid, fill_tree, get_nearest, prepare_transformer


if __name__ == '__main__':
    if (len(argv) != 2):
        print('Second argument should be file name.')
        exit(1)

    atoms = read_file(argv[1])
    acids = group_by_acid(atoms)
    tree = fill_tree(atoms)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    class Transformer(nn.Module):
        def __init__(self, dist, N):
            super(Transformer, self).__init__()
            self.model = build_model(8, 64, dist, N).to(device)

        def forward(self, x):
            pos = x[0]
            dist = torch.cdist(pos, pos).float().to(device)
            x = x[1]
            mask = (x != 0).unsqueeze(1).to(device)
            out = self.model(x.long(), mask, dist).to(device)
            return out
    
    model = nn.Sequential(
        Transformer([5, 25, 125], 192),
        nn.Linear(64, 64),
        nn.ReLU(),
        nn.Linear(64, 2)
    ).to(device)

    checkpoint = torch.load('model.ckpt')
    model.load_state_dict(checkpoint)
    model.eval()

    epitope = list()

    with torch.no_grad():
        for acid in acids:
            ag_nearest_indexes = get_nearest(tree, acid, 192)
            ag_nearest = [x[0][i] for i in ag_nearest_indexes]
            coordinates, types = prepare_transformer(ag_nearest)

            x = [torch.FloatTensor([coordinates]).to(device), torch.LongTensor([types]).to(device)]

            outputs = model(x)
            _, predicted = torch.max(outputs.data, 1)
            if (predicted == 1):
                epitope.append(acid.acid_id)

    print(','.join(epitope))
