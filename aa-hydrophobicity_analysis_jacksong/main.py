"""
Protein Sequence Hydrophobicity and Composition Analyzer (Python 3)

This Python 3 script processes protein sequences from a FASTA file, calculates their amino acid
composition and average hydrophobicity using the Kyte-Doolittle scale, and generates
visualizations (histograms, bar charts) and a summary CSV file. It accepts user-specified
parameters via command-line arguments and saves output to a designated directory.

DISCLAIMER: AI tools were used to help develop this script.

"""

import argparse
import os
import sys  # Import the sys module for exit
import re  # Import re

# Import the modules from the package
from package import amino_acid_analysis
from package import visualizations

# Define the Kyte-Doolittle scale as a constant
KYTE_DOOLITTLE_SCALE = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

class InputValidator:
    """
    Class to handle input validation
    """
    def __init__(self, fasta_file, output_dir):
        """
        Constructor for the InputValidator class
        """
        self.fasta_file = fasta_file
        self.output_dir = output_dir

    def validate_fasta_file(self):
        """
        Method to validate the FASTA file
        """
        if not os.path.exists(self.fasta_file):
            print(f"Error: FASTA file not found at {self.fasta_file}")
            return False
        return True

    def validate_output_dir(self):
        """
        Method to validate the output directory
        """
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
                print(f"Created output directory: {self.output_dir}")
            except OSError as e:
                print(f"Error creating output directory: {e}")
                return False  # Indicate failure
        return True  # Indicate success

def main():
    """
    Main function to run the script
    """
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Analyze amino acid sequences from a FASTA file, calculate composition and hydrophobicity, and generate visualizations.")
    parser.add_argument("--fasta_file", "-f", required=True, help="Path to the input FASTA file.")
    parser.add_argument("--output_dir", "-o", default="output/", help="Path to the output directory (default: 'output/').")
    parser.add_argument("--parameter", "-p", type=int, default=1, help="Number of top/bottom sequences to report in .csv file.")
    args = parser.parse_args()
    # --- End Argument Parsing ---

    # Get the values from the parsed arguments
    fasta_file = args.fasta_file
    output_dir = args.output_dir
    top_n = args.parameter # Get the top_n value from arguments

    # Create an instance of the InputValidator class
    validator = InputValidator(fasta_file, output_dir)

    # Validate the input FASTA file.  Exit if there's an error.
    if not validator.validate_fasta_file():
        sys.exit(1)  # Use sys.exit() for a cleaner exit

    # Validate the output directory. Create if it doesn't exist.
    if not validator.validate_output_dir():
        sys.exit(1)  # Exit if cannot create output directory

    # Create an instance of SequenceAnalyzer with the Kyte-Doolittle scale
    analyzer = amino_acid_analysis.SequenceAnalyzer(KYTE_DOOLITTLE_SCALE)
    results = amino_acid_analysis.analyze_sequences(fasta_file, analyzer)

    # Analyze the sequences
    try:
        analysis_results = amino_acid_analysis.analyze_sequences(fasta_file, analyzer)
    except Exception as e:
        print(f"Error during sequence analysis: {e}")
        sys.exit(1)

    # Create an instance of DataVisualizer with the output directory
    visualizer = visualizations.DataVisualizer(output_dir)  

    # Generate and save the histograms
    try:
        visualizer.generate_histograms(analysis_results)  
    except Exception as e:
        print(f"Error generating histograms: {e}")
        sys.exit(1)

    # Generate and save the bar chart
    try:
        visualizer.generate_bar_chart(analysis_results)  
    except Exception as e:
        print(f"Error generating bar chart: {e}")
        sys.exit(1)

    # Generate and save the .csv summary file
    try:
        visualizer.create_hydrophobicity_csv(analysis_results, top_n)
    except Exception as e:
        print(f"Error generating .csv file: {e}")
        sys.exit(1)

    print(f"Analysis complete. Results and visualizations saved in: {output_dir}")

if __name__ == "__main__":
    main()