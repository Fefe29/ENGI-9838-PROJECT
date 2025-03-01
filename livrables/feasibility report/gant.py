import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Définition des tâches avec leurs dates
tasks = [
    ("Definition & Feasibility Study", "2024-01-25", "2024-02-03"),
    ("System Design", "2024-02-03", "2024-02-15"),
    ("Data collection", "2024-02-15", "2024-03-01"),
    ("Phase 1", "2024-03-01", "2024-03-10"),
    ("Phase 2", "2024-03-10", "2024-03-30"),
    ("Phase 3", "2024-03-30", "2024-04-15"),
    ("Final Deployment", "2024-04-15", "2024-04-21"),
]

# Conversion des dates en format datetime
df = pd.DataFrame(tasks, columns=["Task", "Start", "End"])
df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])
df["Duration"] = df["End"] - df["Start"]

# Palette de couleurs distinctes pour chaque tâche
colors = plt.cm.get_cmap("tab10", len(df))  # Utilisation d'une palette de couleurs différentes

# Création du diagramme de Gantt avec des couleurs
fig, ax = plt.subplots(figsize=(10, 5))

# Création des barres colorées
for i, (task, start, end, duration) in enumerate(zip(df["Task"], df["Start"], df["End"], df["Duration"])):
    ax.barh(task, width=duration.days, left=start, height=0.5, align="center", color=colors(i))

# Format des dates sur l'axe X
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))  # Affichage des dates tous les 10 jours
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.xticks(rotation=45)

# Titres et labels
ax.set_xlabel("Dates")
ax.set_ylabel("Tasks")
ax.set_title("Indicative Gantt Chart")

# Affichage du diagramme
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()
