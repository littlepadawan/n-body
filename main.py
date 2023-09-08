import struct
from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


Body = namedtuple("Body", ["x_pos", "y_pos", "mass", "x_vel", "y_vel", "brightness"])
TIMESTEP = 10 ** -5
TIME = 100
MACHINE_EPSILON = 10 ** -3

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
    sum = 0
    body_i.x_pos
    for j, body_j in enumerate(bodies):
        if j == i: # Skip calculation for the body itself
            continue
        r = (body_i.x_pos - body_j.x_pos) + (body_i.y_pos - body_j.y_pos) # TODO Each parentheses is supposed to be multiplied with e_x respectively e_y??
        r_squared = (body_i.x_pos - body_j.x_pos) ** 2 + (body_i.y_pos - body_j.y_pos) ** 2 # NEEDED?
        r_hat = r/r # TODO Can this be anything other than 1? NEEDED?

        sum += (body_j.mass / (r + MACHINE_EPSILON)) * r
    
    force = -G * body_i.mass * sum

    return force
        
def update_position(body, index, bodies):
    '''
    Update the position of a body

    Parameters:
    body (Body): The body to update position of.
    bodies (list of Body): All of the bodies.

    Returns:
    Body: A new instance of Body, with the same mass and brightness as
    body but with updated velocity and position.
    '''
    force = calculate_force(body, index, bodies) 
    acceleration = force / body.mass
    
    # New velocity
    new_vel_x = body.x_vel + TIMESTEP * acceleration
    new_vel_y = body.y_vel + TIMESTEP * acceleration

    # New position
    new_pos_x = body.x_pos + TIMESTEP * new_vel_x
    new_pos_y = body.y_pos + TIMESTEP * new_vel_y
    
    # Create new Body with same mass and brightness as body, but with new velocity and new position
    new_body = Body(x_pos = new_pos_x, y_pos = new_pos_y, mass = body.mass, x_vel = new_vel_x, y_vel = new_vel_y, brightness = body.brightness)
    #print(f"{'Old body: '} x_pos={body.x_pos}, y_pos={body.y_pos}, x_vel={body.x_vel}, y_vel={body.y_vel} ")
    #print(f"{'New body: '} x_pos={new_body.x_pos}, y_pos={new_body.y_pos}, x_vel={new_body.x_vel}, y_vel={new_body.y_vel} ")
    print()
   
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

def animate(frame, bodies):
    updated_bodies = update_all_positions(bodies)
    x_positions = [body.x_pos for body in updated_bodies]
    y_positions = [body.y_pos for body in updated_bodies]
    ax.plot(x_positions, y_positions, 'o', markersize=3, label='Bodies')
    return updated_bodies


bodies = convert_data_to_bodies(get_data('input_data/circles_N_2.gal'))

fig, ax = plt.subplots()
animation = FuncAnimation(fig, animate, frames=10, fargs = (bodies,), interval=10)
plt.show()

# def run_simulation(file_name, ax):
#     bodies = get_data(file_name)
#     init_plot(bodies, ax)
#     t = 0
#     while (t < time):
#         bodies = update_all(bodies)
#         new_plot(bodies)
#         t += timestep
#     return bodies

# def init_plot(bodies, ax):
#     x_positions = [body.x_pos for body in bodies]
#     y_positions = [body.y_pos for body in bodies]
#     ax.plot(x_positions, y_positions, 'o', markersize=1, label='Bodies')

#     ax.set_title('Initial position of bodies')
#     ax.legend()
#     plt.show()
    


# Check that reading the file works
# data = get_data('input_data\ellipse_N_00010.gal')
# print (data)

# Check that creating bodies work 
# bodies_test = convert_data_to_bodies(data)
# print(bodies_test)

# fig, ax = plt.subplots()

# x_positions = [body.x_pos for body in bodies_test]
# y_positions = [body.y_pos for body in bodies_test]

# ax.plot(x_positions, y_positions, 'o', markersize=1, label='Bodies')

# ax.set_title('Initial position of bodies')
# ax.legend()

# plt.show()