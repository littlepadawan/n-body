import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

TIMESTEP = 0.00001  # 10 ** (-5), given in assignment
EPSILON = 0.001  # 10 ** (-3), given in assignment
NUMOFCALC = 201 # Decides number of calculations

# Kör rad nedan för att välja datafil. Kolla att pathen stämmer.
# För referens kör rad nedan
# ./compare_gal_files/compare_gal_files ANTAL_BODIES REFERENSFIL output.gal

# Get binary data from fil

data = np.fromfile("input_data\ellipse_N_00010.gal", dtype=float, ) # pos_maxdiff = 0.026866764988
# data = np.fromfile("input_data\ellipse_N_00100.gal", dtype=float, ) # pos_maxdiff = 0.021573955637
# data = np.fromfile("input_data\circles_N_2.gal", dtype=float, ) # ej ref data, endast för oservation av animation
#data = np.fromfile("input_data\sun_and_planets_N_4.gal", dtype=float, ) # ej ref data, endast för oservation av animation

N = int(len(data) / 6) # Number of bodies
G = 100 / N # Gravitational constant

# Groups data into arrays corresponding to what the data represents
data = data.reshape(-1, 6)

# Allocate space for all data points that will be generated
x_pos_history = np.zeros((NUMOFCALC, N))
y_pos_history = np.zeros((NUMOFCALC, N))
x_vel_history = np.zeros((NUMOFCALC, N))
y_vel_history = np.zeros((NUMOFCALC, N))

# Extract data to separate arrays
# Mass and brightness are never manipulated
x_pos_history[0] = data[:, 0]
y_pos_history[0] = data[:, 1]
mass             = data[:, 2]
x_vel_history[0] = data[:, 3]
y_vel_history[0] = data[:, 4]
brightness       = data[:, 5]

# Calculate force exerted on one particle
def calculate_force(time_step, current):
    sum_force_x = 0
    sum_force_y = 0

    for i in range(N):
        if i == current:
            continue

        dx = x_pos_history[time_step-1][current] - x_pos_history[time_step-1][i]
        dy = y_pos_history[time_step-1][current] - y_pos_history[time_step-1][i]

        r_squared = dx ** 2 + dy ** 2
        r = np.sqrt(r_squared)
        denominator = (r + EPSILON) ** 3

        force_x = (mass[i] / denominator) * dx
        force_y = (mass[i] / denominator) * dy

        sum_force_x += force_x
        sum_force_y += force_y

    sum_force_x = -G * mass[current] * sum_force_x
    sum_force_y = -G * mass[current] * sum_force_y
    return sum_force_x, sum_force_y

# Update position of one particle
def update_position(time_step, current):
    sum_force_x, sum_force_y = calculate_force(time_step, current)
    
    # acceleration
    acceleration_x = sum_force_x / mass[current]
    acceleration_y = sum_force_y / mass[current]

    # new velocity
    x_vel_history[time_step][current] = x_vel_history[time_step-1][current] + (TIMESTEP * acceleration_x)
    y_vel_history[time_step][current] = y_vel_history[time_step-1][current] + (TIMESTEP * acceleration_y)

    # new position
    x_pos_history[time_step][current] = x_pos_history[time_step-1][current] + (TIMESTEP * x_vel_history[time_step][current])
    y_pos_history[time_step][current] = y_pos_history[time_step-1][current] + (TIMESTEP * y_vel_history[time_step][current])

 # Make all calculations 
def main_sim():
    for time_step in range(1, NUMOFCALC):
        for current in range(N):
            update_position(time_step, current)

main_sim()

# Put data of last time step in the same order as
output = np.zeros(N*6)
for i in range(0, N, 1):
    output[i*6]   = (x_pos_history[NUMOFCALC-1][i])
    output[i*6+1] = (y_pos_history[NUMOFCALC-1][i])
    output[i*6+2] = (mass[i])
    output[i*6+3] = (x_vel_history[NUMOFCALC-1][i])
    output[i*6+4] = (y_vel_history[NUMOFCALC-1][i])
    output[i*6+5] = (brightness[i])


#print(output)
# Write data for last time step to file
output.tofile("output.gal")

# Animate 
fig, ax = plt.subplots()

def animate(frame, x_pos_history, y_pos_history):
    ax.clear()
    ax.scatter(x_pos_history[frame], y_pos_history[frame], s=1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.plot(x_pos_history[frame], y_pos_history[frame], 'o', markersize=3)
    ax.set_title(f"Frame {frame}")

# Create the animation, comment this out if you do not want an animation
anim = FuncAnimation(fig, animate, frames=NUMOFCALC, fargs=(x_pos_history, y_pos_history), interval=0.01, repeat=False)
plt.show()



