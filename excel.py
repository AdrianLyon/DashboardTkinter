import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from docxtpl import DocxTemplate
import pandas as pd

class BatchDocumentGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batch Document Generator")
        self.geometry("600x300")
        self.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        # Buttons to open docx template and excel file
        self.btn_open_docx = ttk.Button(self, text="Select DOCX Template", command=self.open_docx_template)
        self.btn_open_docx.grid(row=0, column=0, padx=10, pady=20, columnspan=2)

        self.btn_open_excel = ttk.Button(self, text="Select Excel File", command=self.open_excel_file)
        self.btn_open_excel.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Button to generate documents
        self.btn_generate = ttk.Button(self, text="Generate Documents", command=self.generate_documents)
        self.btn_generate.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.doc_template = None
        self.excel_file = None

    def open_docx_template(self):
        file_path = filedialog.askopenfilename(
            title="Select DOCX Template",
            filetypes=(("Word Documents", "*.docx"), ("All Files", "*.*"))
        )
        if file_path:
            self.doc_template = file_path
            messagebox.showinfo("Template Selected", f"Selected Template: {file_path}")
        else:
            messagebox.showwarning("No File Selected", "Please select a DOCX template to proceed.")

    def open_excel_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=(("Excel Files", "*.xlsx"), ("All Files", "*.*"))
        )
        if file_path:
            self.excel_file = file_path
            messagebox.showinfo("Excel File Selected", f"Selected Excel File: {file_path}")
        else:
            messagebox.showwarning("No File Selected", "Please select an Excel file to proceed.")

    def generate_documents(self):
        if not self.doc_template:
            messagebox.showerror("Error", "Please select a DOCX template before generating the documents.")
            return
        if not self.excel_file:
            messagebox.showerror("Error", "Please select an Excel file before generating the documents.")
            return

        try:
            df = pd.read_excel(self.excel_file)
            doc = DocxTemplate(self.doc_template)

            for index, row in df.iterrows():
                context = {
                    'name_work': row['name'],
                    'curp': row['curp'],
                    'ocupation': row['ocupation'],
                    'job': row['job'],
                    'razon': row['razon'],
                    'rfc': row['rfc'],
                    'name_curso': row['name_curso'],
                    'hour': row['hour'],
                    'ini_year': row['iyear'],
                    'i_m': row['imonth'],
                    'ini_d': row['iday'],
                    'te_day': row['tyear'],
                    'te_m': row['tmonth'],
                    'te_d': row['tday'],
                    'tematica': row['tematica'],
                    'agent_name': row['agent'],
                    'instructor': row['ins'],
                    'patron': row['pa'],
                    'representante': row['re']
                }

                doc.render(context)
                output_path = f"generated_doc_{index}.docx"
                doc.save(output_path)

            messagebox.showinfo("Success", "Documents generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = BatchDocumentGeneratorApp()
    app.mainloop()