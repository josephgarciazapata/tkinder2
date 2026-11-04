import random
import customtkinter as ctk
from sistema_urgencias import SistemaUrgencias
from main import generar_datos
from arbol import ArbolPacientes
from grafo import GrafoHospital

ctk.set_appearance_mode("Light")

class InterfazUrgencias(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Integrado Hospitalario - Panel de Control")
        self.geometry("1150x780")
        
        self.bg_color = "#E8F0F8"
        self.card_color = "#FFFFFF"
        self.accent_color = "#5A8BBA"
        self.text_main = "#1E2A38"
        self.text_muted = "#758796"
        self.btn_color = "#D4E4F7"
        self.btn_hover = "#B8D0EB"
        
        self.colores_triage = {
            1: "#D9534F",
            2: "#F0AD4E",
            3: "#FCD04B",
            4: "#5CB85C",
            5: "#5BC0DE"
        }
        
        self.configure(fg_color=self.bg_color)
        
        self.servicios = ["Urgencias", "Observacion", "Cirugia", "Rayos X", "UCI"]
        self.sistema = SistemaUrgencias(self.servicios, n_consultorios=1)
        self.arbol = ArbolPacientes()
        self.grafo = GrafoHospital()
        self._inicializar_grafo()
        
        self.pacientes_recepcion = []
        
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(1, weight=1)
        
        self._crear_widgets()

    def _inicializar_grafo(self):
        for s in self.servicios:
            self.grafo.agregar_servicio(s)
        self.grafo.agregar_conexion("Urgencias", "Observacion")
        self.grafo.agregar_conexion("Urgencias", "Rayos X")
        self.grafo.agregar_conexion("Observacion", "Cirugia")
        self.grafo.agregar_conexion("Rayos X", "Cirugia")
        self.grafo.agregar_conexion("Cirugia", "UCI")

    def _crear_widgets(self):
        header = ctk.CTkFrame(self, fg_color=self.accent_color, corner_radius=0, height=75)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lbl_title = ctk.CTkLabel(
            header, text="Plataforma de Gestion Medica y Triage", 
            font=("Segoe UI", 26, "bold"), text_color="#FFFFFF"
        )
        lbl_title.place(relx=0.03, rely=0.35, anchor="w")
        
        lbl_subtitle = ctk.CTkLabel(
            header, text="Modulo Integrado de Admisiones, Arbol BST y Rutas de Traslado", 
            font=("Segoe UI", 12), text_color="#E8F0F8"
        )
        lbl_subtitle.place(relx=0.03, rely=0.70, anchor="w")

        panel_izquierdo = ctk.CTkFrame(
            self, fg_color=self.card_color, corner_radius=12, 
            border_width=1, border_color="#D1D9E0"
        )
        panel_izquierdo.grid(row=1, column=0, sticky="nsew", padx=(25, 12), pady=25)
        
        lbl_ctrl = ctk.CTkLabel(
            panel_izquierdo, text="Comandos del Sistema", 
            font=("Segoe UI", 16, "bold"), text_color=self.accent_color
        )
        lbl_ctrl.pack(anchor="w", padx=20, pady=(20, 15))
        
        frame_botones = ctk.CTkFrame(panel_izquierdo, fg_color="transparent")
        frame_botones.pack(fill="x", padx=20)
        
        estilo_btn = {
            "font": ("Segoe UI", 13, "bold"), 
            "height": 42, 
            "corner_radius": 6,
            "text_color": self.text_main
        }
        
        self.btn_generar = ctk.CTkButton(
            frame_botones, text="1. Registrar Nuevo Lote", 
            command=self.generar_llegadas, fg_color=self.btn_color, 
            hover_color=self.btn_hover, **estilo_btn
        )
        self.btn_generar.pack(fill="x", pady=6)
        
        self.btn_clasificar = ctk.CTkButton(
            frame_botones, text="2. Ejecutar Algoritmo Triage", state="disabled",
            command=self.clasificar_triage, fg_color="#FDE3B3", 
            hover_color="#F7CA79", **estilo_btn
        )
        self.btn_clasificar.pack(fill="x", pady=6)

        self.btn_atender = ctk.CTkButton(
            frame_botones, text="3. Procesar y Trazar Ruta", state="disabled",
            command=self.atender_paciente, fg_color="#C8E6C9", 
            hover_color="#A5D6A7", **estilo_btn
        )
        self.btn_atender.pack(fill="x", pady=6)
        
        self.frame_ruta = ctk.CTkFrame(
            panel_izquierdo, fg_color=self.bg_color, corner_radius=8, 
            border_width=1, border_color="#D1D9E0"
        )
        self.frame_ruta.pack(fill="x", padx=20, pady=25)
        
        self.lbl_ruta_title = ctk.CTkLabel(
            self.frame_ruta, text="Logistica de Traslado", 
            font=("Segoe UI", 13, "bold"), text_color=self.text_muted
        )
        self.lbl_ruta_title.pack(pady=(15, 5))
        
        self.lbl_ruta_val = ctk.CTkLabel(
            self.frame_ruta, text="Sistema en espera...", 
            font=("Segoe UI", 15, "bold"), text_color=self.accent_color, wraplength=320
        )
        self.lbl_ruta_val.pack(pady=(0, 20), padx=20)
        
        lbl_consola = ctk.CTkLabel(
            panel_izquierdo, text="Monitor de Registros", 
            font=("Segoe UI", 14, "bold"), text_color=self.accent_color
        )
        lbl_consola.pack(anchor="w", padx=20, pady=(0, 5))

        self.consola = ctk.CTkTextbox(
            panel_izquierdo, font=("Consolas", 12), fg_color="#1E2A38", 
            text_color="#F8FAFC", corner_radius=8, border_spacing=10
        )
        self.consola.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.consola.tag_config("INFO", foreground="#5BC0DE")
        self.consola.tag_config("ACCION", foreground="#5CB85C")
        self.consola.tag_config("WARN", foreground="#F0AD4E")
        self.consola.tag_config("TRASLADO", foreground="#C69AE5")
        self.consola.tag_config("VERIFICACION", foreground="#A0B2C6")

        panel_derecho = ctk.CTkFrame(
            self, fg_color=self.card_color, corner_radius=12, 
            border_width=1, border_color="#D1D9E0"
        )
        panel_derecho.grid(row=1, column=1, sticky="nsew", padx=(12, 25), pady=25)
        
        lbl_wait = ctk.CTkLabel(
            panel_derecho, text="Monitor de Pacientes Activos", 
            font=("Segoe UI", 16, "bold"), text_color=self.accent_color
        )
        lbl_wait.pack(anchor="w", padx=25, pady=(20, 15))
        
        self.scroll_espera = ctk.CTkScrollableFrame(
            panel_derecho, fg_color="transparent"
        )
        self.scroll_espera.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def log(self, msj):
        self.consola.configure(state="normal")
        
        tag = None
        if msj.startswith("INFO:"):
            tag = "INFO"
        elif msj.startswith("ACCION:"):
            tag = "ACCION"
        elif msj.startswith("WARN:"):
            tag = "WARN"
        elif msj.startswith("TRASLADO:"):
            tag = "TRASLADO"
        elif msj.startswith("VERIFICACION:"):
            tag = "VERIFICACION"
            
        self.consola.insert("end", msj + "\n", tag)
        self.consola.see("end")
        self.consola.configure(state="disabled")

    def _formatear_hora(self, minutos_totales):
        horas = minutos_totales // 60
        minutos = minutos_totales % 60
        return f"{horas:02d}:{minutos:02d}"

    def _renderizar_lista(self, pacientes, ordenado=False):
        for widget in self.scroll_espera.winfo_children():
            widget.destroy()
            
        if ordenado:
            pacientes.sort(key=lambda p: (p.triage, p.hora_llegada))
            
        for p in pacientes:
            color_t = self.colores_triage.get(p.triage, self.text_muted)
            
            tarjeta = ctk.CTkFrame(
                self.scroll_espera, fg_color=self.bg_color, 
                corner_radius=8, height=60, border_width=1, border_color="#E0E7ED"
            )
            tarjeta.pack(fill="x", pady=6, padx=10)
            
            hora_fmt = self._formatear_hora(p.hora_llegada)
            info_texto = f"Doc: {p.documento}   |   Ingreso: {hora_fmt}"
            
            lbl_info = ctk.CTkLabel(
                tarjeta, text=info_texto, font=("Segoe UI", 15, "bold"), text_color=self.text_main
            )
            lbl_info.pack(side="left", padx=20, pady=18)
            
            estado_texto = f"Triage {p.triage}" if ordenado else "Por Evaluar"
            color_estado = color_t if ordenado else self.text_muted
            
            lbl_triage = ctk.CTkLabel(
                tarjeta, text=estado_texto, 
                font=("Segoe UI", 15, "bold"), text_color=color_estado
            )
            lbl_triage.pack(side="right", padx=20)

    def generar_llegadas(self):
        censo, _ = generar_datos(8, semilla=random.randint(1, 10000))
        
        nuevos_pacientes = [censo[i] for i in range(len(censo))]
        self.pacientes_recepcion.extend(nuevos_pacientes)
        
        self._renderizar_lista(self.pacientes_recepcion, ordenado=False)
        
        self.log(f"INFO: {len(censo)} pacientes ingresados en recepcion. Pendientes de clasificacion: {len(self.pacientes_recepcion)}")
        self.btn_clasificar.configure(state="normal")

    def clasificar_triage(self):
        for p in self.pacientes_recepcion:
            self.sistema.registrar_llegada(p)
            self.arbol.insertar(p)
            
        self.pacientes_recepcion = []
        
        pacientes_esperando = []
        for i in range(len(self.sistema.espera._heap)):
            pacientes_esperando.append(self.sistema.espera._heap[i][2])
            
        self._renderizar_lista(pacientes_esperando, ordenado=True)
        
        self.log("INFO: Triage procesado. Pacientes estructurados en ColaPrioridad e indexados en BST.")
        self.btn_clasificar.configure(state="disabled")
        self.btn_atender.configure(state="normal")

    def atender_paciente(self):
        paciente = self.sistema.llamar_a_consultorio(0)
        
        if paciente:
            self.sistema.atender(0)
            self.sistema.admitir(paciente, "Urgencias")
            
            pacientes_esperando = []
            for i in range(len(self.sistema.espera._heap)):
                pacientes_esperando.append(self.sistema.espera._heap[i][2])
            self._renderizar_lista(pacientes_esperando, ordenado=True)
            
            destinos = {1: "UCI", 2: "Cirugia", 3: "Observacion", 4: "Rayos X", 5: "Rayos X"}
            destino_final = destinos.get(paciente.triage, "Observacion")
            
            camino = self.grafo.camino_mas_corto("Urgencias", destino_final)
            if camino:
                lista_camino = [camino[i] for i in range(len(camino))]
                ruta_texto = " -> ".join(lista_camino)
            else:
                ruta_texto = "Ruta no disponible"
            
            self.lbl_ruta_title.configure(text=f"Asignacion Logistica: Doc {paciente.documento}")
            self.lbl_ruta_val.configure(text=ruta_texto)
            
            self.log(f"ACCION: Paciente Doc: {paciente.documento} evaluado clinicamente.")
            self.log(f"TRASLADO: Urgencias -> {destino_final}")
            
            if self.arbol.buscar(paciente.documento):
                self.log("VERIFICACION: Indexacion BST validada y estable.")
        else:
            self.log("WARN: No se detectan pacientes en la estructura de espera.")
            self.btn_atender.configure(state="disabled")

if __name__ == "__main__":
    app = InterfazUrgencias()
    app.mainloop()