from scipy.optimize import linprog

# Zmienne (indeksy):
# 0: s1,1   1: s1,2   2: s1,3
# 3: s2,1   4: s2,2   5: s2,3
# 6: d1,1   7: d1,3
# 8: d2,2   9: d2,u
# 10: d3,2  11: d3,u
# 12: k1,1  13: k1,3
# 14: k2,1  15: k2,3

# Funkcja celu (linprog minimalizuje => negacja)
# Przychody: 199*(d1,1+k1,1+k2,1) + 145*(d2,2+d3,2) + 103*(d1,3+k1,3+k2,3)
# Koszty: 110*s1,1 + 114*s1,2 + 119*s1,3 + 138*s2,1 + 141*s2,2 + 143*s2,3
c = [
    110, 114, 119,       # s1,1 s1,2 s1,3
    138, 141, 143,       # s2,1 s2,2 s2,3
    -199, -103,          # d1,1 d1,3
    -145, 0,             # d2,2 d2,u
    -145, 0,             # d3,2 d3,u
    -199, -103,          # k1,1 k1,3
    -199, -103,          # k2,1 k2,3
]

bounds = [
    (0, 3393),   # s1,1
    (0, 4495),   # s1,2
    (0, 4112),   # s1,3
    (0, 2424),   # s2,1
    (0, 3691),   # s2,2
    (0, 4885),   # s2,3
    (0, None),   # d1,1
    (0, None),   # d1,3
    (0, None),   # d2,2
    (0, None),   # d2,u
    (0, None),   # d3,2
    (0, None),   # d3,u
    (0, None),   # k1,1
    (0, None),   # k1,3
    (0, None),   # k2,1
    (0, None),   # k2,3
]

A_ub = []
b_ub = []

# Przepustowość przygotowalni: s1 + s2 <= 15323
A_ub.append([1,1,1, 1,1,1, 0,0, 0,0, 0,0, 0,0, 0,0])
b_ub.append(15323)

# Przepustowość uwodornienia: d2,u + d3,u <= 5253
A_ub.append([0,0,0, 0,0,0, 0,0, 0,1, 0,1, 0,0, 0,0])
b_ub.append(5253)

# Dostępność S1: s1 <= 12000
A_ub.append([1,1,1, 0,0,0, 0,0, 0,0, 0,0, 0,0, 0,0])
b_ub.append(12000)

# Dostępność S2: s2 <= 11000
A_ub.append([0,0,0, 1,1,1, 0,0, 0,0, 0,0, 0,0, 0,0])
b_ub.append(11000)

# Minimalna dostawa P1: d1,1 + k1,1 + k2,1 >= 3972
A_ub.append([0,0,0, 0,0,0, -1,0, 0,0, 0,0, -1,0, -1,0])
b_ub.append(-3972)

# Minimalna dostawa P2: d2,2 + d3,2 >= 3972
A_ub.append([0,0,0, 0,0,0, 0,0, -1,0, -1,0, 0,0, 0,0])
b_ub.append(-3972)

# Minimalna dostawa P3: d1,3 + k1,3 + k2,3 >= 3972
A_ub.append([0,0,0, 0,0,0, 0,-1, 0,0, 0,0, 0,-1, 0,-1])
b_ub.append(-3972)

A_eq = []
b_eq = []

# Bilans D1: d1,1 + d1,3 = 0,1*s1 + 0,3*s2
A_eq.append([-0.1,-0.1,-0.1, -0.3,-0.3,-0.3, 1,1, 0,0, 0,0, 0,0, 0,0])
b_eq.append(0)

# Bilans D2: d2,2 + d2,u = 0,8*s1 + 0,2*s2
A_eq.append([-0.8,-0.8,-0.8, -0.2,-0.2,-0.2, 0,0, 1,1, 0,0, 0,0, 0,0])
b_eq.append(0)

# Bilans D3: d3,2 + d3,u = 0,1*s1 + 0,5*s2
A_eq.append([-0.1,-0.1,-0.1, -0.5,-0.5,-0.5, 0,0, 0,0, 1,1, 0,0, 0,0])
b_eq.append(0)

# Bilans K1: k1,1 + k1,3 = 0,5*d2,u + 0,4*d3,u
A_eq.append([0,0,0, 0,0,0, 0,0, 0,-0.5, 0,-0.4, 1,1, 0,0])
b_eq.append(0)

# Bilans K2: k2,1 + k2,3 = 0,5*d2,u + 0,6*d3,u
A_eq.append([0,0,0, 0,0,0, 0,0, 0,-0.5, 0,-0.6, 0,0, 1,1])
b_eq.append(0)

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

names = ['s1,1','s1,2','s1,3','s2,1','s2,2','s2,3',
         'd1,1','d1,3','d2,2','d2,u','d3,2','d3,u',
         'k1,1','k1,3','k2,1','k2,3']

print(f"Status: {result.message}")
print(f"Maksymalny zysk: {-result.fun:.2f} zł/dobę")
print("\nWartosci zmiennych:")
for name, val in zip(names, result.x):
    if val > 1e-6:
        print(f"  {name} = {val:.2f}")

s1 = sum(result.x[:3])
s2 = sum(result.x[3:6])
p1 = result.x[6] + result.x[12] + result.x[14]
p2 = result.x[8] + result.x[10]
p3 = result.x[7] + result.x[13] + result.x[15]
print(f"\nProdukcja: P1={p1:.2f}, P2={p2:.2f}, P3={p3:.2f}")
print(f"Surowce:   S1={s1:.2f}, S2={s2:.2f}")
