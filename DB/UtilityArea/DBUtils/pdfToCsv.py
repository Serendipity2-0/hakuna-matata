import pdfplumber
import pandas as pd

# Define the path to the PDF file
pdf_path = "Utils/instabiz.pdf"
csv_output_path = "Utils/instabiz_statement.csv"

# Initialize an empty list to store transaction data
data = []

# Extract text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table:
                if row and len(row) >= 7:  # Ensure it has all columns
                    data.append(row[:7])  # Only take the required columns

# Convert the extracted data to a DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "Transaction ID",
        "Value Date",
        "Transaction Date",
        "Transaction Remarks",
        "Withdrawal (Dr)",
        "Deposit (Cr)",
        "Balance",
    ],
)

# Remove empty or header-like rows
df = df.dropna().reset_index(drop=True)

# Save the cleaned data to CSV
df.to_csv(csv_output_path, index=False)

print(f"CSV file saved at: {csv_output_path}")
