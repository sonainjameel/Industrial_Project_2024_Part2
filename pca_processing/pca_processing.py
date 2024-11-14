import os
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pathlib import Path
from envi2 import read_envi  

def apply_transformation(sample_cube, transformation):
    if transformation == "none":
        return sample_cube
    elif transformation == "standard_normal":
        return (sample_cube - np.mean(sample_cube, axis=2, keepdims=True)) / np.std(sample_cube, axis=2, keepdims=True)
    elif transformation == "first_derivative":
        return np.diff(sample_cube, axis=2)
    elif transformation == "second_derivative":
        return np.diff(np.diff(sample_cube, axis=2), axis=2)
    else:
        raise ValueError("Invalid transformation type.")

def enhance_contrast_percentile(image, lower_percentile, upper_percentile):
    lower_threshold = np.percentile(image, lower_percentile)
    upper_threshold = np.percentile(image, upper_percentile)
    contrast_image = np.clip(image, lower_threshold, upper_threshold)
    contrast_image = 255 * (contrast_image - lower_threshold) / (upper_threshold - lower_threshold)
    return contrast_image.astype(np.uint8)

def apply_pca(input_file, output_dir, n_components=20, transformation="none", lower_percentile=2, upper_percentile=98):
    # Convert input_file to a Path object if it’s not already one
    input_file = Path(input_file)
    
    # Read the stitched image
    sample_cube, _, _ = read_envi(input_file, normalize=False)
    transformed_cube = apply_transformation(sample_cube, transformation)
    
    height, width, num_bands = transformed_cube.shape
    reshaped_cube = transformed_cube.reshape(-1, num_bands)

    # Perform PCA
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(reshaped_cube)
    pca_images = principal_components.reshape(height, width, n_components)

    os.makedirs(output_dir, exist_ok=True)
    for i in range(n_components):
        pca_component = pca_images[:, :, i]
        if transformation in ["first_derivative", "second_derivative"]:
            pca_component = enhance_contrast_percentile(pca_component, lower_percentile, upper_percentile)
        output_path = os.path.join(output_dir, f'PCA_Component_{i+1}.png')
        plt.imsave(output_path, pca_component, cmap='gray')
        print(f'Saved PCA component {i+1} at {output_path}')
