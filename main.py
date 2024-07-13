# preferred order fromLabel, fromAddress, toAddress, toLabel, unitValue, historicalUSD
import pandas as pd
import customtkinter as ctk
from tkinter import ttk, IntVar, messagebox
import locale
# Set locale for USD formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Load the CSV file
file_path = './arkham_txns.csv'
data = pd.read_csv(file_path)

# Print column names for debugging
print("Column names:", data.columns)

# Initialize the main window
app = ctk.CTk()
app.title("Transaction Data Viewer")
app.geometry("1000x600")

# Set the dark theme and configure colors
ctk.set_appearance_mode("dark")

# Define custom colors
background_color = "#1f1f1f"
frame_color = "#2c2c2c"
header_color = "#ff9900"  # Bitcoin orange color
text_color = "#d9d9d9"

# List to keep track of the order of selected columns
selected_columns_order = []

# Function to format USD values
def format_usd(value):
    try:
        return locale.currency(float(value), grouping=True)
    except ValueError:
        return value

# Function to format unitValue to 8 decimal places
def format_unit_value(value):
    try:
        return f"{float(value):.8f}"
    except ValueError:
        return value

# Function to populate the treeview with selected columns
def populate_treeview():
    tree.delete(*tree.get_children())
    tree["columns"] = selected_columns_order
    for col in selected_columns_order:
        tree.heading(str(col), text=str(col), anchor='center')
        tree.column(str(col), width=120, anchor='center')
    for _, row in data[selected_columns_order].iterrows():
        formatted_row = []
        for col, value in zip(selected_columns_order, row):
            if col == "unitValue":
                formatted_row.append(format_unit_value(value))
            elif col == "historicalUSD":
                formatted_row.append(format_usd(value))
                
            else:
                formatted_row.append(value)
        tree.insert("", "end", values=formatted_row)
    

# Create a frame for the treeview
frame = ctk.CTkFrame(app, fg_color=frame_color)
frame.pack(pady=10, padx=10, fill="both", expand=True)

# Create the treeview
style = ttk.Style()
style.configure("Treeview", background=background_color, fieldbackground=background_color, foreground=text_color)
style.configure("Treeview.Heading", background=header_color, foreground="white", font=("Helvetica", 10, "bold"))
tree = ttk.Treeview(frame, show="headings")

# Add scrollbars to the treeview
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
hsb.pack(side='bottom', fill='x')
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tree.pack(fill="both", expand=True)

# Create a scrollable frame for the column selection buttons
button_frame = ctk.CTkScrollableFrame(app, fg_color=frame_color, orientation="horizontal")
button_frame.pack(pady=10, padx=10, fill="x")

# Function to update the columns in the treeview
def update_columns(col):
    if column_vars[col].get() == 1:  # If checkbox is checked
        if col not in selected_columns_order:
            selected_columns_order.append(col)
    else:  # If checkbox is unchecked
        if col in selected_columns_order:
            selected_columns_order.remove(col)
    
    populate_treeview()
    messagebox.showinfo("Column Order", f"Current order: {selected_columns_order}")

# Create IntVars and CheckButtons for each column
column_vars = {}
for col in data.columns:
    var = IntVar()
    check_button = ctk.CTkCheckBox(button_frame, text=str(col), variable=var, onvalue=1, offvalue=0, 
                                   fg_color="#343434", hover_color="#454545", 
                                   command=lambda c=col: update_columns(c))
    check_button.pack(side='left', padx=5, pady=5)
    column_vars[col] = var

# Run the application
app.mainloop()