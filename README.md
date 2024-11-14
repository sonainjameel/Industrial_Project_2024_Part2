
# Industrial Project Part 2: Stitching and PCA

This project is designed to process spectral image data by performing image stitching and Principal Component Analysis (PCA). The project enables the assembly of multiple spectral images into a single, stitched image and performs dimensionality reduction on the stitched data using PCA. 

## Features

- **Image Stitching**: Combines multiple hyperspectral images into a single, high-resolution stitched image.
- **Transformation Options**: Applies transformations to the stitched image before PCA, including:
  - No Transformation
  - Standard Normal Transformation
  - First Derivative (with contrast enhancement)
  - Second Derivative (with contrast enhancement)
- **PCA on Spectral Data**: Reduces the dimensionality of the stitched hyperspectral image, saving each principal component as an individual grayscale PNG image.
- **Configurable Parameters**: Uses a `config.yaml` file to set paths, transformation options, and other processing parameters.

## Installation

### Requirements

- Python 3.8 or higher
- The following Python libraries:
  - `numpy`
  - `matplotlib`
  - `PyYAML`
  - `opencv-python`
  - `scikit-learn`

### Setup Instructions

1. **Clone the repository** to your local machine:
   ```bash
   git clone https://github.com/sonainjameel/Industrial_Project_2024_Part2.git
   cd Industrial_Project_2024_Part2
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Input Data**: Ensure you have the correct input data in the directories specified in `config.yaml`.

## Configuration

The project relies on a `config.yaml` file for setting input paths and processing parameters. Below is an example configuration:

```yaml
paths:
  input_dir: "data/input/images"            # Directory containing input hyperspectral images
  stitched_output: "data/stitched/stitched_image.hdr"  # Path to save stitched hyperspectral image
  pca_output_dir: "data/pca_output"         # Directory for saving PCA component images

parameters:
  stitching:
    num_columns: 8                          # Number of images per row in the stitched output
  pca:
    n_components: 20                        # Number of PCA components to keep
    transformation: "first_derivative"       # Options: "none", "standard_normal", "first_derivative", "second_derivative"
    lower_percentile: 2                     # Percentile for contrast enhancement in derivatives
    upper_percentile: 98
```

## Usage

To run each part of the pipeline, specify the configuration file and task (`stitch` or `pca`) in the command line.

### Stitching

Run the stitching process to create a stitched hyperspectral image from the input directory:

```bash
python3 main.py config.yaml stitch
```

The stitched image will be saved at the location specified in `config.yaml` under `stitched_output`.

### PCA Processing

Run PCA processing on the stitched image, with optional transformations:

```bash
python main.py config.yaml pca
```

The resulting PCA components will be saved as PNG files in the directory specified under `pca_output_dir` in `config.yaml`.

## Project Structure

```
industrial_project_part2/
├── config.yaml                  # Configuration file for paths and parameters
├── main.py                      # Main script to run stitching or PCA processing
├── requirements.txt             # Required libraries
├── stitching/                   # Module for stitching functionality
│   ├── __init__.py
│   └── stitching.py             # Functions for loading and stitching images
├── pca_processing/              # Module for PCA functionality
│   ├── __init__.py
│   └── pca_processing.py        # Functions for transformations, PCA, and saving components
└── Output/                        
    ├── stitched/                # Folder to save the stitched image
    │   └── stitched_image.hdr   # Stitched hyperspectral image (input for PCA)
    └── pca_output/              # Folder to save PCA component images
        ├── PCA_Component_1.png  # Each PCA component saved as a PNG image
        ├── PCA_Component_2.png
        └── ...
```

### Key Modules

- **`stitching/stitching.py`**: Handles image loading, resizing, stitching, and saving the final stitched hyperspectral image.
- **`pca_processing/pca_processing.py`**: Applies optional transformations (e.g., derivatives, standard normal), performs PCA on the transformed image, and saves each principal component with optional contrast enhancement.

## Available Transformations for PCA

- **None**: Uses the stitched image without modification.
- **Standard Normal Transformation**: Normalizes each spectral band to mean 0 and standard deviation 1.
- **First Derivative**: Computes the first derivative along the spectral axis, highlighting spectral changes.
- **Second Derivative**: Computes the second derivative along the spectral axis, emphasizing areas with rapid spectral change.
- **Contrast Enhancement**: Enhances contrast for the first and second derivatives using percentile stretching.

## Contributing

We welcome contributions to this project. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a clear message.
4. Submit a pull request for review.

## License

This project is licensed under the MIT License.

## Acknowledgements

Group A (Sonain, Kasem, and Turab) especially thanks Joni Hyttinen and Prof. Markku Keinänen for their support in developing this project.
