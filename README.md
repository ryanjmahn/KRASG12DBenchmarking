# KRAS G12D Cryptic-Pocket Benchmark

Benchmarking MD-free pocket-prediction tools on the KRAS G12D Switch-II pocket (SII-P),
a clinically important cryptic pocket in pancreatic cancer.

**Status:** Phase 1 COMPLETE. Phase 2 (conformational ladder) starting.
**Target venue:** IJHSR (ECS track) primary, NHSJS fallback.

---

## What this project is (the one-paragraph version)

The discovery of a hidden "cryptic" pocket is what turned KRAS from undruggable to
druggable. The field now relies on software tools to find such pockets, but those tools
were mostly built for *visible* pockets. We test three MD-free tools on the KRAS G12D
Switch-II pocket -- a cryptic site of real clinical importance -- asking not just whether
each tool *detects* the pocket, but whether its prediction is good enough to actually
*dock a known drug* into. We measure this across a closed->open conformational series,
using the drug MRTX1133 as ground truth.

## The two research questions

- **RQ1 (novel):** As the SII-P opens, at what point does a predicted pocket become good
  enough that MRTX1133 redocks to native pose? (detection -> docking-recoverability coupling)
- **RQ2:** Which tool detects the cryptic pocket earliest/most reliably across the openness
  series?

## The three tools we benchmark (all MD-free at inference)

| Tool | Type | Role |
|------|------|------|
| fpocket | pure geometry (Voronoi/alpha-spheres, no ML) | baseline / floor |
| P2Rank | general-purpose ML | the tool everyone actually uses |
| PocketMiner | ML built specifically for cryptic pockets | the specialist |

(P2Rank+conservation was considered and dropped -- optional future arm.)

---

## The two anchor structures (Phase 1)

| PDB | State | Resolution | Notes |
|-----|-------|-----------|-------|
| 5US4 | CLOSED (apo, GDP, SII-P empty) | 1.83 A | closed end of the ladder |
| 7RPZ | OPEN (GDP + MRTX1133 bound) | 1.30 A | ANSWER KEY only -- see below |

Both are native G12D, GDP-bound, high-res X-ray -> only pocket-openness differs.

**7RPZ is the ANSWER KEY.** It is used ONLY to (a) validate docking and (b) grade the
Phase 2 ladder. It is NEVER an input to conformer generation. The ladder is built from
5US4 (closed) only. See the ANSWERKEY_DO_NOT_USE_AS_LADDER_INPUT/ folder.

## The openness metric (the x-axis of the whole study)

SII-P pocket VOLUME (measured by fpocket), identified positionally via His95.
Validated on the anchors:
- 5US4 (closed): ~245 A^3, druggability 0.001  (pocket collapsed)
- 7RPZ (open):    822 A^3, druggability 0.684  (pocket formed)
Open pocket is ~3.4x volume, ~680x druggability -> the cryptic collapse, confirmed.

## Validation gate -- PASSED

MRTX1133 redocked into 7RPZ SII-P: RMSD = 0.96 A (<= 2 A), affinity -12.7 kcal/mol.
=> docking pipeline is trustworthy. (Computed with symmetry correction on matched heavy
atoms -- see rmsd_check.py.)

---

## Repo file guide

- `5us4.pdb`, `7rpz.pdb` -- raw-ish structures
- `5US4_H.pdb`, `7RPZ_H.pdb` -- prepped: chain A, stripped, protonated (pH 7.4), aligned
- `MRTX1133_ideal.sdf` -- clean ligand w/ correct bonds (RCSB ligand 6IC)
- `MRTX1133.pdbqt` -- docking-ready ligand (Meeko)
- `7RPZ_receptor.pdbqt` -- docking receptor (Meeko)
- `MRTX1133_crystal_pose_aligned.pdb` -- answer-key ligand pose (aligned frame, 44 heavy atoms)
- `MRTX1133_redocked_v2.pdbqt` -- Vina docking output
- `docked_pose1.pdb` -- top docked pose
- `rmsd_check.py` -- symmetry-corrected RMSD script (the validation-gate measurement)
- `ANSWERKEY_DO_NOT_USE_AS_LADDER_INPUT/` -- 7RPZ, flagged so it can't leak into Phase 2
- `PROGRESS_*.md` -- session-by-session progress notes (READ THESE)

**NOT in the repo (download separately -- see SETUP):** ae-pocketminer/, p2rank_2.4.2/
(the tools themselves are gitignored; each person installs them locally).

---

## SETUP (read SETUP.md for full details)

Two conda environments + three tools. Key gotchas learned the hard way:
- **P2Rank needs Java 17** (Java 25 gives "class file major version 69" error).
- **PocketMiner** needs its optimizer patched: `tf.keras.optimizers.Adam()` ->
  `tf.keras.optimizers.legacy.Adam()`, TensorFlow 2.13 (not 2.10), remove cudatoolkit
  from environment.yml on Apple Silicon.
- **Always check your conda env** before running -- (base) vs (structprep) vs
  (aepocketminer) matters; tools live in specific envs.

---

## Phase 2 -- what's next (both people)

Build a graded closed->open conformational ladder between 5US4 and 7RPZ, WITHOUT MD:
1. NMA (ProDy) -- push 5US4 along its opening normal mode in steps
2. Backrub / side-chain repacking (PyRosetta) around switch-II for realism
3. Compute SII-P volume (fpocket) per conformer = the openness x-axis
4. Run all 3 tools on every conformer (detection metrics)
5. Dock MRTX1133 into each conformer (pipeline validated) -> docking-recoverability
6. Plot everything vs openness; the coupling threshold (RQ1) is the headline

Ladder is built from 5US4 ONLY. 7RPZ stays the answer key.

## Suggested track split (2 people)

- **Person A (ML/compute):** running the 3 tools across the ladder, detection metrics, analysis/plots
- **Person B (structure/chemistry):** conformer generation (NMA/backrub), docking across the ladder, openness-metric computation
