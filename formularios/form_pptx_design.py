import os
import time
import customtkinter as ctk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from pptx import Presentation
from pptx_replace import replace_text
import comtypes.client

class FormularioPptxDesign():

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
            self.barra_superior, text="Generar Constancias desde formulario", font=ctk.CTkFont(size=30, weight="bold"))
        self.labelTitulo.pack(side=ctk.TOP, fill='both', expand=True, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        self.fields = {
            "Nombre": ctk.StringVar(),
            "CURP": ctk.StringVar(),
            "Categoria": ctk.StringVar(),
            "Curso": ctk.StringVar(),
            "folio": ctk.StringVar()
        }

        row = 0
        for label, var in self.fields.items():
            ctk.CTkLabel(self.barra_inferior, text=label).grid(row=row, column=0, sticky=ctk.W, padx=10, pady=5)
            entry = ctk.CTkEntry(self.barra_inferior, textvariable=var, width=250)

            # Configurar validaciones específicas
            if label == "Nombre":
                self.add_placeholder(entry, "debes empezar con el apellido")  # Añadir placeholder
                entry.bind('<KeyRelease>', lambda e, var=var: var.set(var.get().upper()))
            else:
                # Convertir el texto a mayúsculas mientras se escribe
                entry.bind('<KeyRelease>', lambda e, var=var: var.set(var.get().upper()))

            entry.grid(row=row, column=1, padx=10, pady=5)
            row += 1

        # Botón para abrir la plantilla pptx
        self.btn_open = ctk.CTkButton(self.barra_inferior, text="Select PPTX Template", command=self.open_template)
        self.btn_open.grid(row=row, column=0, padx=10, pady=20, columnspan=2)

        # Botón para generar pptx
        self.btn_generate = ctk.CTkButton(self.barra_inferior, text="Generate Presentation", command=self.generate_presentation)
        self.btn_generate.grid(row=row+1, column=0, padx=10, pady=10, columnspan=2)

        self.ppt_template = None

    def add_placeholder(self, entry, placeholder):
        """Añadir placeholder al campo de texto."""
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.add_back_placeholder(entry, placeholder))

    def clear_placeholder(self, entry, placeholder):
        """Eliminar placeholder cuando el campo está enfocado."""
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)

    def add_back_placeholder(self, entry, placeholder):
        """Restaurar placeholder si el campo está vacío."""
        if entry.get() == "":
            entry.insert(0, placeholder)

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

        # Generar el contexto, asegurándonos de que todas las entradas sean cadenas de texto
        context = {key.lower().replace(" ", "_"): str(var.get()) for key, var in self.fields.items()}
        
        try:
            prs = Presentation(self.ppt_template)

            # Reemplazar el texto en las diapositivas
            for key, value in context.items():
                replace_text(prs, f"{{{key}}}", value)

            # Guardar la presentación modificada en .pptx
            output_path_pptx = filedialog.asksaveasfilename(
                defaultextension=".pptx",
                filetypes=(("PowerPoint Files", "*.pptx"), ("All Files", "*.*")),
                title="Save Generated Presentation"
            )
            if output_path_pptx:
                prs.save(output_path_pptx)
                messagebox.showinfo("Success", f"Presentation saved successfully: {output_path_pptx}")
                time.sleep(2)
                self.convert_to_pdf(output_path_pptx)  # Llamar al método para convertir a PDF
                self.clear_form()  # Limpiar el formulario después de guardar
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def convert_to_pdf(self, pptx_path):
        """Convertir la presentación pptx a PDF."""
        try:
            # Cerrar cualquier instancia anterior de PowerPoint que pudiera estar abierta
            powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
            powerpoint.Visible = 1

            # Normaliza la ruta (por si acaso hay problemas con las barras)
            #pptx_path = pptx_path.replace("\\", "/")
            pptx_path = os.path.normpath(pptx_path)  # Convertir la ruta a formato correcto para Windows
            print(pptx_path)

            # Abre la presentación
            presentation = powerpoint.Presentations.Open(pptx_path)

            print(presentation)
            # Generar ruta para PDF
            pdf_path = pptx_path.replace(".pptx", ".pdf")

            # Guardar como PDF (32 indica el formato PDF)
            presentation.SaveAs(pdf_path, 32)

            # Cierra la presentación y PowerPoint
            presentation.Close()
            powerpoint.Quit()

            messagebox.showinfo("Success", f"PDF saved successfully: {pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while converting to PDF: {str(e)}")

    def clear_form(self):
        """Función para limpiar el formulario."""
        for var in self.fields.values():
            var.set("")  # Limpiar todos los campos