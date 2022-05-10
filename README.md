# EpitopeMappingPredictor

## Requirements

1. Download Molformer:
```
git clone https://github.com/smiles724/Molformer.git
```
2. Move model from Molformer to the project directory:
```
mv Molformer/model ./model
```
3. Install packages, required for Molformer (inside virtual environment, if needed):
```
pip3 install torch scikit-learn mendeleev rdkit-pypi
``` 
4. Launch code:
```
python3 main.py <antigen.pdb>
```
