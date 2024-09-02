import customtkinter as ctk
from formularios.form_maestro_design import FormularioMaestroDesign
from PIL import Image, ImageTk
import tkinter as tk
import json
import os

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
        self.bg_image = self.bg_image.resize((500, 400), Image.Resampling.LANCZOS)
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
        
        # Botón para abrir el formulario de gestión de usuarios
        self.manage_button = ctk.CTkButton(self.login_frame, text="Gestionar Usuarios", command=self.open_user_management)
        self.manage_button.pack(pady=12, padx=10)
        
        # Cargar datos de usuarios
        self.users = self.load_users()

    def load_users(self):
        """Carga los usuarios desde el archivo JSON."""
        if not os.path.exists('data.json'):
            return {}
        with open('data.json', 'r') as file:
            return json.load(file)

    def save_users(self):
        """Guarda los usuarios en el archivo JSON."""
        with open('data.json', 'w') as file:
            json.dump(self.users, file, indent=4)

    def login(self):
        """Verifica las credenciales del usuario."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username] == password:
            self.error_label.configure(text="Login exitoso!", text_color="green")
            # Aquí puedes redirigir al formulario principal
            self.destroy()  # Cierra la ventana de login
            app = FormularioMaestroDesign()  # Inicia la aplicación principal
            app.mainloop()
        else:
            self.error_label.configure(text="Usuario o contraseña incorrectos")

    def open_user_management(self):
        """Abre la ventana de gestión de usuarios."""
        UserManagementForm(self)

# Clase para la gestión de usuarios
class UserManagementForm(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.geometry("400x300")
        
        # Campo de usuario
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nuevo Usuario")
        self.username_entry.pack(pady=12, padx=10)
        
        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Nueva Contraseña", show="*")
        self.password_entry.pack(pady=12, padx=10)
        
        # Botón para agregar usuario
        self.add_button = ctk.CTkButton(self, text="Agregar/Actualizar Usuario", command=self.add_or_update_user)
        self.add_button.pack(pady=12, padx=10)
        
        # Mensaje de resultado
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=12, padx=10)
    
    def add_or_update_user(self):
        """Agrega o actualiza un usuario."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:
            self.master.users[username] = password
            self.master.save_users()
            self.result_label.configure(text="Usuario guardado exitosamente", text_color="green")
        else:
            self.result_label.configure(text="Debe ingresar un usuario y una contraseña", text_color="red")


# Ejecutar la aplicación de login
if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()
