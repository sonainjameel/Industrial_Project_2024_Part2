import yaml
import argparse
from stitching.stitching import load_and_stitch_images
from pca_processing.pca_processing import apply_pca

def main(config_path, task):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if task == "stitch":
        input_dir = config['paths']['input_dir']
        output_file = config['paths']['stitched_output']
        num_columns = config['parameters']['stitching']['num_columns']

        # Perform stitching
        load_and_stitch_images(input_dir, output_file, num_columns)
        
    elif task == "pca":
        input_file = config['paths']['stitched_output']
        output_dir = config['paths']['pca_output_dir']
        pca_params = config['parameters']['pca']

        # Perform PCA on stitched image
        apply_pca(
            input_file,
            output_dir,
            n_components=pca_params['n_components'],
            transformation=pca_params['transformation'],
            lower_percentile=pca_params['lower_percentile'],
            upper_percentile=pca_params['upper_percentile']
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run stitching or PCA task.")
    parser.add_argument("config_path", type=str, help="Path to the configuration file")
    parser.add_argument("task", type=str, choices=["stitch", "pca"], help="Task to perform: 'stitch' or 'pca'")
    args = parser.parse_args()
    main(args.config_path, args.task)
