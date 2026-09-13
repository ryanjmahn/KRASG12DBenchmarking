"""
FIGURE — Real-structure anchor comparison (the cleanest, no-NMA result).
All 3 tools on the 2 REAL experimental structures: 5US4 (closed), 7RPZ (open).
Hardcoded from the anchor_comparison.py output (real experimental data).
Grouped bars: recall on closed vs open, per tool.
"""
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Data from anchor_comparison.py (real experimental structures)
# recall values
tools=['fpocket','P2Rank','PocketMiner']
closed_recall=[0.20, 0.15, 0.35]   # 5US4
open_recall  =[0.44, 0.80, 0.40]   # 7RPZ
closed_mcc   =[0.24, 0.04, 0.07]
open_mcc     =[0.54, 0.61, 0.12]

x=np.arange(len(tools)); w=0.35

# --- Panel A: recall closed vs open ---
fig, (axA, axB) = plt.subplots(1, 2, figsize=(11,5))

axA.bar(x-w/2, closed_recall, w, label='Closed (5US4)', color='#B0B0B0')
axA.bar(x+w/2, open_recall,  w, label='Open (7RPZ)',   color='#2E75B6')
axA.set_xticks(x); axA.set_xticklabels(tools)
axA.set_ylabel('SII-P recall'); axA.set_title('A. Recall on real structures')
axA.legend(); axA.grid(alpha=0.3, axis='y')
axA.set_ylim(0,0.9)
# annotate the P2Rank open bar
axA.text(1+w/2, 0.82, '0.80', ha='center', fontsize=9, weight='bold', color='#2E75B6')

# --- Panel B: MCC closed vs open ---
axB.bar(x-w/2, closed_mcc, w, label='Closed (5US4)', color='#B0B0B0')
axB.bar(x+w/2, open_mcc,  w, label='Open (7RPZ)',   color='#C00000')
axB.set_xticks(x); axB.set_xticklabels(tools)
axB.set_ylabel('MCC'); axB.set_title('B. Prediction quality on real structures')
axB.legend(); axB.grid(alpha=0.3, axis='y')
axB.set_ylim(0,0.9)

plt.suptitle('Tool performance on real experimental structures (no NMA)', y=1.02, fontsize=12)
plt.tight_layout()
plt.savefig('fig_anchor_comparison.png', dpi=200, bbox_inches='tight')
plt.close()
print("Saved fig_anchor_comparison.png")
print("\nKey: On real OPEN 7RPZ, P2Rank recall 0.80 (localizes best);")
print("PocketMiner recall 0.40 but MCC only 0.12 (over-spreads even on real structure).")