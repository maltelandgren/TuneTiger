import pandas as pd
import json

# Define the file path
file_path = "data/JSONL/pianoBig_max_300_events_val.jsonl"

# Initialize lists to store the data
concepts = []
descriptions = []

# Open the JSONL file and extract the relevant data
with open(file_path, 'r') as file:
    for line in file:
        data = json.loads(line)
        concept = data.get("request", "")
        description = data.get("response", "")
        concepts.append(concept)
        descriptions.append(description)

# Create a DataFrame
df = pd.DataFrame({'Concept': concepts, 'Description': descriptions})

# Combine the 'Concept' and 'Description' columns into 'Text'
df['text'] = df.apply(lambda row: f"###Human:\n{row['Concept']}\n\n###Assistant:\n{row['Description']} ", axis=1)

# Drop the 'Concept' and 'Description' columns if you don't need them anymore
#df.drop(['Concept', 'Description'], axis=1, inplace=True)

# Save the DataFrame to a CSV file
df.to_csv('val.csv', index=False)

# Display the DataFrame (optional)
print(df)