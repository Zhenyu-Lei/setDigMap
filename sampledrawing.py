import json
from PIL import Image
import matplotlib.pyplot as plt
import random

# Load the JSON file
with open('closest_points.json') as f:
    data = json.load(f)

# Get all unique starting ids in the data
start_ids = set(elem['id1'] for elem in data)

# Randomly select 10 starting ids
selected_start_ids = random.sample(start_ids, 20)

# Load the image
img = Image.open('roadimage.jpg')

# Create a plot
fig, ax = plt.subplots()

# Plot the image
ax.imshow(img)

# Plot the endpoints and lines
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
for start_id in selected_start_ids:
    # Extract matching elements for the current starting id
    matching_elements = [elem for elem in data if elem['id1'] == start_id]

    # Extract the ending ids and coordinates for each matching element
    end_ids = [elem['id2'] for elem in matching_elements]
    end_coords = [(elem['x2'], elem['y2']) for elem in matching_elements]

    # Plot the starting point
    ax.plot(int(matching_elements[0]['x1']), int(matching_elements[0]['y1']), 'r.')

    # Plot the ending points and lines
    for i, (x2, y2) in enumerate(end_coords):
        ax.plot(x2, y2, 'g.', label=f'Endpoint {end_ids[i]}')
        ax.plot([int(matching_elements[0]['x1']), x2], [int(matching_elements[0]['y1']), y2], colors[2])

    # Add legend
    ax.legend(['Starting Point', 'Endpoint'])

# Save the plot as a PNG file
plt.savefig('sampledraw.png', dpi=300)

# Show the plot
plt.show()
