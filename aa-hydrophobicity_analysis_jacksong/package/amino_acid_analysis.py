"""
Amino Acid Sequence Analysis Module (Python 3)

This Python 3 module provides tools to analyze protein sequences from a FASTA file using Biopython.
It includes functionality for calculating amino acid composition and average hydrophobicity
based on the Kyte-Doolittle scale.

Key Features:
- Calculates normalized amino acid composition.
- Computes average hydrophobicity of sequences.
- Reads FASTA files using Biopython's SeqIO.
- Supports integration into larger bioinformatics pipelines.

DISCLAIMER: AI tools were used to help develop this script.

"""
import sys  # Import the sys module
from Bio import SeqIO # Import SeqIO from Biopython

class SequenceAnalyzer:
    """
    Class to analyze amino acid sequences
    """
    def __init__(self, hydrophobicity_scale):
        """
        Constructor for the SequenceAnalyzer class
        Initializes the analyzer with the given hydrophobicity scale.

        Args:
            hydrophobicity_scale (dict): A dictionary mapping amino acids to their hydrophobicity values.
        """
        self.hydrophobicity_scale = hydrophobicity_scale

    def calculate_aa_composition(self, sequence):
        """
        Calculates the amino acid composition of a sequence.

        Args:
            sequence (str): The amino acid sequence string.

        Returns:
            dict: A dictionary where keys are amino acids and values are their frequencies.
                  Returns an empty dictionary if the sequence is empty or contains invalid amino acids.
        """
        composition = {}
        total_aa_count = 0

        if not sequence:  # Handle empty sequence
            return {}

        for aa in sequence:
            if aa.upper() in self.hydrophobicity_scale:  # Consider only standard amino acids
                if aa.upper() in composition:
                    composition[aa.upper()] += 1
                else:
                    composition[aa.upper()] = 1
                total_aa_count += 1

        if total_aa_count == 0:
            return {}  # Return empty dict if no valid amino acids

        # Use a list comprehension for the frequency calculation
        composition = {aa: count / total_aa_count for aa, count in composition.items()}

        return composition

    def calculate_average_hydrophobicity(self, sequence):
        """
        Calculates the average hydrophobicity of an amino acid sequence.

        Args:
            sequence (str): The amino acid sequence string.

        Returns:
            float: The average hydrophobicity value. Returns 0.0 if the sequence is empty
                   or contains no valid amino acids.
        """
        total_hydrophobicity = 0
        valid_aa_count = 0

        if not sequence:
            return 0.0

        for aa in sequence:
            if aa.upper() in self.hydrophobicity_scale:
                total_hydrophobicity += self.hydrophobicity_scale[aa.upper()]
                valid_aa_count += 1

        if valid_aa_count > 0:
            return total_hydrophobicity / valid_aa_count
        else:
            return 0.0


def read_fasta_file(filename):
    """
    Reads a FASTA file and returns a list of sequences using Biopython's SeqIO.

    Args:
        filename (str): The path to the FASTA file.

    Returns:
        list: A list of tuples, where each tuple contains (sequence_name, sequence_string).
              Returns an empty list if the file is empty or an error occurs.
    """
    sequences = []
    try:
        for record in SeqIO.parse(filename, "fasta"):
            sequences.append((record.id, str(record.seq)))
    except FileNotFoundError:
        print(f"Error: FASTA file not found at {filename}")
        return []
    except Exception as e:
        print(f"Error reading FASTA file with Biopython: {e}")
        return []
    return sequences

def analyze_sequences(fasta_file, analyzer):
    """
    Analyzes amino acid sequences from a FASTA file using a SequenceAnalyzer object.

    Args:
        fasta_file (str): The path to the FASTA file.
        analyzer (SequenceAnalyzer): An instance of the SequenceAnalyzer class.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
            {'name': sequence_name, 'composition': aa_composition, 'hydrophobicity': avg_hydrophobicity}.
            Returns an empty list if no sequences are found or an error occurs.
    """
    sequences = read_fasta_file(fasta_file)
    if not sequences:
        return []  # Return empty list if no sequences were read

    results = []
    for sequence_name, sequence_string in sequences:
        try:
            aa_composition = analyzer.calculate_aa_composition(sequence_string)
            avg_hydrophobicity = analyzer.calculate_average_hydrophobicity(sequence_string)
            results.append({
                'name': sequence_name,
                'composition': aa_composition,
                'hydrophobicity': avg_hydrophobicity
            })
        except Exception as e:
            print(f"Error analyzing sequence {sequence_name}: {e}")
            # Consider whether to continue processing other sequences or stop.
            # Here, we continue to process other sequences, but log the error.
    return results