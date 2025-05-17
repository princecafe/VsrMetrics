import os
import json

json_folder = "D:/Users/CY/Desktop/Diffusion_Model/udm10/vmaf_results"

total_sum = 0
count = 0

for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        json_path = os.path.join(json_folder, filename)
        try:
            with open(json_path, "r") as file:
                data = json.load(file)
                vmaf_average = data["global"]["vmaf"]["vmaf"]["average"]
                total_sum += vmaf_average
                count += 1
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error processing file {filename}: {e}")

if count > 0:
    average = total_sum / count
    print(f"Average vmaf.average value: {average:.4f}")
else:
    print("No valid JSON files found or error in processing files.")