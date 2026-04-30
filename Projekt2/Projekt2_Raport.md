<div style="text-align: right;">
  Jakub Kieruczenko 318669
</div>

# Modelowanie Matematyczne 26L
## Projekt 2

## 1. Model programowania liniowego-całkowitoliczbowego

### Zbiory

| Symbol                                 | Opis                                | Elementy                                                       |
|----------------------------------------|-------------------------------------|----------------------------------------------------------------|
| $W$                                    | zakłady wytwórcze                   | W1, W2                                                         |
| $P$                                    | produkty                            | P1, P2                                                         |
| $M$                                    | magazyny hurtowe                    | M1, M2                                                         |
| $T$                                    | typy / rozmiary magazynów           | none, small, large                                             |
| $S$                                    | punkty sprzedaży detalicznej        | S1, S2, S3                                                     |
| $\textit{MT} \subseteq M \times T$  | dopuszczalne kombinacje magazyn-typ | (M1, small), (M1, large), (M2, none), (M2, small), (M2, large) |

---

### Parametry

| Symbol | Indeksy | Opis |
|--------|---------|------|
| $production_{p,w}$ | $p \in P,\ w \in W$ | maksymalna dzienna produkcja produktu $p$ w zakładzie $w$ |
| $demand_{p,s}$ | $p \in P,\ s \in S$ | dzienne zapotrzebowanie na produkt $p$ w punkcie $s$ |
| $transport\_unit\_cost\_factory\_to\_warehouse_{w,m}$ | $w \in W,\ m \in M$ | jednostkowy koszt transportu z zakładu $w$ do magazynu $m$ [tys. zł] |
| $transport\_unit\_cost\_warehouse\_to\_shop_{m,s}$ | $m \in M,\ s \in S$ | jednostkowy koszt transportu z magazynu $m$ do punktu $s$ [tys. zł] |
| $truck\_big\_capacity$ | - | ładowność dużej ciężarówki |
| $truck\_small\_capacity$ | - | ładowność małej ciężarówki |
| $truck\_big\_maintenance\_cost$ | - | dzienny koszt utrzymania dużej ciężarówki [tys. zł] |
| $truck\_small\_maintenance\_cost$ | - | dzienny koszt utrzymania małej ciężarówki [tys. zł] |
| $warehouse\_capacity_{m,t}$ | $(m,t) \in \textit{MT}$ | pojemność magazynu $m$ typu $t$ |
| $warehouse\_cost_{m,t}$ | $(m,t) \in \textit{MT}$ | dzienny koszt operacyjny magazynu $m$ typu $t$ [tys. zł] |

**Wartości parametrów magazynowych:**

| $m\ \backslash\ t$ | none | small | large |
|--------------------|------|-------|-------|
| M1 - $warehouse\_capacity$ | -  | 58  | 153 |
| M1 - $warehouse\_cost$     | -  | 232 | 692 |
| M2 - $warehouse\_capacity$ | 0  | 97  | 156 |
| M2 - $warehouse\_cost$     | 0  | 440 | 624 |

**Produkcja:**\
$production_{p,w}$

| $p\ \backslash\ w$ | W1 | W2 |
|--|--|--|
| P1 | 52 | 67 |
| P2 | 53 | 70 |

**Zapotrzebowanie:**\
$demand_{p,s}$

| $p\ \backslash\ s$ | S1 | S2 | S3 |
|--|--|--|--|
| P1 | 34 | 31 | 22 |
| P2 | 33 | 36 | 39 |

**Jednostkowy koszt transportu z zakładu wytwórczego do magazynu hurtowego:**\
$transport\_unit\_cost\_factory\_to\_warehouse_{w,m}$ [tys. zł]

| $w\ \backslash\ m$ | M1 | M2 |
|--|--|--|
| W1 | 3 | 4 |
| W2 | 4 | 8 |

**Jednostkowy koszt transportu z magazynu hurtowego do punktu sprzedaży:**\
$transport\_unit\_cost\_warehouse\_to\_shop_{m,s}$ [tys. zł]

| $m\ \backslash\ t$ | S1 | S2 | S3 |
|--|--|--|--|
| M1 | 12 | 20 | 20 |
| M2 | 8 | 19 | 15 |


**Parametry ciężarówek:**

| Symbol | Wartość |
|--|--|
| $truck\_big\_capacity$ | 22 |
| $truck\_small\_capacity$ | 10 |
| $truck\_big\_maintenance\_cost$ | 3 tys. zł |
| $truck\_small\_maintenance\_cost$ | 0,9 tys. zł |

---

### Zmienne decyzyjne

| Symbol | Indeksy | Typ | Opis |
|--------|---------|-----|------|
| $transport\_factory\_to\_warehouse_{p,w,m}$ | $p \in P,\ w \in W,\ m \in M$ | rzeczywista $\geq 0$ | ilość produktu $p$ przewożona z zakładu $w$ do magazynu $m$ |
| $transport\_warehouse\_to\_shop_{p,m,s}$ | $p \in P,\ m \in M,\ s \in S$ | rzeczywista $\geq 0$ | ilość produktu $p$ przewożona z magazynu $m$ do punktu $s$ |
| $trucks\_big\_count_{w,m}$ | $w \in W,\ m \in M$ | całkowita $\geq 0$ | liczba dużych ciężarówek na trasie $w \to m$ |
| $trucks\_small\_count_{m,s}$ | $m \in M,\ s \in S$ | całkowita $\geq 0$ | liczba małych ciężarówek na trasie $m \to s$ |
| $warehouse\_type_{m,t}$ | $(m,t) \in \textit{MT}$ | binarna $\{0,1\}$ | 1 jeśli magazyn $m$ ma wybrany typ $t$, 0 w przeciwnym przypadku |

---

### Ograniczenia

**1) Wybór dokładnie jednego typu dla magazynu:**

$$
\sum_{t:\,(m,t)\,\in\,\textit{MT}} warehouse\_type_{m,t} = 1 \qquad \forall m \in M
$$

Każdy magazyn musi mieć przypisany dokładnie jeden typ spośród dopuszczalnych.

**(2) Moce produkcyjne zakładów:**

$$
\sum_{m \in M} transport\_factory\_to\_warehouse_{p,w,m} \leq production_{p,w} \qquad \forall p \in P,\ w \in W
$$

Łączna wysyłka produktu $p$ z zakładu $w$ nie może przekraczać jego dziennej zdolności produkcyjnej.

**3) Pokrycie zapotrzebowania:**

$$
\sum_{m \in M} transport\_warehouse\_to\_shop_{p,m,s} = demand_{p,s} \qquad \forall p \in P,\ s \in S
$$

Każdy punkt sprzedaży musi otrzymać dokładnie swoje zapotrzebowanie.

**4) Bilans przepływu w magazynach:**

$$
\sum_{w \in W} transport\_factory\_to\_warehouse_{p,w,m} = \sum_{s \in S} transport\_warehouse\_to\_shop_{p,m,s} \qquad \forall p \in P,\ m \in M
$$

Ilość produktu wchodząca do magazynu musi być równa ilości z niego wychodzącej - magazyn działa wyłącznie jako węzeł tranzytowy.

**5) Pojemność magazynów:**

$$
\sum_{\substack{w \in W \\ p \in P}} transport\_factory\_to\_warehouse_{p,w,m} \leq \sum_{t:\,(m,t)\,\in\,\textit{MT}} warehouse\_capacity_{m,t}\cdot warehouse\_type_{m,t} \qquad \forall m \in M
$$

Łączna ilość wszystkich produktów w magazynie nie przekracza pojemności wybranego typu.\
Suma po $t$ daje dokładnie jedną niezerową wartość, ponieważ tylko wybrany typ ma $warehouse\_type_{m,t} = 1$.

**6) Pojemność dużych ciężarówek (W→M):**

$$
\sum_{p \in P} transport\_factory\_to\_warehouse_{p,w,m} \leq truck\_big\_capacity\cdot trucks\_big\_count_{w,m} \qquad \forall w \in W,\ m \in M
$$

Łączny ładunek na trasie $w \to m$ nie może przekroczyć łącznej pojemności przydzielonych dużych ciężarówek.

**7) Pojemność małych ciężarówek (M→S):**

$$
\sum_{p \in P} transport\_warehouse\_to\_shop_{p,m,s} \leq truck\_small\_capacity\cdot trucks\_small\_count_{m,s} \qquad \forall m \in M,\ s \in S
$$
Łączny ładunek na trasie $m \to s$ nie może przekroczyć łącznej pojemności przydzielonych małych ciężarówek.

**8) Dziedziny zmiennych:**

$$
transport\_factory\_to\_warehouse_{p,w,m} \geq 0, \quad transport\_warehouse\_to\_shop_{p,m,s} \geq 0
$$

$$
trucks\_big\_count_{w,m} \in \mathbb{Z}_+, \quad trucks\_small\_count_{m,s} \in \mathbb{Z}_+
$$

$$
warehouse\_type_{m,t} \in \{0, 1\} \qquad \forall (m,t) \in \textit{MT}
$$

Ilości produktów są nieujemnymi liczbami rzeczywistymi.\
Liczby ciężarówek są nieujemnymi liczbami całkowitymi.\
Decyzje o typie magazynu są zmiennymi binarnymi.

---

### Funkcja celu

Minimalizacja łącznego dziennego kosztu dystrybucji:

$$
\min \quad
\underbrace{\sum_{(m,t)\, \in\, \textit{MT}} \text{warehouse\_cost}_{m,t}\cdot \text{warehouse\_type}_{m,t}}_{\text{koszty operacyjne magazynów}}
$$

$$
+\underbrace{\sum_{\substack{p \in P \\ w \in W \\ m \in M}} \text{transport\_unit\_cost\_factory\_to\_warehouse}_{w,m}\cdot \text{transport\_factory\_to\_warehouse}_{p,w,m}}_{\text{transport z zakładu do magazynu}}
$$

$$
+\underbrace{\sum_{\substack{p \in P \\ m \in M \\ s \in S}} \text{transport\_unit\_cost\_warehouse\_to\_shop}_{m,s}\cdot \text{transport\_warehouse\_to\_shop}_{p,m,s}}_{\text{transport z magazynu do punktu sprzedaży}}
$$

$$
+\underbrace{\text{truck\_big\_maintenance\_cost}\cdot\sum_{\substack{w \in W \\ m \in M}}\text{trucks\_big\_count}_{w,m}}_{\text{koszt dużych ciężarówek}}
+\underbrace{\text{truck\_small\_maintenance\_cost}\cdot\sum_{\substack{m \in M \\ s \in S}}\text{trucks\_small\_count}_{m,s}}_{\text{koszt małych ciężarówek}}
$$

## 2. Model AMPL

Implementacja modelu w języku AMPL znajduje się w załączniku.

## 3. Rozwiązanie

### Funkcja celu

Minimalny koszt: 4594.9 tys. zł = 4594900 zł

### Zmienne decyzyjne

#### Wybór typów magazynów

| Magazyn | Wybrany typ | Pojemność | Koszt dzienny |
|---------|-------------|-----------|---------------|
| M1      | small       | 58        | 232 tys. zł   |
| M2      | large       | 156       | 624 tys. zł   |

#### Transport z zakładów do magazynów

$transport\_factory\_to\_warehouse_{p,w,m}$

| $p\ \backslash\ (w,m)$ | W1→M1 | W1→M2 | W2→M1 | W2→M2 |
|------------------------|-------|-------|-------|-------|
| P1                     | 0     | 52    | 22    | 13    |
| P2                     | 0     | 53    | 36    | 19    |

#### Transport z magazynów do punktów sprzedaży

$transport\_warehouse\_to\_shop_{p,m,s}$

| $p\ \backslash\ (m,s)$ | M1→S1 | M1→S2 | M1→S3 | M2→S1 | M2→S2 | M2→S3 |
|------------------------|-------|-------|-------|-------|-------|-------|
| P1                     | 0     | 22    | 0     | 34    | 9     | 22    |
| P2                     | 0     | 36    | 0     | 33    | 0     | 39    |

#### Liczby ciężarówek

$trucks\_big\_count_{w,m}$ — duże ciężarówki (W→M):

| $w\ \backslash\ m$ | M1 | M2 |
|--------------------|----|----|
| W1                 | 0  | 5  |
| W2                 | 3  | 2  |

$trucks\_small\_count_{m,s}$ — małe ciężarówki (M→S):

| $m\ \backslash\ s$ | S1 | S2 | S3 |
|--------------------|----|----|-----|
| M1                 | 0  | 6  | 0  |
| M2                 | 7  | 1  | 7  |

#### Weryfikacja kosztów

| Składnik | Obliczenia | Koszt [tys. zł] |
|----------|-----------|-----------------|
| Magazyny | $232 + 624$ | 856,0 |
| Transport W→M | $105 \cdot 4 + 58 \cdot 4 + 32 \cdot 8$ | 908,0 |
| Transport M→S | $58 \cdot 20 + 67 \cdot 8 + 9 \cdot 19 + 61 \cdot 15$ | 2782,0 |
| Duże ciężarówki | $10 \cdot 3$ | 30,0 |
| Małe ciężarówki | $21 \cdot 0{,}9$ | 18,9 |
| **Suma** | | **4594,9** |
