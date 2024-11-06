# This is an excel agent which will take the directory of excel file from ui, its explanation from patterns/excelguide.md 
# and output analysis in markdown format,based on user's query.

# Step 1: read the excel file using xlwings and pandas and load it in a dataframe
# Step 2: Generate analysis results using predefined functions like budget, upcoming payments, overdue payments, etc.
# Step 3: Provide output in markdown format along with sheet summary to llm for detailed beautiful markdown report
# Step 4: Ask for user's query and generate response based on the user's query

import os
import subprocess
import dotenv
from openai import OpenAI
import pandas as pd
from swarm import Agent
from pathlib import Path

# Get the directory of the current script
current_dir = Path(__file__).parent.absolute()

# Get the path to the .env file
env_path = Path(current_dir).parent.parent / 'kaas.env'

# Load environment variables from .env file
dotenv.load_dotenv(env_path)


OPENAI_API_KEY = os.getenv("NEW_OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# read the excel file and return the list of sheet names
def read_excel_N_return_sheet_names(directory):
    print(f"Excel file path: {directory}")
    xls = pd.ExcelFile(directory)
    sheet_names = xls.sheet_names
    print(f"Sheet names: {sheet_names}")
    return sheet_names
    
# Function to take list of sheet names and return the sheet dataframe dictionary
def generate_sheet_dataframe_dictionary(directory, sheet_names):
    print("Generating sheet dataframe dictionary")
    sheet_dataframe_dictionary = {}
    for sheet_name in sheet_names:
        sheet_dataframe_dictionary[sheet_name] = pd.read_excel(directory, sheet_name=sheet_name)
    print("Sheet dataframe dictionary created")
    return sheet_dataframe_dictionary

# Analysis functions

# Function to get budget from the 'Accounts(Present)'sheet. Get Sum of 'Balance' column dataframe dictionary
def get_budget(sheet_dataframe_dictionary):
    try:
        accounts_df = sheet_dataframe_dictionary['Accounts(Present)']
        # print all columns of accounts_df
        print(f"accounts_df columns: {accounts_df.columns}")
        if 'Balance' in accounts_df.columns:
            budget = accounts_df['Balance'].sum()
        elif 'Amount' in accounts_df.columns:
            budget = accounts_df['Amount'].sum()
        else:
            budget = "Unable to calculate budget. Required columns not found."
        print(f"budget: {budget}")
        return budget
    except KeyError:
        print("Error: 'Accounts(Present)' sheet not found")
        return "Unable to calculate budget. 'Accounts(Present)' sheet not found."

# Function to get upcoming payments from the 'Freedom(Future)'sheet. Get the list of all payments for next one week from today.
def get_upcoming_payments(sheet_dataframe_dictionary):
    try:
        future_df = sheet_dataframe_dictionary['Freedom(Future)']
        today = pd.Timestamp.now().date()
        next_week = today + pd.Timedelta(days=7)
        upcoming_payments = future_df[(future_df['Date'].dt.date >= today) & (future_df['Date'].dt.date <= next_week)]
        print(f"upcoming_payments: {upcoming_payments}")
        return upcoming_payments
    except KeyError:
        print("Error: 'Freedom(Future)' sheet not found")
        return "Unable to get upcoming payments. 'Freedom(Future)' sheet not found."

# Function to get overdue payments from the 'Freedom(Future)'sheet.
def get_overdue_payments(sheet_dataframe_dictionary):
    try:
        future_df = sheet_dataframe_dictionary['Freedom(Future)']
        today = pd.Timestamp.now().date()
        overdue_payments = future_df[future_df['Date'].dt.date < today]
        print(f"overdue_payments: {overdue_payments}")
        return overdue_payments
    except KeyError:
        print("Error: 'Freedom(Future)' sheet not found")
        return "Unable to get overdue payments. 'Freedom(Future)' sheet not found."

# Function to get 'Category' wise expenses from the 'Transactions(Past)'sheet.
def get_category_wise_expenses(sheet_dataframe_dictionary):
    try:
        transactions_df = sheet_dataframe_dictionary['Transactions(Past)']
        if 'Category' in transactions_df.columns and 'Amount' in transactions_df.columns:
            category_wise_expenses = transactions_df.groupby('Category')['Amount'].sum()
        else:
            category_wise_expenses = "Unable to calculate category-wise expenses. Required columns not found."
        print(f"category_wise_expenses: {category_wise_expenses}")
        return category_wise_expenses
    except KeyError:
        print("Error: 'Transactions(Past)' sheet not found")
        return "Unable to get category-wise expenses. 'Transactions(Past)' sheet not found."

# Function to collate the data and generate the markdown report
def collate_data_and_generate_markdown_report(sheet_dataframe_dictionary):
    budget = get_budget(sheet_dataframe_dictionary)
    upcoming_payments = get_upcoming_payments(sheet_dataframe_dictionary)
    overdue_payments = get_overdue_payments(sheet_dataframe_dictionary)
    category_wise_expenses = get_category_wise_expenses(sheet_dataframe_dictionary)
    
    markdown_report = f"""
                        ## Budget
                        {budget}

                        ## Upcoming Payments
                        {upcoming_payments.to_markdown() if isinstance(upcoming_payments, pd.DataFrame) else upcoming_payments}

                        ## Overdue Payments
                        {overdue_payments.to_markdown() if isinstance(overdue_payments, pd.DataFrame) else overdue_payments}

                        ## Category Wise Expenses
                        {category_wise_expenses.to_markdown() if isinstance(category_wise_expenses, pd.Series) else category_wise_expenses}
                        """
    print("Markdown report generated")
    return markdown_report

# Function to generate the financial analysis report using the markdown report and the guidelines
def generate_financial_analysis_report(markdown_report, guidelines):
    print("Generating financial analysis report")
    financial_analysis_report = generate_completion(
        "Financial Analyst",
        "Use the Financial excel sheet summary and Give a wise analysis using the financial stat report given.",
        f"Generated stats: {markdown_report}\n\nGuidelines: {guidelines}"
    )
    print("Analysis Report generated")
    return financial_analysis_report

# Function to generate completions using OpenAI
def generate_completion(role, task, content):
    print(f"Generating completion for {role}")
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"You are a {role}. {task}"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Fast api will get working directory and guidelines from the user and pass it to this agent
class NikhilRaghuAgent(Agent):
    def run(self, directory, guidelines):
        print(f"working directory: {directory}")
        print(f"guidelines: {guidelines}")
        try:
            sheet_names = read_excel_N_return_sheet_names(directory)
            sheet_dataframe_dictionary = generate_sheet_dataframe_dictionary(directory, sheet_names)
            markdown_report = collate_data_and_generate_markdown_report(sheet_dataframe_dictionary)
            
            if not guidelines:
                with open("patterns/Kaas_Sheets_Summary.md", "r") as file:#TODO: check if this is correct path if yes move it to env file
                    guidelines = file.read()
            
            financial_analysis_report = generate_financial_analysis_report(markdown_report, guidelines)
            print("NikhilRaghuAgent: Completed")
            return financial_analysis_report
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            return error_message
