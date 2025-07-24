import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re
import math

# Setup Serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Adjust COM port if needed

# Regex Pattern to match: pitch is : -5.605316   roll is : 1.789911
pattern = re.compile(r"pitch is\s*:\s*(-?\d+\.?\d*)\s+roll is\s*:\s*(-?\d+\.?\d*)")

# Init Figure
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
arrow_line, = ax.plot([], [], lw=3)

# For smoothing
filtered_roll = 0.0
alpha = 0.1  # smoothing factor

# Arrow generator
def get_arrow_coords(angle_deg):
    angle_rad = math.radians(angle_deg)
    x = math.cos(angle_rad)
    y = math.sin(angle_rad)
    return [0, x], [0, y]

# Main update loop
def update(frame):
    global filtered_roll
    try:
        line = ser.readline().decode('utf-8').strip()
        print("From Serial:", line)

        match = pattern.search(line)
        if match:
            pitch = float(match.group(1))
            roll = float(match.group(2))

            # Optional smoothing
            filtered_roll = alpha * roll + (1 - alpha) * filtered_roll

            # Update arrow
            x_vals, y_vals = get_arrow_coords(filtered_roll)
            arrow_line.set_data(x_vals, y_vals)

    except Exception as e:
        print("Error reading/processing:", e)

    return arrow_line,

# Animate
ani = FuncAnimation(fig, update, interval=100, blit=True, cache_frame_data=False)
plt.title("Live Roll Arrow (from IMU)")
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
