from collections import defaultdict
from typing import List, Tuple

from scipy.spatial import cKDTree


class Atom():
    def __init__(self, atom_id: int, acid_id: str, x: float, y: float, z: float, number: int) -> None:
        self.atom_id = atom_id
        self.acid_id = acid_id
        self.x = x
        self.y = y
        self.z = z
        self.number = number


class Acid():
    def __init__(self, acid_id: str, atoms: List[Atom]) -> None:
        self.acid_id = acid_id
        self.atoms = atoms


numbering = {'H': 0, 'C': 1, 'N': 2, 'O': 3, 'F': 4, 'P': 5, 'S': 6, 'K': 7}


def parse_atom(line: str) -> List[str]:
    """Parse one string according to .pdb format description"""
    tokens = list()
    tokens.append(line[4:11].lstrip())
    tokens.append(line[22:27].strip())
    tokens.append(line[30:38].lstrip())
    tokens.append(line[38:46].lstrip())
    tokens.append(line[46:54].lstrip())
    tokens.append(line[77])
    return tokens


def read_file(name) -> List[Atom]:
    """Extract data from .pdb file"""
    ag_atoms = list()
    with open(name) as f:
        for line in f:
            if line.startswith('ATOM'):
                if (len(line) > 77):
                    c = parse_atom(line)
                    ag_atoms.append(Atom(int(c[0]), c[1], float(c[2]), float(c[3]), float(c[4]), numbering[c[5]]))

    return ag_atoms


def group_by_acid(molecule: List[Atom]) -> List[Acid]:
    """Group molecules from the same acid into container"""
    acids = defaultdict(list)
    for atom in molecule:
        acids[atom.acid_id].append(atom)
    
    return [Acid(acid_id, atoms) for acid_id, atoms in acids.items()]


def fill_tree(molecule: List[Atom], leafsize) -> cKDTree:
    """Build structure to get quicker access to data"""
    return cKDTree([[atom.x, atom.y, atom.z] for atom in molecule], leafsize)


def get_nearest(tree: cKDTree, acid: Acid, size: int = 64) -> List[int]:
    """Extract the area of uniform size around acid"""
    _, indexes = tree.query([[atom.x, atom.y, atom.z] for atom in acid.atoms], size)
    return indexes[0]


def prepare_transformer(atoms: List[Atom]) -> Tuple[List[Tuple[float, float, float]], List[int]]:
    """Arrange the data in the input format of Molformer"""
    positions = list()
    numbers   = list()
    for atom in atoms:
        positions.append([atom.x, atom.y, atom.z])
        numbers.append(atom.number)
    return positions, numbers
