import numpy as np
from PIL import Image, ImageDraw
import random

def imagegen(output_path=None):
    """
    Generate a 128x128 PNG image with a random circular pattern.
    
    Parameters:
        output_path (str): Optional. If provided, saves the image to this path.
        
    Returns:
        PIL.Image.Image: The generated image.
    """
    # Image dimensions
    width, height = 128, 128
    number_of_points = random.randint(8, 24)

    # Colors
    blue_to_purple = [
        (random.randint(0, 128), random.randint(0, 128), random.randint(128, 255), 255)
        for _ in range(number_of_points)
    ]

    # Create a blank image with transparency
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Generate random points around the center in a rough circular pattern
    center_x, center_y = width // 2, height // 2
    radius = 40  # Base radius for the circle
    points = [
        (
            center_x + int(random.uniform(0.8, 1.2) * radius * np.cos(2 * np.pi * i / number_of_points)),
            center_y + int(random.uniform(0.8, 1.2) * radius * np.sin(2 * np.pi * i / number_of_points))
        )
        for i in range(number_of_points)
    ]

    # Generate a random greyscale color for the fill
    random_greyscale = (random.randint(80, 100),) * 3 + (255,)

    # Fill the polygon with random greyscale
    draw.polygon(points, fill=random_greyscale)

    # Draw lines connecting the points
    for i in range(len(points)):
        start_point = points[i]
        end_point = points[(i + 1) % len(points)]
        draw.line([start_point, end_point], fill=random.choice(blue_to_purple), width=6)

    # Save the image if an output path is provided
    if output_path:
        image.save(output_path)

    return image
