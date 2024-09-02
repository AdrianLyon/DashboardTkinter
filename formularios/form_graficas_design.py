""" import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FormularioGraficasDesign():

    def __init__(self, panel_principal):           
        
        Label = tk.Label(master=panel_principal, 
                        text= "QHSE AUDITORES S.C. es una empresa especializada en desarrollar \n Programas de Mejora Continua, ya sea de un área en particular, \n un departamento o en todos los procesos de su organización. Nuestro objetivo es generar \n competencia calificada a todo el personal involucrado en el despliegue del programa \n instruyendo en la metodología Lean Six Sigma para la correcta ejecución de sus \n etapas PDCA (Plan-Do-Check-Act); a su vez, formar a cada participante  \n con el conocimiento, experiencia y habilidades  para poder aspirar a las \n certificaciones como Yellow Belt, Green Belt y Black Belt.",
                        font=('FontAwesome', 11)
                        ).pack(padx=20, pady=20) """


import customtkinter as ctk

class FormularioGraficasDesign():

    def __init__(self, panel_principal):           
        
        # Crear un Label moderno utilizando customtkinter
        label_text = ("QHSE AUDITORES S.C. es una empresa especializada en desarrollar \n"
                      "Programas de Mejora Continua, ya sea de un área en particular, \n"
                      "un departamento o en todos los procesos de su organización. Nuestro objetivo es generar \n"
                      "competencia calificada a todo el personal involucrado en el despliegue del programa \n"
                      "instruyendo en la metodología Lean Six Sigma para la correcta ejecución de sus \n"
                      "etapas PDCA (Plan-Do-Check-Act); a su vez, formar a cada participante  \n"
                      "con el conocimiento, experiencia y habilidades  para poder aspirar a las \n"
                      "certificaciones como Yellow Belt, Green Belt y Black Belt.")
        
        label = ctk.CTkLabel(master=panel_principal, 
                             text=label_text,
                             font=('Roboto', 12),
                             fg_color="transparent",  # Fondo transparente para que se integre mejor
                             text_color="#2B2B2B",    # Color de texto más oscuro para mejor legibilidad
                             width=400,               # Ancho del Label
                             height=200,              # Alto del Label
                             corner_radius=10,        # Esquinas redondeadas
                             anchor="center")         # Texto centrado
        label.pack(padx=20, pady=20)
