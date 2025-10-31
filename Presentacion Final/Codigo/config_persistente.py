# config_persistente.py
"""
BLOOM MUSIC - CONFIGURACIÓN PERSISTENTE
========================================
Gestiona la ubicación persistente de la base de datos
para que no se pierda al reinstalar
"""

import os
import sys
import json
from pathlib import Path

class ConfigPersistente:
    """Gestiona rutas persistentes para la base de datos"""
    
    def __init__(self):
        self.config_dir = self._obtener_directorio_config()
        self.config_file = os.path.join(self.config_dir, "bloom_config.json")
        self.db_dir = os.path.join(self.config_dir, "database")
        self.db_path = os.path.join(self.db_dir, "Database_Bloom_Music.db")
        
        # Crear directorios si no existen
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.config = self._cargar_config()
    
    def _obtener_directorio_config(self):
        """Obtiene el directorio apropiado según el sistema operativo"""
        if sys.platform == "win32":
            # Windows: usar AppData/Roaming
            base = os.getenv('APPDATA')
            if not base:
                base = os.path.expanduser("~")
            return os.path.join(base, "BloomMusic")
        
        elif sys.platform == "darwin":
            # macOS: usar ~/Library/Application Support
            return os.path.expanduser("~/Library/Application Support/BloomMusic")
        
        else:
            # Linux: usar ~/.config
            return os.path.expanduser("~/.config/BloomMusic")
    
    def _cargar_config(self):
        """Carga la configuración desde el archivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuración por defecto
        return {
            'db_path': self.db_path,
            'primera_ejecucion': True,
            'version': '1.0.0'
        }
    
    def guardar_config(self):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def get_db_path(self):
        """Retorna la ruta de la base de datos"""
        return self.db_path
    
    def marcar_primera_ejecucion_completa(self):
        """Marca que la primera ejecución se completó"""
        self.config['primera_ejecucion'] = False
        self.guardar_config()
    
    def es_primera_ejecucion(self):
        """Verifica si es la primera ejecución"""
        return self.config.get('primera_ejecucion', True)
    
    def db_existe(self):
        """Verifica si la base de datos existe"""
        return os.path.exists(self.db_path)
    
    def importar_db_existente(self, ruta_origen):
        """Importa una base de datos existente"""
        try:
            import shutil
            if os.path.exists(ruta_origen):
                shutil.copy2(ruta_origen, self.db_path)
                print(f"✅ Base de datos importada desde: {ruta_origen}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error importando base de datos: {e}")
            return False
    
    def get_info(self):
        """Retorna información de la configuración"""
        return {
            'config_dir': self.config_dir,
            'db_path': self.db_path,
            'db_existe': self.db_existe(),
            'primera_ejecucion': self.es_primera_ejecucion()
        }


class GestorBaseDatosPersistente:
    """Gestor de base de datos con ubicación persistente"""
    
    def __init__(self):
        self.config = ConfigPersistente()
        self.db_name = self.config.get_db_path()
        
        # Buscar DB existente en el directorio actual
        db_local = "Database_Bloom_Music.db"
        if not self.config.db_existe() and os.path.exists(db_local):
            print(f"📦 Base de datos encontrada en: {db_local}")
            respuesta = input("¿Deseas importar esta base de datos? (s/n): ")
            if respuesta.lower() in ['s', 'si', 'y', 'yes']:
                self.config.importar_db_existente(db_local)
        
        self.inicializar_bd()
        
        if self.config.es_primera_ejecucion():
            print(f"✅ Base de datos creada en: {self.db_name}")
            print(f"📁 Esta ubicación se mantendrá entre instalaciones")
            self.config.marcar_primera_ejecucion_completa()
    
    def inicializar_bd(self):
        """Inicializa la base de datos en la ubicación persistente"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                fecha_registro DATE NOT NULL,
                genero TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Configuraciones (
                id_config INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER UNIQUE NOT NULL,
                volumen REAL DEFAULT 0.70,
                modo_aleatorio INTEGER DEFAULT 0,
                modo_bucle INTEGER DEFAULT 0,
                ultima_playlist TEXT,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
            )
        ''')
        
        # Nueva tabla para playlists personalizadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Playlists (
                id_playlist INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                color TEXT DEFAULT '#B349FF',
                fecha_creacion DATE NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
            )
        ''')
        
        # Nueva tabla para canciones en playlists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PlaylistCanciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_playlist INTEGER NOT NULL,
                ruta_cancion TEXT NOT NULL,
                orden INTEGER DEFAULT 0,
                fecha_agregada DATE NOT NULL,
                FOREIGN KEY (id_playlist) REFERENCES Playlists(id_playlist)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def validar_login(self, nombre, contraseña):
        """Valida credenciales de login"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_usuario, nombre_usuario, email, genero 
            FROM Usuario 
            WHERE nombre_usuario = ? AND contraseña = ?
        """, (nombre, contraseña))
        
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            return {
                'id': usuario[0],
                'nombre': usuario[1],
                'email': usuario[2],
                'genero': usuario[3]
            }
        return None
    
    def registrar_usuario(self, datos):
        """Registra un nuevo usuario"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO Usuario (nombre_usuario, email, contraseña, fecha_registro, genero)
                VALUES (?, ?, ?, ?, ?)
            """, (datos['nombre'], datos['email'], datos['contraseña'], 
                  datos['fecha_nacimiento'], datos['genero']))
            
            id_usuario = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO Configuraciones (id_usuario)
                VALUES (?)
            """, (id_usuario,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def cargar_configuraciones(self, id_usuario):
        """Carga configuraciones del usuario"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT volumen, modo_aleatorio, modo_bucle, ultima_playlist
            FROM Configuraciones
            WHERE id_usuario = ?
        """, (id_usuario,))
        
        config = cursor.fetchone()
        conn.close()
        
        if config:
            playlist = json.loads(config[3]) if config[3] else []
            return {
                'volumen': config[0],
                'modo_aleatorio': bool(config[1]),
                'modo_bucle': config[2],
                'playlist': playlist
            }
        return None
    
    def guardar_configuraciones(self, id_usuario, config):
        """Guarda configuraciones del usuario"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            playlist_json = json.dumps(config['playlist'])
            
            cursor.execute("""
                UPDATE Configuraciones
                SET volumen = ?, modo_aleatorio = ?, modo_bucle = ?, ultima_playlist = ?
                WHERE id_usuario = ?
            """, (config['volumen'], int(config['modo_aleatorio']), 
                  config['modo_bucle'], playlist_json, id_usuario))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error guardando: {e}")
            return False
    
    def actualizar_usuario(self, id_usuario, datos):
        """Actualiza datos del usuario"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Verificar si se debe actualizar la contraseña
            if datos.get('contraseña') and datos['contraseña'].strip():
                cursor.execute("""
                    UPDATE Usuario
                    SET nombre_usuario = ?, email = ?, genero = ?, contraseña = ?
                    WHERE id_usuario = ?
                """, (datos['nombre'], datos['email'], datos['genero'], 
                      datos['contraseña'], id_usuario))
            else:
                cursor.execute("""
                    UPDATE Usuario
                    SET nombre_usuario = ?, email = ?, genero = ?
                    WHERE id_usuario = ?
                """, (datos['nombre'], datos['email'], datos['genero'], id_usuario))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error actualizando usuario: {e}")
            return False
    
    def eliminar_usuario(self, id_usuario):
        """Elimina un usuario y sus datos asociados"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Eliminar configuraciones
            cursor.execute("DELETE FROM Configuraciones WHERE id_usuario = ?", (id_usuario,))
            
            # Eliminar playlists y sus canciones
            cursor.execute("""
                DELETE FROM PlaylistCanciones 
                WHERE id_playlist IN (SELECT id_playlist FROM Playlists WHERE id_usuario = ?)
            """, (id_usuario,))
            
            cursor.execute("DELETE FROM Playlists WHERE id_usuario = ?", (id_usuario,))
            
            # Eliminar usuario
            cursor.execute("DELETE FROM Usuario WHERE id_usuario = ?", (id_usuario,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error eliminando usuario: {e}")
            return False
    
    def crear_playlist(self, id_usuario, nombre, color):
        """Crea una nueva playlist"""
        import sqlite3
        import datetime
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            fecha = datetime.date.today()
            
            cursor.execute("""
                INSERT INTO Playlists (id_usuario, nombre, color, fecha_creacion)
                VALUES (?, ?, ?, ?)
            """, (id_usuario, nombre, color, fecha))
            
            id_playlist = cursor.lastrowid
            
            conn.commit()
            conn.close()
            return id_playlist
        except Exception as e:
            print(f"Error creando playlist: {e}")
            return None
    
    def obtener_playlists_usuario(self, id_usuario):
        """Obtiene todas las playlists del usuario"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_playlist, nombre, color, fecha_creacion
            FROM Playlists
            WHERE id_usuario = ?
            ORDER BY fecha_creacion DESC
        """, (id_usuario,))
        
        playlists = cursor.fetchall()
        conn.close()
        
        return [{'id': p[0], 'nombre': p[1], 'color': p[2], 'fecha': p[3]} for p in playlists]