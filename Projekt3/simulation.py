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
