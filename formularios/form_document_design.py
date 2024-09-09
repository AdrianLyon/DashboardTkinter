import customtkinter as ctk
import tkinter as tk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from docxtpl import DocxTemplate

class FormularioDocument():
    
    def __init__(self, panel_principal):
        # Configurar el tema de customtkinter
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        # Crear paneles: barra superior
        self.barra_superior = ctk.CTkFrame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = ctk.CTkFrame(panel_principal)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = ctk.CTkLabel(
            self.barra_superior, text="Generar documentos desde formulario", font=ctk.CTkFont(size=30, weight="bold"))
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True, pady=10)

        # Crear widgets en la barra inferior
        self.create_widgets()

    def create_widgets(self):
        # Diccionario de campos y variables
        self.fields = {
            "Nombre": tk.StringVar(),
            "CURP": tk.StringVar(),
            "Ocupacion": tk.StringVar(),
            "Puesto": tk.StringVar(),
            "Razon": tk.StringVar(),
            "RFC": tk.StringVar(),
            "Nombre Curso": tk.StringVar(),
            "Horas": tk.StringVar(),
            "Inicio de año": tk.StringVar(),
            "Inicio de mes": tk.StringVar(),
            "Inicio de día": tk.StringVar(),
            "Término de año": tk.StringVar(),
            "Término de mes": tk.StringVar(),
            "Término de día": tk.StringVar(),
            "Tematica": tk.StringVar(),
            "Agente": tk.StringVar(),
            "Instructor": tk.StringVar(),
            "Patron": tk.StringVar(),
            "Representante": tk.StringVar()
        }

        # Crear widgets organizados en dos columnas
        row = 0
        column = 0
        for index, (label, var) in enumerate(self.fields.items()):
            tk.Label(self.barra_inferior, text=label, bg="#f0f0f0").grid(row=row, column=column*2, sticky=tk.W, padx=10, pady=5)

            entry = ctk.CTkEntry(self.barra_inferior, textvariable=var, width=200)
            
            # Configurar validaciones específicas
            if label == "Nombre":
                self.add_placeholder(entry, "Empezar con el apellido paterno")  # Añadir placeholder
                entry.bind('<KeyRelease>', lambda e, var=var: var.set(var.get().upper()))

            elif label == "CURP":
                entry.bind('<KeyRelease>', lambda e, var=var: var.set(var.get().upper()))

            elif label in ["Puesto", "Razon", "RFC", "Tematica", "Agente", "Instructor", "Patron", "Representante"]:
                entry.bind('<KeyRelease>', lambda e, var=var: var.set(var.get().upper()))

            elif "año" in label or "mes" in label or "día" in label:
                entry.configure(validate="key", validatecommand=(self.barra_inferior.register(self.only_numbers), '%P'))

            entry.grid(row=row, column=column*2 + 1, padx=10, pady=5)
            
            if column == 1:
                row += 1
                column = 0
            else:
                column += 1

        # Botón para abrir la plantilla docx
        self.btn_open = ctk.CTkButton(self.barra_inferior, text="Seleccionar Template", command=self.open_template)
        self.btn_open.grid(row=row+1, column=0, padx=10, pady=20, columnspan=4)

        # Botón para generar el documento docx
        self.btn_generate = ctk.CTkButton(self.barra_inferior, text="Generar Documento", command=self.generate_document)
        self.btn_generate.grid(row=row+2, column=0, padx=10, pady=10, columnspan=4)

        self.doc_template = None
    
    def add_placeholder(self, entry, placeholder):
        """Añadir placeholder al campo de texto."""
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.add_back_placeholder(entry, placeholder))

    def clear_placeholder(self, entry, placeholder):
        """Eliminar placeholder cuando el campo está enfocado."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_back_placeholder(self, entry, placeholder):
        """Restaurar placeholder si el campo está vacío."""
        if entry.get() == "":
            entry.insert(0, placeholder)

    def open_template(self):
        file_path = filedialog.askopenfilename(
            title="Seleccion el documento con el formato DOCX Template",
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

        # Mapeo de los nombres descriptivos a los nombres de la plantilla
        mapping = {
            "Inicio de año": "iaño",
            "Inicio de mes": "imes",
            "Inicio de día": "idia",
            "Término de año": "taño",
            "Término de mes": "tmes",
            "Término de día": "tdia"
        }

        # Crear el contexto mapeando los nombres correctos para la plantilla
        context = {}
        for key, var in self.fields.items():
            mapped_key = mapping.get(key, key.lower().replace(" ", "_"))
            context[mapped_key] = var.get()

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
                self.clear_form()  # Limpiar el formulario después de guardar el documento
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_form(self):
        """Función para limpiar el formulario."""
        for var in self.fields.values():
            var.set("")  # Limpiar todos los campos

    def only_numbers(self, P):
        """Función para validar que solo se ingresen números en ciertos campos."""
        if P.isdigit() or P == "":
            return True
        return False
