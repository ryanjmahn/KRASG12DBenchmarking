# SETUP GUIDE

How to get a working environment from scratch. Learned the hard way -- follow the
gotchas or you'll hit the same walls.

Machine note: developed on Apple Silicon Mac (M-series, osx-arm64). Some fixes below
are Apple-Silicon-specific.

---

## 0. Prereqs
- Install Miniconda (https://docs.conda.io/en/latest/miniconda.html)
- Clone this repo

## 1. Environment: structprep (structure prep + docking + fpocket)

```
conda create -n structprep python=3.10
conda activate structprep
conda install -c conda-forge pymol-open-source pdb2pqr fpocket rdkit scipy gemmi
pip install meeko prody spyrmsd
conda install -c conda-forge vina
conda install -c conda-forge openjdk=17     # for P2Rank -- MUST be 17
```

Verify:
```
pymol -cq -d "print('pymol ok')"
fpocket -h
vina --version
mk_prepare_ligand.py --help
java -version        # must show 17.x
```

## 2. Environment: aepocketminer (PocketMiner)

Clone the PocketMiner repo (Bowman Lab -- ae-pocketminer). Then:
```
cd ae-pocketminer
# EDIT environment.yml: delete the cudatoolkit line (no NVIDIA GPU on Mac)
conda env create -f environment.yml
conda activate aepocketminer
pip install "tensorflow==2.13.0"   # pinned 2.10 doesn't exist on osx-arm64
pip install pyyaml                 # missing dependency
```

**REQUIRED CODE FIX** in `src/xtal_predict.py`:
```
# change this line:
opt = tf.keras.optimizers.Adam()
# to:
opt = tf.keras.optimizers.legacy.Adam()
```
(Without this, the checkpoint won't load on TF 2.13.)

Run PocketMiner (regular, not attention variant):
- put input PDBs in an `inputs/` folder
- make a config (my_config.yaml):
```
nn_path: /ABSOLUTE/PATH/TO/ae-pocketminer/models/pocketminer
input_pdb_directory: inputs
output_directory: results/pocketminer
use_attention: False
debug: False
```
- run: `python src/xtal_predict.py my_config.yaml`
- output: results/pocketminer/<name>-preds.npy  (per-residue cryptic probability)

## 3. Tool: P2Rank (default)

Download release from https://github.com/rdk/p2rank/releases (v2.4.2 used here).
```
tar -xzf p2rank_2.4.2.tar.gz
cd p2rank_2.4.2
# make sure Java 17 is active (conda activate structprep)
./prank predict -f ../7RPZ_H.pdb
```
GOTCHA: needs Java 17. Newer Java gives "Unsupported class file major version 69".
Output: test_output/predict_<name>/<name>_predictions.csv
The SII-P is identified by which predicted pocket's residues include His95 + switch-II
(58-72). Note: P2Rank often ranks the nucleotide site above the SII-P.

## 4. Tool: fpocket (already in structprep)
```
fpocket -f 7RPZ_H.pdb
# creates 7RPZ_H_out/ with *_info.txt listing each pocket's Volume + Druggability
```
Identify the SII-P = the pocket whose alpha spheres (resn STP) cluster near His95.

---

## The environment trap (READ THIS)
conda environments are per-terminal-session. A new terminal starts in (base).
ALWAYS check your prompt shows the right env before running:
- structprep: pymol, fpocket, vina, meeko, rdkit, java, pdb2pqr
- aepocketminer: pocketminer, tensorflow
If you get "command not found" or "No module named X", you're probably in the wrong env.

## PyMOL vs terminal
- PyMOL commands (load, align, get_distance, iterate) -> the PyMOL window's command line
- shell commands (conda, fpocket, vina, python) -> the terminal (or VS Code terminal)
Typing one in the other does nothing / errors.

## RMSD measurement gotcha (validation gate)
Comparing a docked ligand to a crystal ligand: strip ALL hydrogens from both
(Chem.RemoveAllHs), match heavy-atom graphs, and use rdMolAlign.GetBestRMS
(symmetry-aware). Naive PyMOL rms_cur mispairs atoms and inflates the number
(we saw fake 5-6 A; true value was 0.96 A). See rmsd_check.py.
