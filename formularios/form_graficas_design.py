import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FormularioGraficasDesign():

    def __init__(self, panel_principal):           
        
        Label = tk.Label(master=panel_principal, 
                        text= "QHSE AUDITORES S.C. es una empresa especializada en desarrollar \n Programas de Mejora Continua, ya sea de un área en particular, \n un departamento o en todos los procesos de su organización. Nuestro objetivo es generar \n competencia calificada a todo el personal involucrado en el despliegue del programa \n instruyendo en la metodología Lean Six Sigma para la correcta ejecución de sus \n etapas PDCA (Plan-Do-Check-Act); a su vez, formar a cada participante  \n con el conocimiento, experiencia y habilidades  para poder aspirar a las \n certificaciones como Yellow Belt, Green Belt y Black Belt.",
                        font=('FontAwesome', 11)
                        ).pack(padx=20, pady=20)

