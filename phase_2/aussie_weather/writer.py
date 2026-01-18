"""
File Writer Module

Functions for writing weather data and statistics to files.
"""


def write_summary_to_file(df, output_file):
    """
    Write a summary of the weather data to a text file.

    Args:
        df (pandas.DataFrame): The weather DataFrame to summarize.
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'w') as file:
        file.write("=== Weather Data Summary ===\n\n")
        file.write(f"Total records: {len(df)}\n\n")
        file.write(f"Columns: {list(df.columns)}\n\n")
        file.write("Statistical Summary:\n")
        file.write(df.describe().to_string())

