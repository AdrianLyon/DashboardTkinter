import customtkinter as ctk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import filedialog, messagebox
from pptx import Presentation

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
            self.barra_superior, text="Generar Constancias", font=ctk.CTkFont(size=30, weight="bold"))
        self.labelTitulo.pack(side=ctk.TOP, fill='both', expand=True, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        self.fields = {
            "Nombre": ctk.StringVar(),
            "CURP": ctk.StringVar(),
            "Categoría": ctk.StringVar(),
            "Curso": ctk.StringVar()
        }

        row = 0
        for label, var in self.fields.items():
            ctk.CTkLabel(self.barra_inferior, text=label).grid(row=row, column=0, sticky=ctk.W, padx=10, pady=5)
            ctk.CTkEntry(self.barra_inferior, textvariable=var, width=250).grid(row=row, column=1, padx=10, pady=5)
            row += 1

        # Botón para abrir la plantilla pptx
        self.btn_open = ctk.CTkButton(self.barra_inferior, text="Select PPTX Template", command=self.open_template)
        self.btn_open.grid(row=row, column=0, padx=10, pady=20, columnspan=2)

        # Botón para generar pptx
        self.btn_generate = ctk.CTkButton(self.barra_inferior, text="Generate Presentation", command=self.generate_presentation)
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
            
            # Replace text in slides with context data, preserving formatting
            for slide in prs.slides:
                for shape in slide.shapes:
                    if not shape.has_text_frame:
                        continue
                    text_frame = shape.text_frame
                    for paragraph in text_frame.paragraphs:
                        full_text = "".join([run.text for run in paragraph.runs])  # Reconstruir el texto completo del párrafo
                        for key, value in context.items():
                            if f"{{{key}}}" in full_text:
                                full_text = full_text.replace(f"{{{key}}}", value)

                        # Actualizar cada run con el nuevo texto
                        current_pos = 0
                        for run in paragraph.runs:
                            run_len = len(run.text)
                            run.text = full_text[current_pos:current_pos + run_len]
                            current_pos += run_len

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

