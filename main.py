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
        self.geometry("800x400")  # Mantener el tamaño de la ventana
        
        # Frame principal para la disposición de imagen y formulario
        self.main_frame = ctk.CTkFrame(self, width=800, height=400)
        self.main_frame.grid(sticky="nsew")  # Hacemos que se expanda y ocupe todo el espacio disponible
        self.grid_columnconfigure(0, weight=1)  # Configurar la columna para expandirse

        # Crear un frame para la imagen
        self.image_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Ajustamos para la izquierda

        # Cargar la imagen
        image_path = "./imagenes/qhse.jpg"
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((300, 400), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Crear un label para mostrar la imagen
        self.image_label = tk.Label(self.image_frame, image=self.bg_photo)
        self.image_label.grid(row=0, column=0)

        # Frame para los elementos de login
        self.login_frame = ctk.CTkFrame(self.main_frame, width=300, height=300, corner_radius=15)
        self.login_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")  # Lo ajustamos a la derecha

        # Título de login
        self.login_label = ctk.CTkLabel(self.login_frame, text="Inicio de Sesión", font=("Arial", 20))
        self.login_label.grid(row=0, column=0, pady=12, padx=10)

        # Campo de usuario
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuario")
        self.username_entry.grid(row=1, column=0, pady=12, padx=10)

        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*")
        self.password_entry.grid(row=2, column=0, pady=12, padx=10)

        # Botón de login
        self.login_button = ctk.CTkButton(self.login_frame, text="Iniciar Sesión", command=self.login)
        self.login_button.grid(row=3, column=0, pady=12, padx=10)

        # Mensaje de error (inicialmente oculto)
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.grid(row=4, column=0, pady=12, padx=10)

        # Botón para abrir el formulario de gestión de usuarios
        self.manage_button = ctk.CTkButton(self.login_frame, text="Gestionar Usuarios", command=self.validate_admin_password)
        self.manage_button.grid(row=5, column=0, pady=12, padx=10)

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
            self.destroy()  # Cierra la ventana de login
            app = FormularioMaestroDesign()  # Inicia la aplicación principal
            app.mainloop()
        else:
            self.error_label.configure(text="Usuario o contraseña incorrectos")

    def validate_admin_password(self):
        """Solicita la contraseña de administrador desde el archivo JSON."""
        if "admin" not in self.users:
            self.error_label.configure(text="No existe el usuario administrador", text_color="red")
            return

        # Crear un cuadro de diálogo para pedir la contraseña
        password_prompt = ctk.CTkInputDialog(
            title="Validación de Administrador",
            text="Por favor, ingrese la contraseña de administrador:"
        )
        entered_password = password_prompt.get_input()

        # Validar si la contraseña ingresada coincide con la del usuario admin
        if entered_password == self.users["admin"]:
            self.open_user_management()  # Abre la gestión de usuarios si la contraseña es correcta
        else:
            self.error_label.configure(text="Contraseña de administrador incorrecta", text_color="red")

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
