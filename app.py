import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import csv
import io
import os
from PIL import Image

# CSV file
DATA_FILE = "data.csv"

# Ensure CSV exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        pass  

def track_expense(category, amount):
    # Validate amount
    try:
        amount = float(amount)
    except:
        return "❌ Please enter a valid number for amount.", None

    # Save expense
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([category, amount])

    # Load CSV
    data = pd.read_csv(DATA_FILE, names=["Category", "Amount"])
    if data.empty:
        return "No expenses yet.", None

    # Summary
    summary = data.groupby("Category").sum().to_string()
    total = data["Amount"].sum()
    summary_text = f"{summary}\nTotal = {total}"

    # Pie chart
    grouped = data.groupby("Category").sum()
    fig, ax = plt.subplots()
    grouped.plot(kind="pie", y="Amount", autopct="%1.1f%%", ax=ax)
    plt.ylabel("")

    # Save to buffer and convert to PIL Image
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    img = Image.open(buf)

    return summary_text, img

# Gradio interface
demo = gr.Interface(
    fn=track_expense,
    inputs=["text", "number"],
    outputs=["text", "image"],
    title="Personal Expense Tracker",
    description="Enter category and amount to track your expenses."
)

demo.launch()

