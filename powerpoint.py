import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pptx import Presentation

class PresentationGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Presentation Generator")
        self.geometry("600x600")
        self.configure(bg="#f0f0f0")

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
            tk.Label(self, text=label, bg="#f0f0f0").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Entry(self, textvariable=var, width=30).grid(row=row, column=1, padx=10, pady=5)
            row += 1

        # Button to open pptx template
        self.btn_open = ttk.Button(self, text="Select PPTX Template", command=self.open_template)
        self.btn_open.grid(row=row, column=0, padx=10, pady=20, columnspan=2)

        # Button to generate pptx
        self.btn_generate = ttk.Button(self, text="Generate Presentation", command=self.generate_presentation)
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
                        print(f"este es full text: {full_text}")
                       # print(f"este es run text: {run.text}")
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



if __name__ == "__main__":
    app = PresentationGeneratorApp()
    app.mainloop()