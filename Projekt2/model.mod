# ------------------------------------------------------------
# Zbiory
# ------------------------------------------------------------

set W;                        # zakłady wytwórcze
set P;                        # produkty
set M;                        # magazyny hurtowe
set T;                        # typy magazynów
set S;                        # punkty sprzedaży
set MT within M cross T;      # dopuszczalne kombinacje magazyn-typ


# ------------------------------------------------------------
# Parametry
# ------------------------------------------------------------

param production {P, W} >= 0;
param demand {P, S} >= 0;

param transport_unit_cost_factory_to_warehouse {W, M} >= 0;
param transport_unit_cost_warehouse_to_shop {M, S} >= 0;

param truck_big_capacity >= 0;
param truck_small_capacity >= 0;
param truck_big_maintenance_cost >= 0;
param truck_small_maintenance_cost >= 0;

param warehouse_capacity {MT} >= 0;
param warehouse_cost {MT} >= 0;


# ------------------------------------------------------------
# Zmienne decyzyjne
# ------------------------------------------------------------

var transport_factory_to_warehouse {P, W, M} >= 0;
var transport_warehouse_to_shop {P, M, S} >= 0;
var trucks_big_count {W, M} integer >= 0;
var trucks_small_count {M, S} integer >= 0;
var warehouse_type {MT} binary;


# ------------------------------------------------------------
# Ograniczenia
# ------------------------------------------------------------

# 1) Wybór dokładnie jednego typu dla magazynu
subject to one_type_per_warehouse {m in M}:
    sum {t in T: (m,t) in MT} warehouse_type[m,t] = 1;

# 2) Moce produkcyjne zakładów
subject to production_capacity {p in P, w in W}:
    sum {m in M} transport_factory_to_warehouse[p,w,m] <= production[p,w];

# 3) Pokrycie zapotrzebowania
subject to demand_fulfillment {p in P, s in S}:
    sum {m in M} transport_warehouse_to_shop[p,m,s] = demand[p,s];

# 4) Bilans przepływu w magazynach
subject to flow_balance {p in P, m in M}:
    sum {w in W} transport_factory_to_warehouse[p,w,m]
    = sum {s in S} transport_warehouse_to_shop[p,m,s];

# 5) Pojemność magazynów
subject to warehouse_capacity_limit {m in M}:
    sum {p in P, w in W} transport_factory_to_warehouse[p,w,m]
    <= sum {t in T: (m,t) in MT} warehouse_capacity[m,t] * warehouse_type[m,t];

# 6) Pojemność dużych ciężarówek (W→M)
subject to big_truck_capacity {w in W, m in M}:
    sum {p in P} transport_factory_to_warehouse[p,w,m]
    <= truck_big_capacity * trucks_big_count[w,m];

# 7) Pojemność małych ciężarówek (M→S)
subject to small_truck_capacity {m in M, s in S}:
    sum {p in P} transport_warehouse_to_shop[p,m,s]
    <= truck_small_capacity * trucks_small_count[m,s];


# ------------------------------------------------------------
# Funkcja celu
# ------------------------------------------------------------

minimize total_cost:
    sum {(m,t) in MT}
        warehouse_cost[m,t] * warehouse_type[m,t]
    + sum {p in P, w in W, m in M}
        transport_unit_cost_factory_to_warehouse[w,m] * transport_factory_to_warehouse[p,w,m]
    + sum {p in P, m in M, s in S}
        transport_unit_cost_warehouse_to_shop[m,s] * transport_warehouse_to_shop[p,m,s]
    + truck_big_maintenance_cost *
        sum {w in W, m in M} trucks_big_count[w,m]
    + truck_small_maintenance_cost *
        sum {m in M, s in S} trucks_small_count[m,s];
