""" from formularios.form_maestro_design import FormularioMaestroDesign

app = FormularioMaestroDesign()
app.mainloop() 


 """
import customtkinter as ctk
from formularios.form_maestro_design import FormularioMaestroDesign
from PIL import Image, ImageTk
import tkinter as tk

# Clase para el formulario de login
class LoginForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Inicio de Sesión")
        self.geometry("500x400")
        
        # Cargar la imagen de fondo
        image_path = "./imagenes/qhse.jpg"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((500, 400), Image.Resampling.LANCZOS)  # Cambiado a LANCZOS
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Crear un label para la imagen de fondo
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Frame para los elementos de login
        self.login_frame = ctk.CTkFrame(self, width=300, height=300, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título de login
        self.login_label = ctk.CTkLabel(self.login_frame, text="Inicio de Sesión", font=("Arial", 20))
        self.login_label.pack(pady=12, padx=10)
        
        # Campo de usuario
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuario")
        self.username_entry.pack(pady=12, padx=10)
        
        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=12, padx=10)
        
        # Botón de login
        self.login_button = ctk.CTkButton(self.login_frame, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=12, padx=10)
        
        # Mensaje de error (inicialmente oculto)
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.pack(pady=12, padx=10)
        
    def login(self):
        # Lógica para verificar las credenciales del usuario
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "password":  # Aquí deberías verificar con tu sistema de autenticación
            self.error_label.configure(text="Login exitoso!", text_color="green")
            # Aquí puedes redirigir al formulario principal
            self.destroy()  # Cierra la ventana de login
            app = FormularioMaestroDesign()  # Inicia la aplicación principal
            app.mainloop()
        else:
            self.error_label.configure(text="Usuario o contraseña incorrectos")

# Ejecutar la aplicación de login
if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()

