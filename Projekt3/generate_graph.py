import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

q = np.linspace(0, 1, 300)
L1 = 2 + 13*q
L2 = 23*q
L3 = 15 - 7*q
env = np.maximum(np.maximum(L1, L2), L3)

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('white')

ax.plot(q, L1, color='#378ADD', linewidth=1.5, label='Utrzymać poziom')
ax.plot(q, L2, color='#D4537E', linewidth=1.5, label='Nieco zwiększyć')
ax.plot(q, L3, color='#1D9E75', linewidth=1.5, label='Zmienić profil')
ax.plot(q, env, color='#444444', linewidth=2.5, linestyle='--', label='obwiednia górna')

ax.axvline(x=0.5, color='#bbbbbb', linewidth=0.8, linestyle=':')
ax.axhline(y=11.5, color='#bbbbbb', linewidth=0.8, linestyle=':')

ax.scatter([0.5], [11.5], color='#222222', s=60, zorder=5)
ax.annotate('q = 0,5, v = 11,5', xy=(0.5, 11.5), xytext=(0.54, 10.2),
            fontsize=10, color='#222222', fontweight='bold')

ax.set_xlabel('q - P(Umiarkowany wzrost)', fontsize=11)
ax.set_ylabel('v [mln PLN]', fontsize=11)
ax.set_xlim(0, 1)
ax.set_ylim(-2, 26)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0', '0,25', '0,5', '0,75', '1,0'])
ax.grid(True, linewidth=0.4, color='#e0e0e0')
ax.legend(loc='upper right', fontsize=10, framealpha=1)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('./mixed_strategy_graph.png', dpi=300, bbox_inches='tight')
