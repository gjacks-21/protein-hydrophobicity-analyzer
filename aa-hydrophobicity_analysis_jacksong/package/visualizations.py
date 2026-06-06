"""

Protein Sequence Visualization Module (Python 3)

This Python 3 module provides tools for visualizing amino acid composition and 
average hydrophobicity of protein sequences. It defines a DataVisualizer class 
that generates histograms for amino acid frequencies, bar charts of average 
hydrophobicity, and a CSV report highlighting the sequences with the highest 
and lowest hydrophobicity values.

Key Features:
- Generates per-amino-acid frequency histograms for all sequences.
- Creates a bar chart of average hydrophobicity per sequence.
- Outputs a CSV file summarizing hydrophobicity values and ranking sequences.
- Automatically creates the output directory if it doesn't exist.

"""
import matplotlib.pyplot as plt
import os
import sys  # Import sys
import pandas as pd # Import pandas

class DataVisualizer:
    """
    Class to generate visualizations
    """
    def __init__(self, output_dir):
        """
        Constructor for the DataVisualizer class
        Initializes the visualizer with the output directory.

        Args:
            output_dir (str): The path to the output directory.
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except OSError as e:
                print(f"Error creating output directory: {e}")
                sys.exit(1) # Exit if directory cannot be created

    def generate_histograms(self, data):
        """
        Generates histograms showing the frequency of each amino acid.

        Args:
            data (list): A list of dictionaries, where each dictionary contains:
                {'name': sequence_name, 'composition': aa_composition, 'hydrophobicity': avg_hydrophobicity}.
        """
        if not data:
            print("No data provided to generate histograms.")
            return

        # Use pandas DataFrame for easier data manipulation
        df = pd.DataFrame([
            {**{'name': d['name']}, **d['composition']} for d in data
        ]).set_index('name').fillna(0)

        for amino_acid in df.columns:
            plt.figure(figsize=(8, 6))
            plt.hist(df[amino_acid], bins=10, edgecolor='black')
            plt.title(f"Frequency of Amino Acid {amino_acid}")
            plt.xlabel("Frequency")
            plt.ylabel("Count")
            plt.grid(True)
            plt.tight_layout()
            filename = os.path.join(self.output_dir, f"aa_frequency_{amino_acid}.png")
            try:
                plt.savefig(filename)
            except Exception as e:
                print(f"Error saving histogram for {amino_acid}: {e}")
            plt.close()

    def generate_bar_chart(self, data, top_n=1):
        """
        Generates a bar chart showing the average hydrophobicity of each sequence.

        Args:
            data (list): A list of dictionaries, where each dictionary contains:
                {'name': sequence_name, 'composition': aa_composition, 'hydrophobicity': avg_hydrophobicity}.
        """
        if not data:
            print("No data provided to generate bar chart.")
            return

        # Use pandas DataFrame for easier data manipulation
        df = pd.DataFrame(data)

        plt.figure(figsize=(10, 6))
        plt.bar(df['name'], df['hydrophobicity'], color='skyblue')
        plt.title("Average Hydrophobicity of Sequences")
        plt.xlabel("Sequence Name")
        plt.ylabel("Average Hydrophobicity")
        plt.xticks(rotation=45, ha="right")

        # Add the hydrophobicity values to the bars
        for i, hydrophobicity in enumerate(df['hydrophobicity']):
            plt.text(i, hydrophobicity, f"{hydrophobicity:.2f}", ha='center', va='bottom')  # Display value above each bar
            
        plt.tight_layout()
        filename = os.path.join(self.output_dir, "average_hydrophobicity.png")
        try:
            plt.savefig(filename)
        except Exception as e:
            print(f"Error saving bar chart: {e}")
        plt.close()
        self.create_hydrophobicity_csv(data, top_n)

    def create_hydrophobicity_csv(self, data, top_n=1):
        """
        Creates a CSV file reporting the average hydrophobicity of each sequence
        and indicating the sequences with the highest and lowest average
        hydrophobicity.

        Args:
            data (list):  A list of dictionaries, where each dictionary contains:
                {'name': sequence_name, 'composition': aa_composition, 'hydrophobicity': avg_hydrophobicity}.
            top_n (int, optional): The number of top and bottom sequences to report. Defaults to 1.
        """
        if not data:
            print("No data provided to create CSV.")
            return

        # Convert the input data (list of dicts) to a DataFrame.
        df = pd.DataFrame(data)

        if 'name' not in df.columns or 'hydrophobicity' not in df.columns:
            print(
                "Error: DataFrame must contain 'name' and 'hydrophobicity' columns to"
                " create the CSV file."
            )
            return

        outfile_name = os.path.join(
            self.output_dir, "average_hydrophobicity.csv")  # More specific name
        try:
            # Sort the dataframe by hydrophobicity
            sorted_df = df.sort_values(by='hydrophobicity', ascending=False)

            # Get the top N sequences
            top_n_sequences = sorted_df.head(top_n)['name'].tolist()
            # Get the bottom N sequences
            bottom_n_sequences = sorted_df.tail(top_n)['name'].tolist()

            # Create a new DataFrame for the CSV output
            csv_df = df[['name', 'hydrophobicity']].copy()  # Create a copy
            csv_df[f'top_{top_n}_sequence(s)'] = ', '.join(top_n_sequences)
            csv_df[f'bottom_{top_n}_sequence(s)'] = ', '.join(bottom_n_sequences)

            # Save to CSV
            csv_df.to_csv(outfile_name, index=False)
            #print(f"CSV file created successfully: {outfile_name}")
        except Exception as e:
            print(f"Error creating CSV file: {e}")
