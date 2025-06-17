import kagglehub
import pandas as pd
import os

# Download latest version
path = kagglehub.dataset_download("utkarshsharma11r/student-mental-health-analysis")

print("Path to dataset files:", path)

csv_path = os.path.join(path, "Student Mental Health Analysis During Online Learning.csv") 
df = pd.read_csv(csv_path)
print(df.head(n=5))