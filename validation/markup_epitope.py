from math import sqrt
from sys import argv

class Atom:
    def __init__(self, residue, x, y, z) -> None:
        self.residue = residue
        self.x = x
        self.y = y
        self.z = z

def distance(lhs: Atom, rhs: Atom):
    return sqrt((lhs.x - rhs.x) ** 2 + (lhs.y - rhs.y) ** 2 + (lhs.z - rhs.z) ** 2)

if __name__ == '__main__':
    id = argv[1]
    ags = list()
    abs = list()
    epitope = set()
    with open(f'ag_source/{id}_ag_u.pdb', 'r') as f:
        for line in f.readlines():
            if line.startswith('ATOM'):
                ags.append(Atom(line[22:27].strip(), float(line[27:38]), float(line[38:46]), float(line[46:54])))
    with open(f'ab_source/{id}_ab_u.pdb', 'r') as f:
        for line in f.readlines():
            if line.startswith('ATOM'):
                v = line.split()
                abs.append(Atom(line[22:27].strip(), float(line[27:38]), float(line[38:46]), float(line[46:54])))
    for ag in ags:
        if (ag.residue not in epitope):
            for ab in abs:
                if (distance(ag, ab) <= 4):
                    epitope.add(ag.residue)
                    break
    ordered = list(epitope)
    ordered.sort()
    print(','.join(ordered))
