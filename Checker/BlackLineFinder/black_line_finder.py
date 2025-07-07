import os
import sys
import cv2

script_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)

class BlackLineFinder:
    
    def __init__(self, image_folder, top_margin_percent=5, bottom_margin_percent=10):
            self.image_folder = image_folder
            self.top_margin_percent = top_margin_percent
            self.bottom_margin_percent = bottom_margin_percent
            
    def detect_black_lines(self, image_path):
        # Read image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Could not read image: {image_path}")
            return False

        img_height, img_width = img.shape
        top_margin_pixels = int((self.top_margin_percent / 100.0) * img_height)
        bottom_margin_pixels = int((self.bottom_margin_percent / 100.0) * img_height)

        # Invert image: black becomes white
        inverted = cv2.bitwise_not(img)

        # Threshold to binary
        _, binary = cv2.threshold(inverted, 200, 255, cv2.THRESH_BINARY)

        # Morphology to emphasize horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (img_width - 10, 1))
        horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)

        # Find all connected components
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(horizontal_lines, connectivity=8)

        for label in range(1, num_labels):  # Skip background
            x, y, w, h, area = stats[label]

            # Exclude lines within top or bottom margin
            if y < top_margin_pixels or (y + h) > (img_height - bottom_margin_pixels):
                continue

            # Accept if wide enough
            if w >= img_width * 0.98:
                return True

        return False
