import serial
import matplotlib.pyplot as plt

# configure the serial port
ser = serial.Serial(
    port='COM10',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()

# List to store current coordinates
curr_x_coordinates = []
curr_y_coordinates = []

# List to store coordinates of detected metals
metal_x_coordinates = []
metal_y_coordinates = []

# Current coordinates
current_x = 0
current_y = 0

# Read data until we stop receiving values
while True:
    line = ser.readline().decode().strip()
    if not line:  # Break the loop when no more data is received
        break
    
    try:
        if line.startswith("SStrength:"):
            strength = int(line.split(":")[1])
            if strength >= 2:
                # Metal detected
                print("Metal detected at coordinates:", (current_x, current_y))
                metal_x_coordinates.append(current_x)
                metal_y_coordinates.append(current_y)
                continue  # Skip the rest of the loop for metal detections
    except ValueError:
        # Ignore other lines and continue
        continue

    coordinates = line.split()
    if len(coordinates) == 2:
        x, y = map(float, coordinates)
        if (x, y) == (16, 16):
            current_x += 0
            current_y += 0
        elif (x, y) == (33, 16):
            current_x += 0
            current_y += 1
        elif (x, y) == (0, 16):
            current_x += 0
            current_y -= 0
        elif (x, y) == (16, 33):
            current_x += 1
            current_y += 0
        elif (x, y) == (16, 0):
            current_x -= 1
            current_y += 0

        curr_x_coordinates.append(current_x)
        curr_y_coordinates.append(current_y)

        print("Current coordinates:", (current_x, current_y))

# Close serial port
ser.close()

# Print metal detection coordinates
print("Metal detection coordinates:")
print("X:", metal_x_coordinates)
print("Y:", metal_y_coordinates)

# Plot the final path
plt.plot(curr_x_coordinates, curr_y_coordinates, color='blue', label='Robot Path')
plt.scatter(metal_x_coordinates, metal_y_coordinates, color='red', label='Metal Detection')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Robot Path and Metal Detection')
plt.grid(True)
plt.legend()
plt.show()

