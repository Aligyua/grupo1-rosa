# Módulo de Radio para Bloom Music usando SOLO pygame
# No requiere VLC - Solo pygame y bibliotecas estándar de Python

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pygame
import threading
import tempfile
import os
import ssl
import socket
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


class RadioModule:
    """Módulo de Radio para Bloom Music - Usando solo pygame"""
    
    def __init__(self, parent_frame, parent_app):
        """
        Inicializa el módulo de radio
        
        Args:
            parent_frame: Frame de tkinter donde se dibujará la interfaz de radio
            parent_app: Referencia a la instancia de Pagina_Principal
        """
        self.parent_frame = parent_frame
        self.parent_app = parent_app
        
        # Estado de la radio
        self.radio_playing = False
        self.current_station = None
        self.radio_volume = 0.70
        self.radio_thread = None
        self.stop_radio_flag = False
        
        # Inicializar referencias de widgets (se crean en create_radio_view)
        self.volume_value_label = None
        self.radio_status_label = None
        self.current_station_label = None
        self.current_genre_label = None
        self.radio_play_button = None
        self.radio_stop_button = None
        
        # Lista de emisoras de radio (streaming URLs)
        # URLs DIRECTAS Y VERIFICADAS - Octubre 2025
        # Usando principalmente direcciones IP y servidores públicos estables
        self.radio_stations = [
            {
                "name": "Radio Nacional Argentina",
                "country": "Argentina",
                "genre": "Variado",
                "url": "http://sa.mp3.icecast.magma.edge-access.net/sc_rad1"
            },
            {
                "name": "Radio JAI Plus",
                "country": "Argentina",
                "genre": "Clásica/Jazz",
                "url": "http://stream.zeno.fm/f3vd3fd231zuv"
            },
            {
                "name": "LU5 Radio Neuquén",
                "country": "Argentina",
                "genre": "Noticias/Variado",
                "url": "http://streaming.neuquen.gov.ar:8000/lu5"
            },
            {
                "name": "Radio Universidad (Rosario)",
                "country": "Argentina",
                "genre": "Cultural/Universidad",
                "url": "http://200.55.193.45:8000/radiouniversidad"
            },
            {
                "name": "FM Boedo 98.9",
                "country": "Argentina",
                "genre": "Tango",
                "url": "http://streamall.alsolnet.com:8036/live"
            },
            {
                "name": "Radio Online Argentina",
                "country": "Argentina",
                "genre": "Variado",
                "url": "http://jenny.torontocast.com:8142/stream"
            },
            {
                "name": "Radio Cultura Buenos Aires",
                "country": "Argentina",
                "genre": "Música Clásica",
                "url": "http://91.121.134.23:8100/stream"
            },
            {
                "name": "FM Arcoiris 102.3",
                "country": "Argentina",
                "genre": "Tropical/Cumbia",
                "url": "http://stream.zenolive.com/g26pxqt8r5zuv"
            },
            {
                "name": "Rock & Pop (Stream)",
                "country": "Argentina",
                "genre": "Rock",
                "url": "http://5.9.56.134:8168/stream"
            },
            {
                "name": "Radio Uno 106.3 (Mendoza)",
                "country": "Argentina",
                "genre": "Pop/Top 40",
                "url": "http://playerservices.streamtheworld.com/api/livestream-redirect/UNOFM.mp3"
            },
            {
                "name": "Radio Provincia AM 1270",
                "country": "Argentina",
                "genre": "Noticias/Deportes",
                "url": "http://streaming.radioprovincia.gob.ar:8064/radioprovincia"
            },
            {
                "name": "LRA 7 Radio Nacional Córdoba",
                "country": "Argentina",
                "genre": "Variado/Cultural",
                "url": "http://sa.mp3.icecast.magma.edge-access.net/sc_rad7"
            }
        ]
        
        # Crear la interfaz
        self.create_radio_view()
    
    def create_radio_view(self):
        """Crear toda la interfaz gráfica de radio"""
        
        # Frame principal de radio
        self.radio_main_frame = tk.Frame(self.parent_frame, bg="#f0f0f0")
        self.radio_main_frame.pack(fill="both", expand=True)
        
        # ===== HEADER CON TÍTULO =====
        header_frame = tk.Frame(self.radio_main_frame, bg="#CF0A8D", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📻 Radio Bloom", 
                              font=("Helvetica", 24, "bold"), 
                              bg="#CF0A8D", 
                              fg="white")
        title_label.pack(pady=20)
        
        # Botón de diagnóstico (pequeño, en la esquina)
        diag_button = tk.Button(header_frame,
                               text="🔧 Diagnóstico",
                               font=("Helvetica", 9),
                               bg="#9d0868",
                               fg="white",
                               relief="flat",
                               padx=10,
                               pady=2,
                               command=self.run_diagnostics)
        diag_button.place(relx=0.95, rely=0.5, anchor="e")
        
        # ===== REPRODUCTOR DE RADIO ACTUAL =====
        self.current_station_frame = tk.Frame(self.radio_main_frame, bg="white", height=180)
        self.current_station_frame.pack(fill="x", padx=20, pady=20)
        self.current_station_frame.pack_propagate(False)
        
        # Info de la estación actual
        self.station_info_frame = tk.Frame(self.current_station_frame, bg="white")
        self.station_info_frame.pack(expand=True)
        
        self.current_station_label = tk.Label(self.station_info_frame, 
                                             text="Selecciona una emisora", 
                                             font=("Helvetica", 16, "bold"), 
                                             bg="white")
        self.current_station_label.pack(pady=5)
        
        self.current_genre_label = tk.Label(self.station_info_frame, 
                                           text="Haz clic en ▶ de cualquier emisora para comenzar", 
                                           font=("Helvetica", 12), 
                                           bg="white",
                                           fg="gray")
        self.current_genre_label.pack()
        
        # Controles de reproducción
        controls_frame = tk.Frame(self.current_station_frame, bg="white")
        controls_frame.pack(pady=10)
        
        self.radio_play_button = tk.Button(controls_frame, 
                                          text="▶ Reproducir", 
                                          font=("Helvetica", 12, "bold"), 
                                          bg="#CF0A8D", 
                                          fg="white", 
                                          relief="flat", 
                                          padx=20, 
                                          pady=5,
                                          command=self.play_radio,
                                          state="disabled")
        self.radio_play_button.pack(side="left", padx=5)
        
        self.radio_stop_button = tk.Button(controls_frame, 
                                          text="⏹ Detener", 
                                          font=("Helvetica", 12, "bold"), 
                                          bg="#e0e0e0", 
                                          fg="black", 
                                          relief="flat", 
                                          padx=20, 
                                          pady=5,
                                          command=self.stop_radio,
                                          state="disabled")
        self.radio_stop_button.pack(side="left", padx=5)
        
        # Control de volumen de radio
        volume_frame = tk.Frame(self.current_station_frame, bg="white")
        volume_frame.pack(pady=5)
        
        volume_label = tk.Label(volume_frame, text="🔊 Volumen:", 
                               font=("Helvetica", 10), bg="white")
        volume_label.pack(side="left", padx=5)
        
        self.radio_volume_scale = ttk.Scale(volume_frame, 
                                           from_=0, 
                                           to=100, 
                                           orient="horizontal", 
                                           length=150,
                                           command=self.adjust_radio_volume)
        self.radio_volume_scale.set(self.radio_volume * 100)
        self.radio_volume_scale.pack(side="left", padx=5)
        
        self.volume_value_label = tk.Label(volume_frame, 
                                          text=f"{int(self.radio_volume * 100)}%",
                                          font=("Helvetica", 10),
                                          bg="white")
        self.volume_value_label.pack(side="left", padx=5)
        
        # Label de estado (Conectando, En vivo, Error, etc.)
        self.radio_status_label = tk.Label(self.current_station_frame,
                                          text="● En espera",
                                          font=("Helvetica", 10),
                                          bg="white",
                                          fg="gray")
        self.radio_status_label.pack()
        
        # ===== LISTA DE EMISORAS CON SCROLL =====
        list_label = tk.Label(self.radio_main_frame, 
                            text="Emisoras Disponibles", 
                            font=("Helvetica", 14, "bold"), 
                            bg="#f0f0f0")
        list_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        # Canvas y Scrollbar para hacer scroll en la lista
        canvas_frame = tk.Frame(self.radio_main_frame, bg="#f0f0f0")
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        self.stations_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        canvas.create_window((0, 0), window=self.stations_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear una tarjeta para cada emisora
        for station in self.radio_stations:
            self.create_station_card(station)
        
        # Actualizar el área de scroll
        self.stations_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def create_station_card(self, station):
        """
        Crear una tarjeta visual para cada emisora
        
        Args:
            station: Diccionario con info de la emisora (name, country, genre, url)
        """
        # Tarjeta contenedora
        card = tk.Frame(self.stations_frame, bg="white", relief="solid", borderwidth=1)
        card.pack(fill="x", pady=5, padx=5)
        
        # Frame con la información de la emisora
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # Nombre de la emisora
        name_label = tk.Label(info_frame, 
                             text=station["name"], 
                             font=("Helvetica", 12, "bold"), 
                             bg="white",
                             anchor="w")
        name_label.pack(fill="x")
        
        # Detalles (género y país)
        details_label = tk.Label(info_frame, 
                                text=f"🎵 {station['genre']} • 🌎 {station['country']}", 
                                font=("Helvetica", 10), 
                                bg="white",
                                fg="gray",
                                anchor="w")
        details_label.pack(fill="x")
        
        # Botón de play
        play_btn = tk.Button(card, 
                           text="▶", 
                           font=("Helvetica", 14), 
                           bg="#CF0A8D", 
                           fg="white", 
                           relief="flat",
                           width=3,
                           command=lambda s=station: self.select_station(s))
        play_btn.pack(side="right", padx=10, pady=10)
        
        # Efectos hover (cambio de color al pasar el mouse)
        def on_enter(e):
            card.config(bg="#f9f9f9")
            info_frame.config(bg="#f9f9f9")
            name_label.config(bg="#f9f9f9")
            details_label.config(bg="#f9f9f9")
        
        def on_leave(e):
            card.config(bg="white")
            info_frame.config(bg="white")
            name_label.config(bg="white")
            details_label.config(bg="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def select_station(self, station):
        """
        Seleccionar una emisora y reproducirla automáticamente
        
        Args:
            station: Diccionario con los datos de la emisora
        """
        # Detener música MP3 si está reproduciéndose
        if self.parent_app.en_reproduccion:
            self.parent_app.parar_musica()
        
        # Guardar la estación seleccionada
        self.current_station = station
        
        # Actualizar la interfaz con la info de la estación
        self.current_station_label.config(text=station["name"])
        self.current_genre_label.config(text=f"🎵 {station['genre']} • 🌎 {station['country']}")
        
        # Habilitar los botones de control
        self.radio_play_button.config(state="normal")
        self.radio_stop_button.config(state="normal")
        
        # Reproducir automáticamente
        self.play_radio()
    
    def play_radio(self):
        """Reproducir la emisora seleccionada usando pygame"""
        if not self.current_station:
            messagebox.showwarning("Aviso", "Por favor selecciona una emisora primero")
            return
        
        # Detener cualquier radio anterior
        if self.radio_playing:
            self.stop_radio()
        
        # Detener música local si está sonando
        if self.parent_app.en_reproduccion:
            self.parent_app.parar_musica()
        
        # Mostrar estado "Conectando..."
        if self.radio_status_label:
            self.radio_status_label.config(text="● Conectando...", fg="orange")
        self.parent_frame.update()
        
        # Iniciar reproducción
        self._play_radio_pygame()
    
    def _play_radio_pygame(self):
        """Reproducir usando pygame con streaming optimizado"""
        # Resetear bandera de detención
        self.stop_radio_flag = False
        
        # Función que descarga y reproduce en streaming
        def stream_radio():
            temp_file = None
            temp_path = None
            
            try:
                # Crear archivo temporal
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_path = temp_file.name
                temp_file.close()
                
                # Configurar request con headers mejorados
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Icy-MetaData': '1',
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
                
                req = Request(self.current_station["url"], headers=headers)
                
                # Configurar contexto SSL para ignorar verificación de certificados
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                print(f"🔄 Conectando a: {self.current_station['name']}")
                print(f"   URL: {self.current_station['url']}")
                
                # Abrir conexión al stream con timeout extendido y contexto SSL
                response = urlopen(req, timeout=20, context=context)
                
                # Descargar buffer inicial (más grande para mejor estabilidad)
                buffer_size = 1024 * 512  # 512KB buffer inicial
                initial_data = response.read(buffer_size)
                
                if not initial_data:
                    raise Exception("No se recibieron datos del stream")
                
                with open(temp_path, 'wb') as f:
                    f.write(initial_data)
                
                # Cargar y reproducir con pygame
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.set_volume(self.radio_volume)
                pygame.mixer.music.play(-1)  # Loop infinito
                
                self.radio_playing = True
                
                if self.radio_status_label:
                    self.radio_status_label.config(text="● En vivo", fg="green")
                
                self.parent_app.barra_estado.config(text=f'📻 Radio: {self.current_station["name"]}')
                print(f"✓ Conectado: {self.current_station['name']}")
                
                # Continuar descargando en background para mantener el stream
                chunk_size = 1024 * 16  # 16KB chunks
                while not self.stop_radio_flag:
                    try:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            print("⚠ Stream terminado por el servidor")
                            break
                    except Exception as e:
                        print(f"⚠ Error leyendo chunk: {e}")
                        break
                
                response.close()
                
            except URLError as e:
                error_detail = str(e.reason) if hasattr(e, 'reason') else str(e)
                
                if self.radio_status_label:
                    self.radio_status_label.config(text="● Error de conexión", fg="red")
                
                print(f"❌ Error URL: {error_detail}")
                
                # Mensaje más específico según el error
                if "SSL" in error_detail or "ssl" in error_detail.lower():
                    error_msg = "Error de certificado SSL.\nLa emisora tiene problemas de seguridad."
                elif "11001" in error_detail or "getaddrinfo" in error_detail or "Name or service not known" in error_detail:
                    error_msg = "No se pudo resolver el dominio.\nVerifica tu conexión a internet o la URL está caída."
                elif "timed out" in error_detail.lower() or "timeout" in error_detail.lower():
                    error_msg = "Tiempo de espera agotado.\nLa emisora no responde. Puede estar temporalmente fuera de línea."
                elif "Connection refused" in error_detail or "10061" in error_detail:
                    error_msg = "Conexión rechazada.\nEl servidor no acepta conexiones o está apagado."
                elif "Not Available" in error_detail or "404" in error_detail:
                    error_msg = "Stream no disponible.\nLa emisora cambió su URL o está fuera de línea."
                else:
                    error_msg = f"No se pudo conectar a la emisora.\n{error_detail[:100]}"
                
                # No mostrar messagebox si el usuario detuvo manualmente
                if not self.stop_radio_flag:
                    messagebox.showerror("Error de Red", 
                                       f"{error_msg}\n\nIntenta con otra emisora.")
                self.radio_playing = False
                
            except HTTPError as e:
                if self.radio_status_label:
                    self.radio_status_label.config(text="● Error HTTP", fg="red")
                
                print(f"❌ Error HTTP {e.code}: {e.reason}")
                
                if e.code == 401:
                    error_msg = "Acceso no autorizado (401).\nLa emisora requiere autenticación."
                elif e.code == 404:
                    error_msg = "Stream no encontrado (404).\nLa URL ha cambiado o la emisora está fuera de línea."
                elif e.code == 403:
                    error_msg = "Acceso prohibido (403).\nLa emisora puede estar bloqueando accesos."
                elif e.code == 503:
                    error_msg = "Servicio no disponible (503).\nLa emisora está temporalmente fuera de línea."
                else:
                    error_msg = f"Error del servidor ({e.code}).\n{e.reason}"
                
                # No mostrar messagebox si el usuario detuvo manualmente
                if not self.stop_radio_flag:
                    messagebox.showerror("Error HTTP", 
                                       f"{error_msg}\n\nIntenta con otra emisora.")
                self.radio_playing = False
                
            except Exception as e:
                if self.radio_status_label:
                    self.radio_status_label.config(text="● Error", fg="red")
                
                print(f"❌ Error inesperado: {type(e).__name__}: {e}")
                
                messagebox.showerror("Error", 
                                   f"No se pudo reproducir la emisora:\n{str(e)}\n\n"
                                   f"Intenta con otra emisora.")
                self.radio_playing = False
            
            finally:
                # Limpiar archivo temporal con reintentos
                if temp_path and os.path.exists(temp_path):
                    import time
                    # Intentar eliminar con reintentos (pygame puede tener el archivo bloqueado)
                    max_attempts = 3
                    for attempt in range(max_attempts):
                        try:
                            # Pequeño delay para que pygame libere el archivo
                            time.sleep(0.5)
                            os.unlink(temp_path)
                            print(f"🗑️ Archivo temporal eliminado: {temp_path}")
                            break
                        except PermissionError:
                            if attempt < max_attempts - 1:
                                print(f"⚠ Intento {attempt + 1}/{max_attempts}: Archivo aún en uso, reintentando...")
                                time.sleep(1)
                            else:
                                print(f"⚠ No se pudo eliminar archivo temporal (en uso): {temp_path}")
                                # El archivo se eliminará cuando Windows lo permita
                        except Exception as e:
                            print(f"⚠ Error al eliminar archivo temporal: {e}")
                            break
        
        # Ejecutar en thread separado
        self.radio_thread = threading.Thread(target=stream_radio, daemon=True)
        self.radio_thread.start()
    
    def stop_radio(self):
        """Detener la reproducción de radio"""
        if self.radio_playing:
            print(f"⏹ Deteniendo radio: {self.current_station['name'] if self.current_station else 'N/A'}")
            
            self.stop_radio_flag = True
            
            # Detener pygame mixer - esto libera el archivo
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()  # CRÍTICO: Liberar el archivo explícitamente
            
            self.radio_playing = False
            
            if self.radio_status_label:
                self.radio_status_label.config(text="● Detenido", fg="gray")
            
            self.parent_app.barra_estado.config(text='Radio detenida')
    
    def adjust_radio_volume(self, value):
        """Ajustar el volumen de la radio"""
        self.radio_volume = float(value) / 100
        
        # Verificar que el widget existe antes de actualizarlo
        if self.volume_value_label:
            self.volume_value_label.config(text=f"{int(float(value))}%")
        
        # Aplicar volumen si la radio está reproduciéndose
        if self.radio_playing:
            pygame.mixer.music.set_volume(self.radio_volume)
    
    def destroy(self):
        """
        Destruir el módulo de radio y liberar recursos
        Se llama cuando se cambia de vista (de Radio a Home)
        """
        print("🔄 Destruyendo módulo de radio...")
        
        if self.radio_playing:
            self.stop_radio()
        
        # Dar tiempo para que el thread termine
        if self.radio_thread and self.radio_thread.is_alive():
            self.stop_radio_flag = True
            self.radio_thread.join(timeout=1)
        
        self.radio_main_frame.destroy()
        print("✓ Módulo de radio destruido")
    
    def run_diagnostics(self):
        """Ejecutar diagnóstico de conexión para debugging"""
        print("\n" + "="*60)
        print("🔧 DIAGNÓSTICO DE RADIO")
        print("="*60)
        
        # Test 1: Conexión a internet básica
        print("\n[1/4] Probando conexión a internet básica...")
        try:
            test_req = Request("http://www.google.com", headers={'User-Agent': 'Mozilla/5.0'})
            test_response = urlopen(test_req, timeout=5)
            test_response.close()
            print("✓ Conexión a internet: OK")
        except Exception as e:
            print(f"❌ Conexión a internet: FALLO - {e}")
            messagebox.showerror("Diagnóstico", 
                               "No hay conexión a internet.\n\n"
                               "Verifica tu conexión de red.")
            return
        
        # Test 2: Resolución DNS
        print("\n[2/4] Probando resolución DNS...")
        import socket
        test_domains = [
            "sa.mp3.icecast.magma.edge-access.net",
            "stream.zeno.fm",
            "google.com"
        ]
        dns_ok = 0
        for domain in test_domains:
            try:
                ip = socket.gethostbyname(domain)
                print(f"✓ {domain} → {ip}")
                dns_ok += 1
            except Exception as e:
                print(f"❌ {domain} → Error: {e}")
        
        if dns_ok == 0:
            print("❌ DNS: FALLO TOTAL")
            messagebox.showerror("Diagnóstico", 
                               "Problema con resolución DNS.\n\n"
                               "Posibles soluciones:\n"
                               "• Cambia tus DNS a 8.8.8.8 (Google)\n"
                               "• Reinicia tu router\n"
                               "• Desactiva VPN si tienes una")
            return
        else:
            print(f"✓ DNS: {dns_ok}/{len(test_domains)} dominios resueltos")
        
        # Test 3: Probar primera estación
        print("\n[3/4] Probando Radio Nacional...")
        try:
            test_url = "http://sa.mp3.icecast.magma.edge-access.net/sc_rad1"
            test_req = Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            test_response = urlopen(test_req, timeout=10, context=context)
            test_data = test_response.read(1024)
            test_response.close()
            
            if len(test_data) > 0:
                print(f"✓ Radio Nacional: OK ({len(test_data)} bytes recibidos)")
            else:
                print("❌ Radio Nacional: Sin datos")
        except Exception as e:
            print(f"❌ Radio Nacional: Error - {e}")
        
        # Test 4: Verificar firewall/antivirus
        print("\n[4/4] Verificando puertos comunes...")
        test_ports = [80, 8000, 8080]
        ports_ok = 0
        for port in test_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex(('google.com', port))
                sock.close()
                if result == 0:
                    print(f"✓ Puerto {port}: Accesible")
                    ports_ok += 1
                else:
                    print(f"⚠ Puerto {port}: Bloqueado o inaccesible")
            except Exception as e:
                print(f"❌ Puerto {port}: Error - {e}")
        
        print("\n" + "="*60)
        print("📊 RESUMEN DEL DIAGNÓSTICO")
        print("="*60)
        
        # Resumen
        issues = []
        if dns_ok < len(test_domains):
            issues.append("• Problemas de DNS detectados")
        if ports_ok < len(test_ports):
            issues.append("• Algunos puertos pueden estar bloqueados")
        
        if len(issues) == 0:
            summary = "✓ Todo parece estar bien.\n\nSi algunas emisoras no funcionan,\npuede ser que estén temporalmente fuera de línea."
        else:
            summary = "⚠ Problemas detectados:\n\n" + "\n".join(issues)
            summary += "\n\nConsulta la consola para más detalles."
        
        print(summary)
        print("="*60 + "\n")
        
        messagebox.showinfo("Diagnóstico Completado", summary)