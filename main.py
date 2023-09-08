import struct
from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Body = namedtuple("Body", ["x_pos", "y_pos", "mass", "x_vel", "y_vel", "brightness"])
timestep = 10 ** -5
time = 10

def get_data(file_name):
    # Open the binary file in binary read mode
    with open(file_name, 'rb') as file:
        # Read the binary data from the file
        binary_data = file.read()
    # Calculate the number of double-precision floats in the binary data
    num_doubles = len(binary_data) // 8  # Assuming each double is 8 bytes

    # Unpack the binary data into a list of floats
    float_list = struct.unpack('d' * num_doubles, binary_data)

    # Return list of floats
    return float_list

def get_bodies(data):
    bodies = []
    i = 0
    while (i < len(data)):
        body = Body(x_pos=data[i], y_pos=data[i+1], mass=data[i+2], x_vel=data[i+3], y_vel=data[i+4], brightness=data[i+5])
        bodies.append(body)
        i+=6
    return bodies

def calculate_force(body, bodies): #TODO
    return 5
        
def update_pos(body, bodies):
    acc = calculate_force(body, bodies) / body.mass
    
    # Update velocity
    new_vel_x = body.x_vel + timestep * acc
    new_vel_y = body.y_vel + timestep * acc

    # Update position
    new_pos_x = body.x_pos + timestep * new_vel_x
    new_pos_y = body.y_pos + timestep * new_vel_y
    
    # Update new_body
    new_body = Body(x_pos=new_pos_x, y_pos=new_pos_y, mass=body.mass, x_vel=new_vel_x, y_vel=new_vel_y, brightness=body.brightness)
    
    return new_body
    
    
def update_all(bodies): # State for one frame
    new_bodies = []
    for body in bodies:
        new_bodies.append(update_pos(body, bodies))
    return new_bodies

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
    
# def new_plot(bodies, ax):
    
#     ax.clear()
#     x_positions = [body.x_pos for body in bodies]
#     y_positions = [body.y_pos for body in bodies]
#     ax.plot(x_positions, y_positions, 'o', markersize=1, label='Bodies')

fig, ax = plt.subplots()
actual_bodies = get_bodies(get_data('n-body\input_data\ellipse_N_00010.gal'))
animation = FuncAnimation(fig, update_all, frames=100, interval=100)
plt.show()



# Check that reading the file works
# data = get_data('input_data\ellipse_N_00010.gal')
# print (data)

# Check that creating bodies work 
# bodies_test = get_bodies(data)
# print(bodies_test)

# fig, ax = plt.subplots()

# x_positions = [body.x_pos for body in bodies_test]
# y_positions = [body.y_pos for body in bodies_test]

# ax.plot(x_positions, y_positions, 'o', markersize=1, label='Bodies')

# ax.set_title('Initial position of bodies')
# ax.legend()

# plt.show()