import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from tkinter import ttk
from pptx import Presentation


class FormularioPptxDesign():

    def __init__(self, panel_principal):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame( panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame( panel_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Página en construcción")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        self.fields = {
            "nombre": tk.StringVar(),
            "curp": tk.StringVar(),
            "categoria": tk.StringVar(),
            "curso": tk.StringVar()
        }

        row = 0
        for label, var in self.fields.items():
            tk.Label(self.barra_inferior, text=label, bg="#f0f0f0").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Entry(self.barra_inferior, textvariable=var, width=30).grid(row=row, column=1, padx=10, pady=5)
            row += 1

        # Button to open pptx template
        self.btn_open = ttk.Button(self.barra_inferior, text="Select PPTX Template", command=self.open_template)
        self.btn_open.grid(row=row, column=0, padx=10, pady=20, columnspan=2)

        # Button to generate pptx
        self.btn_generate = ttk.Button(self.barra_inferior, text="Generate Presentation", command=self.generate_presentation)
        self.btn_generate.grid(row=row+1, column=0, padx=10, pady=10, columnspan=2)

        self.ppt_template = None      

    def open_template(self):
        file_path = filedialog.askopenfilename(
            title="Select PPTX Template",
            filetypes=(("PowerPoint Files", "*.pptx"), ("All Files", "*.*"))
        )
        if file_path:
            self.ppt_template = file_path
            messagebox.showinfo("Template Selected", f"Selected Template: {file_path}")
        else:
            messagebox.showwarning("No File Selected", "Please select a PPTX template to proceed.")

    def generate_presentation(self):
        if not self.ppt_template:
            messagebox.showerror("Error", "Please select a PPTX template before generating the presentation.")
            return

        context = {key.lower().replace(" ", "_"): var.get() for key, var in self.fields.items()}
        
        try:
            # Load the PowerPoint template
            prs = Presentation(self.ppt_template)
            
            # Replace text in slides with context data
            for slide in prs.slides:
                for shape in slide.shapes:
                    if not shape.has_text_frame:
                        continue
                    text = shape.text
                    for key, value in context.items():
                        if f"{{{key}}}" in text:
                            shape.text = text.replace(f"{{{key}}}", value)

            # Save the modified presentation
            output_path = filedialog.asksaveasfilename(
                defaultextension=".pptx",
                filetypes=(("PowerPoint Files", "*.pptx"), ("All Files", "*.*")),
                title="Save Generated Presentation"
            )
            if output_path:
                prs.save(output_path)
                messagebox.showinfo("Success", f"Presentation saved successfully: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")