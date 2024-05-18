import os
import subprocess

def run_inference_test(filename, method):
    """Run the inference engine test on a specific file with the given method."""
    try:
        result = subprocess.run(['python', 'main.py', filename, method], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running test for {filename}: {e.stderr}")

def main():
    # Directory containing the text files
    directory = 'test_files'

    # Method to use for inference (FC, BC, or TT)
    method = 'TT'

    # Loop through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            print(f"Running test for {filepath} using {method} method...")
            run_inference_test(filepath, method)
            print()  # Add a blank line between test results

if __name__ == "__main__":
    main()
