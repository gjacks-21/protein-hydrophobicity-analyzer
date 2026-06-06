# Project Title: Sequence Amino Acid (AA) Composition & Hydrophobicity Analyzer

## PSEUDOCODE FOR FIRST MODULE: amino_acid_analysis.py

0.  #!/usr/bin/env python3
1.  Import necessary tools (the sys module and SeqIO from Biopython).

###  CLASS: SequenceAnalyzer--A blueprint for analyzing sequences

    1.  INITIALIZE CLASS: constructor(self, hydrophobicity_scale) :
        # Store the hydrophobicity scale.

    2.  DEFINE METHOD: calculate_composition(sequence):
        # Calculate and return amino acid frequencies.
        1.  If sequence is empty, return empty result.
        2.  Count each amino acid.
        3.  Calculate frequencies.
        4.  Return frequencies.

    3.  DEFINE METHOD: calculate_hydrophobicity(sequence):
        # Calculate and return average hydrophobicity.
        1.  If sequence is empty, return 0.
        2.  Sum hydrophobicity of each amino acid in the sequence.
        3.  Calculate average.
        4.  Return average.

###  DEFINE FUNCTION: read_sequences(filename)--Read and return sequences from a file.
    1.  Read sequences from the file.
    2.  If error, print message and return empty result.
    3.  Return sequences.

###  DEFINE FUNCTION: analyze_sequences(fasta_file, analyzer)--Analyze sequences from a file.
    1.  Read sequences.
    2.  If no sequences, return empty result.
    3.  For each sequence:
        1.  Calculate composition and hydrophobicity.
        2.  Store results.
    4.  Return results.

## PSEUDOCODE FOR SECOND MODULE: visualizations.py

0.  #!/usr/bin/env python3
1.  Import necessary tools (the matplotlib, os, sys, and pandas modules).

###  DEFINE CLASS: DataVisualizer--A blueprint for creating visualizations

    1.  INITIALIZE CLASS: constructor (output_dir):
        # Store the output directory path.

    2.  DEFINE METHOD: save_histogram(data, title, filename):
        # Generate and save a histogram.
        1.  Create a new figure.
        2.  Add a subplot.
        3.  Create a histogram from the data.
        4.  Set the title of the plot.
        5.  Label the x-axis as "Amino Acid Frequency".
        6.  Label the y-axis as "Frequency".
        7.  Save the plot to a file in the output directory.
        8.  Close the figure to free memory.

    3.  DEFINE FUNCTION: save_bar_chart(data, title, filename):
        # Generate and save a bar chart.
        1.  Create a new figure.
        2.  Add a subplot.
        3.  Extract the amino acid names and hydrophobicity values from the data.
        4.  Create a bar chart from the amino acid names and hydrophobicity values.
        5.  Set the title of the plot.
        6.  Label the x-axis as "Amino Acid".
        7.  Label the y-axis as "Average Hydrophobicity".
        8.  Save the plot to a file in the output directory.
        9.  Close the figure to free memory.

    4. DEFINE METHOD: create_hydrophobicity_csv(self, data, top_n=1)
        # Creates a CSV file reporting the average hydrophobicity of each sequence and the sequences with the highest and lowest average hydrophobicity.
        1.  IF the data is empty:
            2.  Print a message and RETURN.
        3.  Convert the input data (list of dictionaries) to a Pandas DataFrame.
        4.  IF the DataFrame does not contain 'name' and 'hydrophobicity' columns:
            5.  Print an error message and RETURN.
        6.  Define the output CSV file name.
        7.  TRY:
            8.  Sort the DataFrame by hydrophobicity in descending order.
            9.  Get the names of the top N sequences.
            10. Get the names of the bottom N sequences.
            11. Create a new DataFrame containing 'name' and 'hydrophobicity' columns.
            12. Add columns for the top N sequences and bottom N sequences (comma-separated).
            13. Save the DataFrame to a CSV file.
            14. Print a success message.
        15. EXCEPT Exception:
            16. Print an error message.


## PSEUDOCODE FOR MAIN SCRIPT: main.py

0.  #!/usr/bin/env python3
1.  Import necessary tools (the argparse, os, sys, and re modules as well as the amino_acid_analysis and visualization modules from the package 'package').
2.  Define the hydrophobicity scale in the form of a dictionary.

###  CLASS: InputValidator--A blueprint to validate input files and directories

    1.  Initialize class: constructor(fasta_file, output_dir):
        # Store file and out put directory paths.

    2.  DEFINE method: validate_fasta_file():
        # Check if FASTA file exists. 
        # If not, display error and stop.

    3.  DEFINE method: validate_output_dir():
        # Check if output directory exists.
        # If not, create it.

###   --- Handle input arguments ---
4.  Get FASTA file and output directory from user input, as well as any optional parameters.
###  ---  End input arguments ---

###   Include a guard statement to ensure that if the script is run directly:
    1.  Create an InputValidator object.
    2.  Validate the FASTA file. If invalid, stop.
    3.  Validate the output directory. Create if needed.
    4.  Create a sequence analyzer.
    5.  Analyze sequences from the FASTA file.
    6.  Create a data visualizer.
    7.  Generate and save histograms of amino acid frequencies.
    8.  Generate and save a bar chart of average hydrophobicity.
    9.  Generate and save a .csv file of average hydrophobicity (according to user parameters if necessary).
    9.  Display the output directory path.

### DISCLAIMER: AI was used to help generate this pseudocode.