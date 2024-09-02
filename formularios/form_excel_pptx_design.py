import customtkinter as ctk
from config import  COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from tkinter import ttk
from pptx import Presentation
import pandas as pd


class BatchPresentationGeneratorApp():

    def __init__(self, panel_principal):
        # Configurar el tema de customtkinter
        ctk.set_appearance_mode("Light")  # Opciones: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

        # Crear paneles: barra superior
        self.barra_superior = ctk.CTkFrame( panel_principal)
        self.barra_superior.pack(side=ctk.TOP, fill=ctk.X, expand=False)

        # Crear paneles: barra inferior
        self.barra_inferior = ctk.CTkFrame(panel_principal)
        self.barra_inferior.pack(side=ctk.BOTTOM, fill='both', expand=True)  

         # Primer Label con texto
        self.labelTitulo = ctk.CTkLabel(
            self.barra_superior, text="Generar Constancias", font=ctk.CTkFont(size=30, weight="bold"))
        self.labelTitulo.pack(side=ctk.TOP, fill='both', expand=True, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Buttons to open pptx template and excel file
        self.btn_open_pptx = ctk.CTkButton(self.barra_inferior, text="Select PPTX Template", command=self.open_pptx_template)
        self.btn_open_pptx.grid(row=0, column=0, padx=10, pady=20, columnspan=2)

        self.btn_open_excel = ctk.CTkButton(self.barra_inferior, text="Select Excel File", command=self.open_excel_file)
        self.btn_open_excel.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Button to generate presentations
        self.btn_generate = ctk.CTkButton(self.barra_inferior, text="Generate Presentations", command=self.generate_presentations)
        self.btn_generate.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.pptx_template = None
        self.excel_file = None

    def open_pptx_template(self):
        file_path = filedialog.askopenfilename(
            title="Select PPTX Template",
            filetypes=(("PowerPoint Files", "*.pptx"), ("All Files", "*.*"))
        )
        if file_path:
            self.pptx_template = file_path
            messagebox.showinfo("Template Selected", f"Selected Template: {file_path}")
        else:
            messagebox.showwarning("No File Selected", "Please select a PPTX template to proceed.")

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

    def generate_presentations(self):
        if not self.pptx_template:
            messagebox.showerror("Error", "Please select a PPTX template before generating the presentations.")
            return
        if not self.excel_file:
            messagebox.showerror("Error", "Please select an Excel file before generating the presentations.")
            return

        try:
            df = pd.read_excel(self.excel_file)
            for index, row in df.iterrows():
                prs = Presentation(self.pptx_template)
                
                context = {
                    'nombre': row['nombre'],
                    'curp': row['curp'],
                    'categoria': row['categoria'],
                    'curso': row['curso']
                }

                # Replace text in slides with context data
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if not shape.has_text_frame:
                            continue
                        text_frame = shape.text_frame
                        for paragraph in text_frame.paragraphs:
                            full_text = "".join([run.text for run in paragraph.runs])
                            for key, value in context.items():
                                if f"{{{key}}}" in full_text:
                                    full_text = full_text.replace(f"{{{key}}}", value)

                            # Update each run with the new text
                            current_pos = 0
                            for run in paragraph.runs:
                                run_len = len(run.text)
                                run.text = full_text[current_pos:current_pos + run_len]
                                current_pos += run_len

                output_path = f"generated_presentation_{index}.pptx"
                prs.save(output_path)

            messagebox.showinfo("Success", "Presentations generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")