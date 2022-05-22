# EpitopeMappingPredictor
# Improving Quality of Epitope Mapping by Deep Learning Methods

## Goal
The aim of the work is to create a machine learning model for solving the problem of epitope mapping with a precision quality metric that surpasses analogues.
Tasks to achieve this goal: 
* Make an overview of existing models.
* Select a data set for training.
* Design and implement a deep learning model.
* Conduct experiments, compare the results with other models. 
* Develop a prototype to use a pretrained model.

## Requirements
It is supposed to use python3 in the *nix-environment. 

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
4. Unzip model checkpoint:
```
gunzip model.ckpt.gz
```


## Usage
Launch code with:
```
python3 main.py <antigen.pdb>
```
The output would be a list of numbers, corresponding to ids of acids that are in epitope by model suggestion.

## Validation of epitope3D
1. To run validation scripts, anbase repository is required:
```
git clone https://github.com/biocad/anbase.git
```
2. Run script:
```
sh validate.sh
```

## Results
1. The review of existing models is carried out:
   
| Model     | Representation of the molecule | Input   | Method   |
|-----------|--------------------------------|---------|----------|
| PECAN     | Graph                          | Complex | CAN      |
| PInet     | Geometric                      | Complex | GAN      |
| Epitope3D | Geometric                      | Antigen | AdaBoost |

2. The [Anbase](https://github.com/biocad/anbase.git) database has been selected for training:

| Database  | Number of molecules | Type of content |
|-----------|---------------------|-----------------|
| PRISM     | 6001                | Proteins        |
| PDB       | 10714               | Proteins        |
| DBD5      | 409                 | Antigens        |
| Anbase    | 570                 | Antigens        |

3. A deep learning model for Transformer architecture (with use of [Molformer](https://arxiv.org/abs/2110.01191)) has been designed and implemented.
4. Experiments were carried out, precision and recall metrics were compared with the Epitope3D model, precision was increased by 80%

| Model     | Precision | Recall |
|-----------|-----------|--------|
| Epitope3D | 0.084     | 0.153  |
| Model     | 0.191     | 0.090  |

5. To use the pre-trained model, a prototype of the system in the python programming language has been developed.
   
## Discussion
The results obtained indicate that the information used is insufficient to solve the problem of epitope mapping. To obtain qualitatively higher values of metrics, it is necessary to use a more complex model.
