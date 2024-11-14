import os
import numpy as np
import cv2
from pathlib import Path
from envi2 import read_envi, write_envi

def load_and_stitch_images(input_dir, output_file, num_columns=8):
    def numeric_sort_key(filename):
        return int(filename.split('_')[0])

    reflectance_images = []
    for filename in sorted(os.listdir(input_dir), key=numeric_sort_key):
        if filename.endswith('.hdr'):
            # Load each hyperspectral cube
            sample_cube, wavelengths, header = read_envi(Path(input_dir) / filename, normalize=False)
            reflectance_images.append(sample_cube)
    
    # Determine maximum dimensions to resize all images to a common size
    max_height = max(img.shape[0] for img in reflectance_images)
    max_width = max(img.shape[1] for img in reflectance_images)
    resized_images = [cv2.resize(img, (max_width, max_height), interpolation=cv2.INTER_LINEAR) for img in reflectance_images]

    # Stitch images into rows and then concatenate rows vertically
    stitched_rows = []
    for start_idx in range(0, len(resized_images), num_columns):
        row_images = resized_images[start_idx:start_idx + num_columns]
        stitched_row = np.concatenate(row_images, axis=1)
        stitched_rows.append(stitched_row)

    # Final stitched image
    stitched_image = np.concatenate(stitched_rows, axis=0)

    # Ensure the output directory exists
    output_dir = Path(output_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save stitched image using write_envi
    header_stitched = write_envi(Path(output_file), header, stitched_image, wavelengths)
    print(f"Stitched image saved at {output_file}")
