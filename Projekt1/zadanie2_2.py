"""
Zadanie 2.2 – Problem najtańszego skojarzenia (przydziału)
"""

from scipy.optimize import linprog

# Koszty t[i][j] – projekt i, zespół j (None = brak kompetencji)
t = [
    [None, 12,   10,   12,   18,   None],  # projekt 1
    [None, 15,   11,   13,   None, 14  ],  # projekt 2
    [10,   15,   None, None, 13,   None],  # projekt 3
    [12,   None, None, 20,   None, 17  ],  # projekt 4
    [15,   14,   12,   None, 11,   None],  # projekt 5
    [10,   None, 18,   16,   None, 12  ],  # projekt 6
]
#   A,     B,    C,    D,    E,    F

# Funkcja celu: minimalizuj sumę kosztów
c = []
for i in range(6):
    for j in range(6):
        c.append(t[i][j] if t[i][j] is not None else 0)

# Bounds: brak kompetencji -> (0,0), reszta -> (0,1)
bounds = []
for i in range(6):
    for j in range(6):
        bounds.append((0, 1) if t[i][j] is not None else (0, 0))

A_eq, b_eq = [], []

# Każdy projekt dostaje dokładnie jeden zespół
for i in range(6):
    row = [0]*36
    for j in range(6):
        row[i*6 + j] = 1
    A_eq.append(row)
    b_eq.append(1)

# Każdy zespół dostaje co najwyżej jeden projekt
A_ub, b_ub = [], []
for j in range(6):
    row = [0]*36
    for i in range(6):
        row[i*6 + j] = 1
    A_ub.append(row)
    b_ub.append(1)

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

teams = ['A', 'B', 'C', 'D', 'E', 'F']
print(f"Minimalny koszt: {result.fun:.0f}")
for i in range(6):
    for j in range(6):
        if result.x[i*6 + j] > 0.5:
            print(f"  Projekt {i+1} -> Zespół {teams[j]} (koszt {t[i][j]})")
