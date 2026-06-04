<div style="text-align: right;">
  Jakub Kieruczenko 318669
</div>

# Modelowanie Matematyczne 26L
## Projekt 3

Niech będzie dana firma „Drewrur” produkująca drukarki 3D. Analitycy wyznaczyli przewidywane zyski
(straty) wynikające ze strategii rozwoju firmy przy różnych scenariuszach rozwoju gospodarki.

*Tabela 1 Roczny zysk firmy [mln PLN] prognozowany przez analityków w zależności od przyszłego stanu gospodarki*

<table border="0.5" cellpadding="6" cellspacing="0" style="border-collapse: collapse; text-align: center;">
  <thead>
    <tr>
      <th colspan="2" rowspan="2"></th>
      <td colspan="4">Stan gospodarki</td>
    </tr>
    <tr>
      <td>Silny wzrost</td>
      <td>Umiarkowany wzrost</td>
      <td>Umiarkowana recesja</td>
      <td>Silna recesja</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4" style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center;">przedsiębiorca</td>
      <td>Utrzymać poziom produkcji</td>
      <td>35</td>
      <td>15</td>
      <td>19</td>
      <td>2</td>
    </tr>
    <tr>
      <td>Nieco zwiększyć produkcję</td>
      <td>40</td>
      <td>23</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Znacznie zwiększyć produkcję</td>
      <td>60</td>
      <td>21</td>
      <td>2</td>
      <td>-24</td>
    </tr>
    <tr>
      <td>Zmienić profil produkcji</td>
      <td>10</td>
      <td>8</td>
      <td>20</td>
      <td>15</td>
    </tr>
  </tbody>
</table>


## 1. Decyzje podjęte przez zarząd firmy, zakładając zastosowanie operatorów eliminacji niepewności:

### a) Laplace'a
Zakładając rozkład jednostajny,

| Strategia | Obliczenie | Średnia |
|---|---|---|
| **Utrzymać** | (35+15+19+2)/4 | **17,75**  |
| Nieco zwiększyć | (40+23+2+0)/4 | 16,25 |
| Znacznie zwiększyć | (60+21+2-24)/4 | 14,75 |
| Zmienić profil | (10+8+20+15)/4 | 13,25 |

**Decyzja: Utrzymać poziom produkcji**

### b) Waldegrave’a

| Strategia | Minimum w wierszu |
|---|---|
| Utrzymać | 2 |
| Nieco zwiększyć | 0 |
| Znacznie zwiększyć | -24 |
| **Zmienić profil** | **8**  |

**Decyzja: Zmienić profil produkcji**

### c) Savage’a

Maksima kolumn (najlepszy możliwy wynik w każdym stanie):
Silny wzrost: **60**, Umiark. wzrost: **23**, Umiark. recesja: **20**, Silna recesja: **15**

Macierz żalu = max_kolumny - wartość:

| Strategia | Silny wzrost | Umiark. wzrost | Umiark. recesja | Silna recesja | Max żalu |
|---|---|---|---|---|---|
| Utrzymać | 60-35=25 | 23-15=8 | 20-19=1 | 15-2=13 | 25 |
| **Nieco zwiększyć** | 60-40=20 | 23-23=0 | 20-2=18 | 15-0=15 | **20**  |
| Znacznie zwiększyć | 60-60=0 | 23-21=2 | 20-2=18 | 15-(-24)=39 | 39 |
| Zmienić profil | 60-10=50 | 23-8=15 | 20-20=0 | 15-15=0 | 50 |

**Decyzja: Nieco zwiększyć produkcję**

### d) Hurwicza ze współczynnikiem optymizmu równym 0,9
Zakładając, że α = 1 - θ,
**α × max + (1-α) × min**

| Strategia | max | min | 0,9×max + 0,1×min |
|---|---|---|---|
| Utrzymać | 35 | 2 | 0,9×35 + 0,1×2 = 31,7 |
| Nieco zwiększyć | 40 | 0 | 0,9×40 + 0,1×0 = 36,0 |
| **Znacznie zwiększyć** | 60 | -24 | 0,9×60 + 0,1×(-24) = **51,6** |
| Zmienić profil | 20 | 8 | 0,9×20 + 0,1×8 = 18,8 |

**Decyzja: Znacznie zwiększyć produkcję**

## 2. Program symulacji

### Opis proponowanego rozkładu
Jako rozkład stanów gospodarki przyjęto rozkład dwumianowy B(3, p=0,5). Modeluje on liczbę sukcesów - korzystnych sygnałów gospodarczych w 3 niezależnych próbach, gdzie każdy sygnał z równym prawdopodobieństwem może być pozytywny lub negatywny. Wynikowe prawdopodobieństwa stanów wynoszą:

| Stan | k | P(k) |
|---|---|---|
| Silny wzrost | 3 | 0,125 |
| Umiarkowany wzrost | 2 | 0,375 |
| Umiarkowana recesja | 1 | 0,375 |
| Silna recesja | 0 | 0,125 |

Rozkład ten różni się od rozkładu zakładengo przez kryterium Laplace'a — stany umiarkowane są łącznie trzykrotnie bardziej prawdopodobne niż skrajne, co lepiej odzwierciedla rzeczywistość gospodarczą.

### Opis programu symulacyjnego
Program losuje 100 stanów gospodarki zgodnie z B(3, 0,5) przy użyciu np.random.choice. Dla każdego wylosowanego stanu odczytywany jest zysk każdej z czterech strategii z macierzy wypłat. Po 100 losowaniach obliczana jest średnia wartość zysku dla każdej strategii, a wynik porównywany z decyzjami z Zadania 1.


```
import numpy as np

profit_matrix = np.array([[35, 15, 19, 2],
                         [40, 23, 2, 0],
                         [60, 21, 2, -24],
                         [10, 8, 20, 15]])

laplace = np.mean(profit_matrix, axis=1)
print("Laplace:", laplace)

waldegrave = np.min(profit_matrix, axis=1)
print("Waldegrave:", waldegrave)

best_in_state = np.max(profit_matrix, axis=0)
regret_matrix = best_in_state - profit_matrix
savage = np.max(regret_matrix, axis=1)
print("Savage:", savage)

hurwicz_alpha = 0.9
hurwicz = hurwicz_alpha * np.max(profit_matrix, axis=1) + (1 - hurwicz_alpha) * np.min(profit_matrix, axis=1)
print("Hurwicz, α = 0.9:", hurwicz)

strategies = {
    0: "Utrzymać poziom produkcji",
    1: "Nieco zwiększyć produkcję",
    2: "Znacznie zwiększyć produkcję",
    3: "Zmienić profil produkcji"
}

np.random.seed(141)
num_simulations = 100

probabilities = [0.125, 0.375, 0.375, 0.125]
state_draws = np.random.choice(4, size=num_simulations, p=probabilities)

sim_profits = profit_matrix[:, state_draws]
mean_profits = np.mean(sim_profits, axis=1)
print("Symulacja B(3,0.5):", mean_profits)
print("Najlepsza strategia:", strategies[np.argmax(mean_profits)])

```

### Uzasadnienie wyniku
Symulacja przy rozkładzie B(3, 0,5) potwierdza wynik kryterium Laplace'a — najlepsza strategia to "Utrzymać poziom produkcji" (17,71 mln PLN). Rozkład B(3, 0,5) faworyzuje stany umiarkowane (łącznie 75% prawdopodobieństwa), a strategia utrzymania poziomu jako jedyna nie ma katastrofalnego wyniku w żadnym ze stanów (minimum = 2 mln PLN). Strategie agresywne ("Znacznie zwiększyć") tracą na wartości ze względu na duże ryzyko straty przy recesji (-24 mln PLN), nawet gdy skrajne stany są mało prawdopodobne.

## 3. Gra o sumie zerowej
Macierz wypłat w postaci ogólnej gry dwuosobowej o sumie zerowej znajduje się na górze raportu.

zysk Drewruru = -zysk gospodarki


Oznacza to, że Drewrur maksymalizuje zysk, Gospodarka minimalizuje go.
- Drewrur gra *maximin*
- Gospodarka gra *minimax*

### a) Punkty siodłowe

Punkt siodłowy istnieje, jeśli dla wyniku gry jego wartość jest mniejsza lub równa każdej wartości w jego wierszu, i większa lub równa każdej wartości w jego kolumnie.

**Minima wierszy**

| Strategia | min |
|---|---|
| Utrzymać | 2 |
| Nieco zwiększyć | 0 |
| Znacznie zwiększyć | -24 |
| **Zmienić profil** | **8** |

**Maksima kolumn**

| Stan | max |
|---|---|
| Silny wzrost | 60 |
| Umiark. wzrost | 23 |
| **Silna recesja** | **15** |
| Umiark. recesja | 20 |


8 ≠ 15 - brak punktów siodłowych.


### b) Strategia czysta Drewruru

Strategia czysta istnieje wtedy i tylko wtedy gdy istnieje punkt siodłowy. 
Ponieważ maximin ≠ minimax, strategia czysta nie istnieje.

### c) Strategia mieszana

Znalezienie strategii mieszanej polega na znalezieniu optymalnych prawdopodobieństw dla obu graczy. 
Aby uprościć grę, wyeliminuję zdominowane strategie.

Eliminacja zdominowanych strategii Gospodarki:

| Strategia | Umiarkowana recesja | Silna recesja |
|---|---|---|
| Utrzymać | 19 | 2 |
| Nieco zwiększyć | 2 | 0 |
| Znacznie zwiększyć | 2 | -24 |
| Zmienić profil | 20 | 15 |

Silna recesja ≤ Umiarkowana recesja we wszystkich wierszach.

| Strategia | Silny wzrost | Umiarkowany wzrost |
|---|---|---|
| Utrzymać | 35 | 15 |
| Nieco zwiększyć | 40 | 23 |
| Znacznie zwiększyć | 60 | 21 |
| Zmienić profil | 10 | 8 |

Umiarkowany wzrost ≤ Silny wzrost we wszystkich wierszach.

Usunięto: Umiarkowana recesja, Silny wzrost.

Eliminacja zdominowanych strategii Drewruru:

| Strategia | Umiarkowany wzrost | Silna recesja |
|---|---|---|
| Utrzymać | 15 | 2 |
| Nieco zwiększyć | 23 | 0 |
| Znacznie zwiększyć | 21 | -24 |
| Zmienić profil | 8 | 15 |

Nieco zwiększyć ≥ Znacznie zwiększyć w obu kolumnach.
Usunięto Znacznie zwiększyć.

Pozostała macierz:

| Strategia | Umiarkowany wzrost | Silna recesja |
|---|---|---|
| Utrzymać | 15 | 2 |
| Nieco zwiększyć | 23 | 0 |
| Zmienić profil | 8 | 15 |

**Rozwiązanie metodą graficzną:** 
q = prawdopodobieństwo że Gospodarka wybierze Umiarkowany wzrost:

Oczekiwany zysk Drewruru dla każdej strategii jako funkcja q:
- Utrzymać: 15q + 2(1-q) = **13q + 2**
- Nieco zwiększyć: 23q + 0(1-q) = **23q**
- Zmienić profil: 8q + 15(1-q) = **-7q + 15**

Gospodarka minimalizuje górną obwiednię tych funkcji. Minimum jest w przecięciu dwóch rosnących/malejących krzywych:

Nieco zwiększyć = Zmienić profil
23q = -7q + 15
30q = 15 
**q = 1/2**, v = 11,5

Sprawdzenie: 
przy q=1/2, Utrzymać = 2 + 6,5 = 8,5 < 11,5 

Utrzymać nie wchodzi do strategii mieszanej.

**Optymalna strategia mieszana Drewruru** 
Niech p = P(Nieco zwiększyć):

Drewrur wyrównuje zyski względem obu strategii Gospodarki:
- Umiarkowany wzrost: 23p + 8(1-p) = 15p + 8
- Silna recesja: 0p + 15(1-p) = -15p + 15

15p + 8 = -15p + 15
30p = 7
**p = 7/30**

| Strategia | Prawdopodobieństwo |
|---|---|
| Utrzymać poziom | 0 |
| Nieco zwiększyć | **7/30 ≈ 0,233** |
| Znacznie zwiększyć | 0 |
| Zmienić profil | **23/30 ≈ 0,767** |

| Stan Gospodarki | Prawdopodobieństwo |
|---|---|
| Silny wzrost | 0 |
| Umiark. wzrost | **1/2** |
| Umiark. recesja | 0 |
| Silna recesja | **1/2** |

**Wynik gry:**
v = 11,5 mln PLN

Sprawdzenie:
- Umiarkowany wzrost: (7/30)\*23 + (23/30)\*8 = 161/30 + 184/30 = 345/30 = 11,5
- Silna recesja: (7/30)\*0 + (23/30)\*15 = 345/30 = 11,5
