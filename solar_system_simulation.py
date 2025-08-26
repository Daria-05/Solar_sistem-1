import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


G = 6.67430e-11   
M_sun = 1.989e30


planets = {
    "Меркурий": {"r": 57.9e9, "m": 3.3e23, "color": "gray", "size": 15},
    "Венера":   {"r": 108.2e9, "m": 4.87e24, "color": "orange", "size": 25},
    "Земля":    {"r": 149.6e9, "m": 5.97e24, "color": "blue", "size": 30},
    "Марс":     {"r": 227.9e9, "m": 6.42e23, "color": "red", "size": 20},
}

# --- Начальные условия ---
dt = 60 * 60 * 6  
steps = 3000      
positions = {name: [] for name in planets}

state = {}
for name, data in planets.items():
    r = data["r"]
    v = np.sqrt(G * M_sun / r)
    state[name] = {
        "pos": np.array([r, 0.0]),
        "vel": np.array([0.0, v]),
    }

# --- Симуляция (предрасчёт) ---
for _ in range(steps):
    for name, data in planets.items():
        pos = state[name]["pos"]
        vel = state[name]["vel"]

        # ускорение от гравитации
        r = np.linalg.norm(pos)
        acc = -G * M_sun * pos / r**3

        # обновляем скорость и позицию
        vel += acc * dt
        pos += vel * dt

        state[name]["pos"] = pos
        state[name]["vel"] = vel

        positions[name].append(pos.copy())

# --- Анимация ---
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_facecolor("black")
ax.set_aspect("equal", "box")

# границы графика (увеличим до орбиты Марса)
limit = planets["Марс"]["r"] * 1.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# солнце
ax.scatter(0, 0, color="yellow", s=300, label="Солнце")

# линии траекторий и точки планет
lines = {}
points = {}
for name, data in planets.items():
    line, = ax.plot([], [], color=data["color"], lw=1)
    point, = ax.plot([], [], "o", color=data["color"], markersize=data["size"] / 10)
    lines[name] = line
    points[name] = point

ax.legend()

# функция для обновления кадров
def update(frame):
    for name, data in planets.items():
        traj = np.array(positions[name][:frame])
        lines[name].set_data(traj[:,0], traj[:,1])
        points[name].set_data(traj[-1,0], traj[-1,1])
    return list(lines.values()) + list(points.values())

ani = animation.FuncAnimation(fig, update, frames=steps, interval=20, blit=True)
plt.show()
