import json
import pandas as pd

try:
    with open('cleanedResults2.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)  # Load the JSON data

    # Check if the JSON data is a list of dictionaries
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        # Convert to a DataFrame
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        output_csv_path = r"outputdata.csv"  # Replace with your desired output path
        df.to_csv(output_csv_path, index=False)
        print(f"JSON data has been successfully converted to CSV and saved as '{output_csv_path}'.")
    else:
        print("The JSON file does not contain a list of objects.")
except UnicodeDecodeError as e:
    print(f"Error reading the file due to encoding issues: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")