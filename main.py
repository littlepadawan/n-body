import struct
from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math


Body = namedtuple("Body", ["x_pos", "y_pos", "mass", "x_vel", "y_vel", "brightness"])
TIMESTEP = 10**(-5)
TIME = 200
MACHINE_EPSILON = 10**(-3)

def get_data(file_name):
    """
    Get binary data from file and convert to list of double precision floats.

    Parameters:
    file_name (string): Name of the file containing binary data.

    Returns:
    list: List of data as floats.
    """

    # Open the binary file 
    with open(file_name, 'rb') as file:
        binary_data = file.read()

    # Calculate the number of double-precision floats in the binary data, assuming each double is 8 bytes
    num_doubles = len(binary_data) // 8  

    # Unpack the binary data into a list of floats
    float_list = struct.unpack('d' * num_doubles, binary_data)

    return float_list

def convert_data_to_bodies(data):
    """
    Convert data to a list of tuples, where each tuple is a Body.

    Parameters:
    data (list): List of floats representing body data. The order of numbers in list 
    is as follows:
        body 0 position x
        body 0 particle y
        body 0 mass
        body 0 velocity x
        body 0 velocity y
        body 1 brightness
        body 1 position x
        body 1 particle y
        body 1 mass
        ...

    Returns:
    list: List containing multiple instances of Body.
    """

    bodies = []
    i = 0

    while (i < len(data)):
        body = Body(x_pos = data[i], y_pos = data[i + 1], mass = data[i + 2], x_vel = data[i + 3], y_vel = data[i + 4], brightness = data[i + 5])
        bodies.append(body)
        i += 6

    return bodies

def calculate_force(body_i, i, bodies): 
    G = 100 / len(bodies)
    sum_x = 0
    sum_y = 0

    for j, body_j in enumerate(bodies):
        if j == i: # Skip calculation for the body itself
            continue

        dx = abs(body_j.x_pos - body_i.x_pos)
        dy = abs(body_j.y_pos - body_i.y_pos)

        r_squared = dx ** 2 + dy ** 2 
        r = math.sqrt(r_squared)
        denominator = (r + MACHINE_EPSILON) ** 3
        
        force_x = (G * body_i.mass * body_j.mass / denominator) * dx
        force_y = (G * body_i.mass * body_j.mass / denominator) * dy

        sum_x += force_x
        sum_y += force_y

    return sum_x, sum_y

def update_position(body, index, bodies):
    ''''
    body (Body): The body to update position of.
    bodies (list of Body): All of the bodies.

    Returns:
    Body: A new instance of Body, with the same mass and brightness as
    body but with updated velocity and position.
    '''
    force_x, force_y  = calculate_force(body, index, bodies) 
    acceleration_x = force_x / body.mass
    acceleration_y = force_y / body.mass
    
    # New velocity
    new_vel_x = body.x_vel + TIMESTEP * acceleration_x
    new_vel_y = body.y_vel + TIMESTEP * acceleration_y

    # New position
    new_pos_x = body.x_pos + TIMESTEP * new_vel_x
    new_pos_y = body.y_pos + TIMESTEP * new_vel_y
    
    # Create new Body with same mass and brightness as body, but with new velocity and new position
    new_body = Body(x_pos = new_pos_x, y_pos = new_pos_y, mass = body.mass, x_vel = new_vel_x, y_vel = new_vel_y, brightness = body.brightness)
    # print(f"{'Old body: '} x_pos={body.x_pos}, y_pos={body.y_pos}, x_vel={body.x_vel}, y_vel={body.y_vel} ")
    # print(f"{'New body: '} x_pos={new_body.x_pos}, y_pos={new_body.y_pos}, x_vel={new_body.x_vel}, y_vel={new_body.y_vel} ")
    #print()
    return new_body
    
    
def update_all_positions(bodies): 
    '''
    Update the position of all bodies.

    Parameters:
    bodies (list): List of the bodies to update.

    Return:
    list: List containing bodies with updated positions. 
    '''
    new_bodies = []

    for index, body in enumerate(bodies):
        new_bodies.append(update_position(body, index, bodies))

    #print(new_bodies)
    return new_bodies

#bodies = convert_data_to_bodies(get_data('input_data/ellipse_N_00010.gal'))

fig, ax = plt.subplots()

# Define a list to store the bodies
bodies_container = [convert_data_to_bodies(get_data('input_data/ellipse_N_00010.gal'))]

def animate(frame, bodies_container):
    # Update the positions of the bodies
    bodies = bodies_container[0]
    bodies = update_all_positions(bodies)
    bodies_container[0] = bodies

    # Clear the axis and plot the updated positions
    ax.clear()
    x_positions = [body.x_pos for body in bodies]
    y_positions = [body.y_pos for body in bodies]
    ax.plot(x_positions, y_positions, 'o', markersize=5, label='Bodies')

     # Set fixed limits for the x and y axes (adjust these values as needed)
    ax.set_xlim(-0.5, 1.5)  # Set x-axis limits
    ax.set_ylim(-0.5, 1.5)  # Set y-axis limits
    
    # Customize your plot here (titles, labels, legends, etc.)
    ax.set_title(f'Time Step {frame + 1}')
    ax.legend()

# Create an animation with a frame for each time step
animation = FuncAnimation(fig, animate, frames=TIME, fargs=(bodies_container,), interval=1, repeat=False)  # 'TIME' is the total number of time steps

# Show the animation
plt.show()

def write_bodies_to_gal(bodies, output_filename):
    with open(output_filename, 'wb') as file:
        for body in bodies:
            file.write(struct.pack('d', body.x_pos))
            file.write(struct.pack('d', body.y_pos))
            
            # Write mass
            file.write(struct.pack('d', body.mass))
            
            # Write velocity
            file.write(struct.pack('d', body.x_vel))
            file.write(struct.pack('d', body.y_vel))
            
            # Write brightness
            file.write(struct.pack('d', body.brightness))
            print(body.x_pos)
            print(body.y_pos)
            print(body.mass)
            print(body.x_vel)
            print(body.y_vel)
            print(body.brightness)
            print()

write_bodies_to_gal(bodies_container[0], 'output.gal')
"""
def animate(frame, bodies):
    updated_bodies = update_all_positions(bodies)
    x_positions = [body.x_pos for body in updated_bodies]
    y_positions = [body.y_pos for body in updated_bodies]
    ax.clear()
    ax.plot(x_positions, y_positions, 'o', markersize=3, label='Bodies')
    return updated_bodies



fig, ax = plt.subplots()
animation = FuncAnimation(fig, animate, frames=10, fargs = (bodies,), interval=1000)
plt.show()

"""