"""
Zadanie 1 – Problem najtańszego przepływu
Sieć kolejowa: kopalnie A,B,C -> stacje D,E -> elektrownie F,G,H

Zmienne (indeksy 0..11):
  0: f_AD   1: f_BD   2: f_BE   3: f_CD   4: f_CH
  5: f_DE   6: f_DF   7: f_DG   8: f_DH   9: f_ED
 10: f_EF  11: f_EG
"""

from scipy.optimize import linprog

# --- Funkcja celu (koszty jednostkowe) ---
# min: 3*f_AD + 6*f_BD + 2*f_BE + 4*f_CD + 5*f_CH +
#      3*f_DE + 5*f_DF + 7*f_DG + 3*f_DH + 3*f_ED +
#      2*f_EF + 4*f_EG
c = [3, 6, 2, 4, 5, 3, 5, 7, 3, 3, 2, 4]

# --- Ograniczenia przepustowości: 0 <= f_ij <= p_ij ---
bounds = [
    (0, 9),   # f_AD
    (0, 5),   # f_BD
    (0, 13),  # f_BE
    (0, 6),   # f_CD
    (0, 7),   # f_CH
    (0, 15),  # f_DE
    (0, 11),  # f_DF
    (0, 7),   # f_DG
    (0, 4),   # f_DH
    (0, 15),  # f_ED
    (0, 10),  # f_EF
    (0, 14),  # f_EG
]

# --- Ograniczenia nierównościowe (A_ub @ x <= b_ub) ---
# Ograniczenia zdolności wydobywczych
#   f_AD        <= 10   (A)
#   f_BD + f_BE <= 13   (B)
#   f_CD + f_CH <= 17   (C)

#    AD  BD  BE  CD  CH  DE  DF  DG  DH  ED  EF  EG
A_ub = [
    [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # f_AD <= 10
    [0,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # f_BD + f_BE <= 13
    [0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0],  # f_CD + f_CH <= 17
]
b_ub = [10, 13, 17]

# --- Ograniczenia równościowe (A_eq @ x == b_eq) ---
# Bilans węzła D
#   f_AD + f_BD + f_CD + f_ED - f_DE - f_DF - f_DG - f_DH = 0

# Bilans węzła E
#   f_BE + f_DE - f_ED - f_EF - f_EG = 0

# Zapotrzebowania elektrowni:
#   f_DF + f_EF = 15  (F)
#   f_DG + f_EG = 12  (G)
#   f_DH + f_CH = 8   (H)

#    AD  BD  BE  CD  CH  DE  DF  DG  DH  ED  EF  EG
A_eq = [
    [1,  1,  0,  1,  0, -1, -1, -1, -1,  1,  0,  0],  # bilans D
    [0,  0,  1,  0,  0,  1,  0,  0,  0, -1, -1, -1],  # bilans E
    [0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  0],  # F = 15
    [0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1],  # G = 12
    [0,  0,  0,  0,  1,  0,  0,  0,  1,  0,  0,  0],  # H = 8
]
b_eq = [0, 0, 15, 12, 8]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

names = ['f_AD', 'f_BD', 'f_BE', 'f_CD', 'f_CH',
         'f_DE', 'f_DF', 'f_DG', 'f_DH', 'f_ED', 'f_EF', 'f_EG']

print("=" * 45)
print(f"Status: {result.message}")
print(f"Minimalny koszt transportu: {result.fun:.2f}")
print("=" * 45)
print("\nOptymalne przepływy [tys. t / dobę]:")
for name, val in zip(names, result.x):
    if val > 1e-6:
        print(f"  {name} = {val:.4f}")

print("\nPodsumowanie planu dostaw:")
fAD,fBD,fBE,fCD,fCH,fDE,fDF,fDG,fDH,fED,fEF,fEG = result.x
print(f"  Kopalnia A wysyła: {fAD:.1f} tys. t do D")
print(f"  Kopalnia B wysyła: {fBD:.1f} do D + {fBE:.1f} do E = {fBD+fBE:.1f} tys. t")
print(f"  Kopalnia C wysyła: {fCD:.1f} do D + {fCH:.1f} do H = {fCD+fCH:.1f} tys. t")
print(f"  Elektrownia F otrzymuje: {fDF:.1f} z D + {fEF:.1f} z E = {fDF+fEF:.1f} tys. t")
print(f"  Elektrownia G otrzymuje: {fDG:.1f} z D + {fEG:.1f} z E = {fDG+fEG:.1f} tys. t")
print(f"  Elektrownia H otrzymuje: {fDH:.1f} z D + {fCH:.1f} z C = {fDH+fCH:.1f} tys. t")
