import customtkinter as ctk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from tkinter import ttk
from pptx import Presentation
import pandas as pd
import os
from pptx_replace import replace_text
import comtypes.client
import comtypes.stream

class BatchPresentationGeneratorApp():

    def __init__(self, panel_principal):
        # Configurar el tema de customtkinter
        ctk.set_appearance_mode("Light")  # Opciones: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

        # Crear paneles: barra superior
        self.barra_superior = ctk.CTkFrame(panel_principal)
        self.barra_superior.pack(side=ctk.TOP, fill=ctk.X, expand=False)

        # Crear paneles: barra inferior
        self.barra_inferior = ctk.CTkFrame(panel_principal)
        self.barra_inferior.pack(side=ctk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = ctk.CTkLabel(
            self.barra_superior, text="Generar Constancias desde un archivo Excel", font=ctk.CTkFont(size=30, weight="bold"))
        self.labelTitulo.pack(side=ctk.TOP, fill='both', expand=True, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Buttons to open pptx template and excel file
        self.btn_open_pptx = ctk.CTkButton(self.barra_inferior, text="Seleccionar el archivo powerpoint", command=self.open_pptx_template)
        self.btn_open_pptx.grid(row=0, column=0, padx=10, pady=20, columnspan=2)

        self.btn_open_excel = ctk.CTkButton(self.barra_inferior, text="Seleccionar el archivo Excel", command=self.open_excel_file)
        self.btn_open_excel.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Button to generate presentations
        self.btn_generate = ctk.CTkButton(self.barra_inferior, text="Generar Presentacion", command=self.generate_presentations)
        self.btn_generate.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.pptx_template = None
        self.excel_file = None

    def open_pptx_template(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo power point",
            filetypes=(("PowerPoint Files", "*.pptx"), ("All Files", "*.*"))
        )
        if file_path:
            self.pptx_template = file_path
            messagebox.showinfo("Template Selected", f"Selected Template: {file_path}")
        else:
            messagebox.showwarning("No File Selected", "Please select a PPTX template to proceed.")

    def open_excel_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar el archivo excel",
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

        # Permitir al usuario seleccionar la carpeta de destino
        output_folder = filedialog.askdirectory(title="Select Folder to Save Presentations")
        if not output_folder:
            messagebox.showerror("Error", "No folder selected. Please select a folder to save the presentations.")
            return

        try:
            df = pd.read_excel(self.excel_file)
            for index, row in df.iterrows():
                prs = Presentation(self.pptx_template)
                
                context = {
                    'nombre': row['nombre'],
                    'curp': row['curp'],
                    'categoria': row['categoria'],
                    'curso': row['curso'],
                    'folio': row['folio'],
                    'horas': str(row['horas']),
                    'dias': str(row['dias']),
                    'mes': row['mes'],
                    'año': str(row['año'])
                }

                # Replace text in slides with context data
                # Reemplazar el texto en las diapositivas
                for key, value in context.items():
                    replace_text(prs, f"{{{key}}}", value)

                # Construir la ruta completa del archivo de salida
                output_path_pptx = os.path.join(output_folder, f"{row['nombre']}_{index}.pptx")
                prs.save(output_path_pptx)
                self.convert_to_pdf(output_path_pptx)

            messagebox.showinfo("Success", "Presentacion generada correctamente.!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def convert_to_pdf(self, pptx_path):
        """Convertir la presentación pptx a PDF."""
        try:
            # Cerrar cualquier instancia anterior de PowerPoint que pudiera estar abierta
            powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
            powerpoint.Visible = 1

            # Normaliza la ruta
            pptx_path = os.path.normpath(pptx_path)
            print(pptx_path)

            # Abre la presentación
            presentation = powerpoint.Presentations.Open(pptx_path)

            # Generar ruta para PDF
            pdf_path = pptx_path.replace(".pptx", ".pdf")

            # Guardar como PDF (32 indica el formato PDF)
            presentation.SaveAs(pdf_path, 32)

            # Cierra la presentación y PowerPoint
            presentation.Close()
            powerpoint.Quit()

            #messagebox.showinfo("Success", f"PDF saved successfully: {pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while converting to PDF: {str(e)}")
