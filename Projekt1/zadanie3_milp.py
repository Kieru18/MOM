from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

# Zmienne 0-15: jak w LP
# Zmienne 16-19: binarne b1,1 b1,2 b2,1 b2,2
# b1,1=1 oznacza ze przedzial 1 S1 jest pelny (mozna uzywac przedzialu 2)
# b1,2=1 oznacza ze przedzial 2 S1 jest pelny (mozna uzywac przedzialu 3)
# b2,1, b2,2 analogicznie dla S2

n = 20
c = np.array([
    110, 114, 119, 138, 141, 143,
    -199, -103, -145, 0, -145, 0,
    -199, -103, -199, -103,
    0, 0, 0, 0
])

integrality = np.array([0]*16 + [1]*4)

lb = np.array([0.0]*16 + [0.0]*4)
ub = np.array([3393, 4495, 4112, 2424, 3691, 4885,
               np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
               np.inf, np.inf, np.inf, np.inf,
               1, 1, 1, 1])

bounds = Bounds(lb=lb, ub=ub)

rows, b_lo, b_hi = [], [], []
inf = np.inf

rows.append([1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]); b_lo.append(-inf); b_hi.append(15323)
rows.append([0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0]); b_lo.append(-inf); b_hi.append(5253)
rows.append([1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]); b_lo.append(-inf); b_hi.append(12000)
rows.append([0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]); b_lo.append(-inf); b_hi.append(11000)
rows.append([0,0,0,0,0,0,-1,0,0,0,0,0,-1,0,-1,0,0,0,0,0]); b_lo.append(-inf); b_hi.append(-3972)
rows.append([0,0,0,0,0,0,0,0,-1,0,-1,0,0,0,0,0,0,0,0,0]); b_lo.append(-inf); b_hi.append(-3972)
rows.append([0,0,0,0,0,0,0,-1,0,0,0,0,0,-1,0,-1,0,0,0,0]); b_lo.append(-inf); b_hi.append(-3972)
rows.append([-0.1,-0.1,-0.1,-0.3,-0.3,-0.3,1,1,0,0,0,0,0,0,0,0,0,0,0,0]); b_lo.append(0); b_hi.append(0)
rows.append([-0.8,-0.8,-0.8,-0.2,-0.2,-0.2,0,0,1,1,0,0,0,0,0,0,0,0,0,0]); b_lo.append(0); b_hi.append(0)
rows.append([-0.1,-0.1,-0.1,-0.5,-0.5,-0.5,0,0,0,0,1,1,0,0,0,0,0,0,0,0]); b_lo.append(0); b_hi.append(0)
rows.append([0,0,0,0,0,0,0,0,0,-0.5,0,-0.4,1,1,0,0,0,0,0,0]); b_lo.append(0); b_hi.append(0)
rows.append([0,0,0,0,0,0,0,0,0,-0.5,0,-0.6,0,0,1,1,0,0,0,0]); b_lo.append(0); b_hi.append(0)
rows.append([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-3393,0,0,0]); b_lo.append(0); b_hi.append(inf)
rows.append([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-4495,0,0,0]); b_lo.append(-inf); b_hi.append(0)
rows.append([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-4495,0,0]); b_lo.append(0); b_hi.append(inf)
rows.append([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-4112,0,0]); b_lo.append(-inf); b_hi.append(0)
rows.append([0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-2424,0]); b_lo.append(0); b_hi.append(inf)
rows.append([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,-3691,0]); b_lo.append(-inf); b_hi.append(0)
rows.append([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-3691]); b_lo.append(0); b_hi.append(inf)
rows.append([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,-4885]); b_lo.append(-inf); b_hi.append(0)

constraints = LinearConstraint(np.array(rows), b_lo, b_hi)
result = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)

names = ['s1,1','s1,2','s1,3','s2,1','s2,2','s2,3',
         'd1,1','d1,3','d2,2','d2,u','d3,2','d3,u',
         'k1,1','k1,3','k2,1','k2,3','b1,1','b1,2','b2,1','b2,2']

print(f"Status: {result.message}")
print(f"Maksymalny zysk: {-result.fun:.2f} zł/dobę")
print("\nWartosci zmiennych:")
for name, val in zip(names, result.x):
    if val > 1e-6:
        print(f"  {name} = {val:.2f}")

p1 = result.x[6] + result.x[12] + result.x[14]
p2 = result.x[8] + result.x[10]
p3 = result.x[7] + result.x[13] + result.x[15]
s1 = sum(result.x[:3])
s2 = sum(result.x[3:6])
print(f"\nProdukcja: P1={p1:.2f}, P2={p2:.2f}, P3={p3:.2f}")
print(f"Surowce:   S1={s1:.2f}, S2={s2:.2f}")
