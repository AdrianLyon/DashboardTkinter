import os
import sys
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
# Nuevo
from formularios.form_graficas_design import FormularioGraficasDesign
from formularios.form_sitio_construccion import FormularioSitioConstruccionDesign
from formularios.form_info_design import FormularioInfoDesign
from formularios.form_document_design import FormularioDocument
from formularios.form_excel_design import FormularioExcelDesign
from formularios.form_pptx_design import FormularioPptxDesign
from formularios.form_excel_pptx_design import BatchPresentationGeneratorApp

def resource_path(relative_path):
    """Obtiene la ruta de acceso al recurso en un ejecutable empaquetado con PyInstaller"""
    try:
        if getattr(sys, 'frozen', False):
            # Ejecutando como un ejecutable empaquetado
            base_path = sys._MEIPASS
        else:
            # Ejecutando desde el código fuente
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error al obtener la ruta del recurso: {e}")
        return None


class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        # Obtener la ruta dinámica de las imágenes
        logo_path = resource_path('imagenes/qhse.jpg')
        if logo_path:
            try:
                self.bg_image = Image.open(logo_path)
                self.bg_image = self.bg_image.resize((560, 136), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(self.bg_image)
            except Exception as e:
                print(f"Error al cargar la imagen de logo desde {logo_path}: {e}")

        profile_path = resource_path('imagenes/profile.png')
        if profile_path:
            try:
                self.bg_image1 = Image.open(profile_path)
                self.bg_image1 = self.bg_image1.resize((100, 100), Image.Resampling.LANCZOS)
                self.perfil = ImageTk.PhotoImage(self.bg_image1)
            except Exception as e:
                print(f"Error al cargar la imagen de perfil desde {profile_path}: {e}")

        
        #sitio_construccion_path = resource_path('../imagenes/sitio_construccion.png')

        # Leer las imágenes usando la ruta dinámica
        #self.logo = util_img.leer_imagen(self.bg_photo)
        #self.perfil = util_img.leer_imagen(profile_path, (100, 100))
        #self.img_sitio_construccion = util_img.leer_imagen(sitio_construccion_path, (200, 200))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Python GUI')
        w, h = 1024, 600        
        util_ventana.centrar_ventana(self, w, h)        

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
        self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
        self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="QHSE Auditores")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de información
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Administrador")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
         
        # Etiqueta de perfil
        # self.labelPerfil = tk.Label(
        # self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        # self.labelPerfil.pack(side=tk.TOP, pady=10)  
        self.labelPerfil = tk.Label(
        self.menu_lateral,  bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)  

        # Botones del menú lateral
        self.buttonDashBoard = tk.Button(self.menu_lateral)        
        self.buttonProfile = tk.Button(self.menu_lateral)        
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)        
        self.buttonSettings = tk.Button(self.menu_lateral)
        self.buttoneSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", "\uf109", self.buttonDashBoard, self.abrir_panel_graficas),
            ("Documentos", "\uf1c2", self.buttonProfile, self.abrir_panel_document),
            ("Documentos Excel", "\uf1c3", self.buttonPicture, self.abrir_panel_excel),
            ("Constancias", "\uf1c4", self.buttonSettings, self.abrir_panel_pptx),
            ("Constancias Excel", "\uf1c4", self.buttoneSettings, self.abrir_panel_excel_pptx)
        ]

        for text, icon, button, comando in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu, comando)
    
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                         bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)        
  
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command=comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def abrir_panel_graficas(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioGraficasDesign(self.cuerpo_principal)   
    
    def abrir_panel_en_construccion(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioSitioConstruccionDesign(self.cuerpo_principal, self.img_sitio_construccion) 
    
    def abrir_panel_document(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioDocument(self.cuerpo_principal)

    def abrir_panel_excel(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioExcelDesign(self.cuerpo_principal)
    
    def abrir_panel_pptx(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioPptxDesign(self.cuerpo_principal)

    def abrir_panel_excel_pptx(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        BatchPresentationGeneratorApp(self.cuerpo_principal)

    def abrir_panel_info(self):           
        FormularioInfoDesign()                    

    def limpiar_panel(self, panel):
        # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()
