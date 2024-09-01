import tkinter as tk
from config import  COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from tkinter import ttk
from docxtpl import DocxTemplate


class FormularioDocument():
    
    def __init__(self, panel_principal):
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Generador de documentos")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Crear widgets en la barra inferior
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        self.fields = {
            "Name Work": tk.StringVar(),
            "CURP": tk.StringVar(),
            "Ocupation": tk.StringVar(),
            "Job": tk.StringVar(),
            "Razon": tk.StringVar(),
            "RFC": tk.StringVar(),
            "Name Curso": tk.StringVar(),
            "Hours": tk.StringVar(),
            "Start Year": tk.StringVar(),
            "Start Month": tk.StringVar(),
            "Start Day": tk.StringVar(),
            "End Year": tk.StringVar(),
            "End Month": tk.StringVar(),
            "End Day": tk.StringVar(),
            "Tematica": tk.StringVar(),
            "Agent Name": tk.StringVar(),
            "Instructor": tk.StringVar(),
            "Patron": tk.StringVar(),
            "Representante": tk.StringVar()
        }

        row = 0
        for label, var in self.fields.items():
            tk.Label(self.barra_inferior, text=label, bg="#f0f0f0").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Entry(self.barra_inferior, textvariable=var, width=30).grid(row=row, column=1, padx=10, pady=5)
            row += 1

        # Botón para abrir la plantilla docx
        self.btn_open = ttk.Button(self.barra_inferior, text="Select Template", command=self.open_template)
        self.btn_open.grid(row=row, column=0, padx=10, pady=20, columnspan=2)

        # Botón para generar el documento docx
        self.btn_generate = ttk.Button(self.barra_inferior, text="Generate Document", command=self.generate_document)
        self.btn_generate.grid(row=row+1, column=0, padx=10, pady=10, columnspan=2)

        self.doc_template = None
    
    def open_template(self):
        file_path = filedialog.askopenfilename(
            title="Select DOCX Template",
            filetypes=(("Word Documents", "*.docx"), ("All Files", "*.*"))
        )
        if file_path:
            self.doc_template = file_path
            messagebox.showinfo("Template Selected", f"Selected Template: {file_path}")
        else:
            messagebox.showwarning("No File Selected", "Please select a DOCX template to proceed.")

    def generate_document(self):
        if not self.doc_template:
            messagebox.showerror("Error", "Please select a DOCX template before generating the document.")
            return

        context = {key.lower().replace(" ", "_"): var.get() for key, var in self.fields.items()}
        
        try:
            doc = DocxTemplate(self.doc_template)
            doc.render(context)
            output_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=(("Word Documents", "*.docx"), ("All Files", "*.*")),
                title="Save Generated Document"
            )
            if output_path:
                doc.save(output_path)
                messagebox.showinfo("Success", f"Document saved successfully: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
