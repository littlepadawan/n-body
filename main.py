import struct
from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Body = namedtuple("Body", ["x_pos", "y_pos", "mass", "x_vel", "y_vel", "brightness"])

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
        
# Check that reading the file works
data = get_data('input_data/circles_N_4.gal')
print (data)

# Check that creating bodies work 
bodies = get_bodies(data)
print(bodies)

fig, ax = plt.subplots()

x_positions = [body.x_pos for body in bodies]
y_positions = [body.y_pos for body in bodies]

ax.plot(x_positions, y_positions, 'o', markersize=10, label='Bodies')

ax.set_title('Initial position of bodies')
ax.legend()

plt.show()