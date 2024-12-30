import re
import json

def clean_data(data):
    cleaned_data = []

    for obj in data:
        # Initialize a new dictionary with camelCase keys
        cleaned_obj = {}
        for key, value in obj.items():
            # Convert keys to camelCase
            new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()

            # Handle specific transformations
            if new_key == "price":
                if value and "Prix non spécifié" not in value and value != "N/A":
                    try:
                        cleaned_obj[new_key] = int(value.replace(" ", "").replace("\u202f", "").replace("DH", ""))
                    except ValueError:
                        cleaned_obj[new_key] = None
                else:
                    cleaned_obj[new_key] = None
            elif new_key == "area":
                if value and value != "N/A":
                    try:
                        # Remove 'm²', strip spaces, and convert to int
                        cleaned_obj[new_key] = int(value.replace("m²", "").strip())
                    except ValueError:
                        cleaned_obj[new_key] = None  # Assign None for invalid values
                else:
                    cleaned_obj[new_key] = None
            elif new_key == "time_since":
                if value:
                    cleaned_obj[new_key] = value.replace("il y a", "").strip()
                else:
                    cleaned_obj[new_key] = None
            elif new_key == "type":
                if value:
                    parts = value.split(",")
                    cleaned_obj["category"] = parts[0].strip() if len(parts) > 0 else None
                    cleaned_obj["transaction_type"] = parts[1].strip() if len(parts) > 1 else None
                else:
                    cleaned_obj["category"] = None
                    cleaned_obj["transaction_type"] = None
            else:
                cleaned_obj[new_key] = value

        # Append cleaned object to the list
        cleaned_data.append(cleaned_obj)

    return cleaned_data

# Read data from results.json
with open('partial_results.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Clean the data
cleaned_json = clean_data(json_data)

# Write cleaned data to cleanedResults.json
with open('cleanedResults2.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_json, file, indent=2, ensure_ascii=False)
