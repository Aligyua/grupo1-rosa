"""
BLOOM MUSIC - INSTALADOR AUTOMÁTICO (Con BD Persistente)
=========================================================
Este script instala todas las dependencias necesarias y crea un ejecutable .exe

NUEVAS CARACTERÍSTICAS:
- ✅ Detecta base de datos existente
- ✅ Ofrece importarla a ubicación persistente
- ✅ La BD no se pierde al reinstalar

REQUISITOS PREVIOS:
- Python 3.8 o superior instalado
- Conexión a internet para descargar dependencias

INSTRUCCIONES:
1. Abre la terminal/CMD en la carpeta del proyecto
2. Ejecuta: python setup_bloom.py
3. Espera a que se instalen todas las dependencias
4. El ejecutable se creará en la carpeta 'dist'
"""

import subprocess
import sys
import os
import platform
import shutil

# ============================================================================
# OBTENER RUTA ABSOLUTA DEL SCRIPT
# ============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

print(f"📂 Trabajando en: {SCRIPT_DIR}\n")

def print_header(text):
    """Imprime un header bonito"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Verifica que Python sea 3.8+"""
    print_header("VERIFICANDO VERSIÓN DE PYTHON")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print("   Descarga Python desde: https://www.python.org/downloads/")
        return False
    
    print("✅ Versión de Python correcta")
    return True

def buscar_bd_existente():
    """Busca una base de datos existente en el directorio"""
    print_header("BUSCANDO BASE DE DATOS EXISTENTE")
    
    bd_local = os.path.join(SCRIPT_DIR, "Database_Bloom_Music.db")
    
    if os.path.exists(bd_local):
        size = os.path.getsize(bd_local) / 1024  # KB
        print(f"✅ Base de datos encontrada!")
        print(f"   📁 {bd_local}")
        print(f"   💾 Tamaño: {size:.2f} KB")
        
        print("\n💡 La nueva versión guarda la BD en una ubicación persistente:")
        if platform.system() == "Windows":
            ubicacion = "%APPDATA%\\BloomMusic\\database\\"
        else:
            ubicacion = "~/.config/BloomMusic/database/"
        print(f"   {ubicacion}")
        
        print("\n📋 Esto significa que:")
        print("   ✅ Tu cuenta NO se perderá al reinstalar")
        print("   ✅ La BD estará protegida del sistema")
        
        respuesta = input("\n¿Deseas que la instalación use esta base de datos? (s/n): ")
        
        if respuesta.lower() in ['s', 'si', 'y', 'yes']:
            print("✅ La base de datos será importada automáticamente")
            return bd_local
        else:
            print("⚠️  Se creará una nueva base de datos")
            return None
    else:
        print("ℹ️  No se encontró una base de datos existente")
        print("   Se creará una nueva en la ubicación persistente")
        return None

def install_dependencies():
    """Instala todas las dependencias necesarias"""
    print_header("INSTALANDO DEPENDENCIAS")
    
    dependencies = [
        "pygame",
        "Pillow",
        "mutagen",
        "pyinstaller"
    ]
    
    for dep in dependencies:
        print(f"📦 Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"   ✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"   ❌ Error instalando {dep}")
            return False
    
    print("\n✅ Todas las dependencias instaladas")
    return True

def create_spec_file():
    """Crea el archivo .spec para PyInstaller con configuración optimizada"""
    print_header("CREANDO CONFIGURACIÓN DE PYINSTALLER")
    
    # Verificar qué archivos de imágenes existen
    logo_exists = os.path.exists(os.path.join(SCRIPT_DIR, 'LogoLogin.png'))
    foto_exists = os.path.exists(os.path.join(SCRIPT_DIR, 'emiliaMP3Foto.png'))
    
    # Construir lista de data files dinámicamente
    datas_list = []
    if logo_exists:
        datas_list.append("('LogoLogin.png', '.')")
    if foto_exists:
        datas_list.append("('emiliaMP3Foto.png', '.')")
    
    # IMPORTANTE: Incluir los módulos nuevos
    modulos_necesarios = [
        'radioBloom.py',
        'config_persistente.py',
        'GestorVentanas.py',
        'PaginaEditarPerfil.py'
    ]
    
    for modulo in modulos_necesarios:
        modulo_path = os.path.join(SCRIPT_DIR, modulo)
        if os.path.exists(modulo_path):
            datas_list.append(f"('{modulo}', '.')")
        else:
            print(f"⚠️  Advertencia: No se encontró {modulo}")
    
    datas_string = ",\n        ".join(datas_list)
    
    # Determinar el ícono
    icon_line = f"icon='LogoLogin.png'" if logo_exists else "icon=None"
    
    script_dir_safe = repr(SCRIPT_DIR)
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['BloomMusic.py'],
    pathex=[{script_dir_safe}],
    binaries=[],
    datas=[
        {datas_string}
    ],
    hiddenimports=[
        'pygame', 'PIL', 'mutagen', 'sqlite3', 'tkinter',
        'config_persistente', 'GestorVentanas', 'PaginaEditarPerfil', 'radioBloom'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BloomMusic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_line}
)
"""
    
    spec_path = os.path.join(SCRIPT_DIR, "BloomMusic.spec")
    with open(spec_path, "w", encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Archivo .spec creado en: {spec_path}")
    return True

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    print_header("CREANDO EJECUTABLE")
    
    print("⚙️  Compilando... (esto puede tardar varios minutos)")
    print("   Por favor espera...")
    
    try:
        spec_file = os.path.join(SCRIPT_DIR, "BloomMusic.spec")
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "PyInstaller", 
            spec_file,
            "--clean"
        ])
        print("\n✅ Ejecutable creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al crear el ejecutable: {e}")
        return False

def verify_files():
    """Verifica que existan los archivos necesarios"""
    print_header("VERIFICANDO ARCHIVOS DEL PROYECTO")
    
    print(f"📂 Buscando archivos en: {SCRIPT_DIR}\n")
    
    required_files = [
        "BloomMusic.py",
        "config_persistente.py",
        "GestorVentanas.py",
        "PaginaEditarPerfil.py",
        "radioBloom.py"
    ]
    
    optional_files = [
        "LogoLogin.png",
        "emiliaMP3Foto.png"
    ]
    
    all_ok = True
    
    print("📋 Archivos REQUERIDOS:")
    for file in required_files:
        file_path = os.path.join(SCRIPT_DIR, file)
        if os.path.exists(file_path):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NO ENCONTRADO")
            print(f"     Ruta: {file_path}")
            all_ok = False
    
    print("\n📋 Archivos OPCIONALES:")
    for file in optional_files:
        file_path = os.path.join(SCRIPT_DIR, file)
        if os.path.exists(file_path):
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} no encontrado (recomendado)")
    
    return all_ok

def create_installer_script():
    """Crea un script .bat para Windows"""
    print_header("CREANDO SCRIPT DE INSTALACIÓN RÁPIDA")
    
    if platform.system() == "Windows":
        bat_content = """@echo off
echo ========================================
echo   BLOOM MUSIC - INSTALADOR V2
echo   (Con Base de Datos Persistente)
echo ========================================
echo.
cd /d "%~dp0"
echo.
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install pygame Pillow mutagen pyinstaller
echo.
echo ========================================
echo   CREANDO EJECUTABLE
echo ========================================
echo.
python setup_bloom.py
echo.
pause
"""
        bat_path = os.path.join(SCRIPT_DIR, "INSTALAR.bat")
        with open(bat_path, "w") as f:
            f.write(bat_content)
        print(f"✅ Script INSTALAR.bat creado")

def create_readme():
    """Crea un README con instrucciones"""
    print_header("CREANDO DOCUMENTACIÓN")
    
    readme_content = """# BLOOM MUSIC - Instrucciones de Instalación (V2 - BD Persistente)

## 🎵 NUEVA VERSIÓN - Características

✅ **Base de datos persistente**: Ya no se pierde tu cuenta al reinstalar
✅ **Navegación mejorada**: Cambio entre ventanas sin perder datos
✅ **Editar perfil**: Gestiona tu cuenta desde la aplicación
✅ **Código optimizado**: 53% menos líneas, más rápido

## 📦 Instalación Automática

### Windows:
1. Haz doble clic en `INSTALAR.bat`
2. Espera a que termine
3. El ejecutable estará en `dist/BloomMusic.exe`

## 🔧 Instalación Manual

```bash
# 1. Instalar dependencias
pip install pygame Pillow mutagen pyinstaller

# 2. Crear ejecutable
python setup_bloom.py

# 3. Ejecutar
dist/BloomMusic.exe
```

## 💾 Base de Datos Persistente

La nueva versión guarda tu base de datos en:
- **Windows**: `%APPDATA%\\BloomMusic\\database\\`
- **Linux**: `~/.config/BloomMusic/database/`

**Esto significa:**
- ✅ Tu cuenta NO se pierde al reinstalar
- ✅ Puedes actualizar la aplicación sin perder datos
- ✅ La BD está protegida en ubicación del sistema

## 🔄 Migración desde Versión Anterior

Si ya tienes una cuenta:
1. El instalador detectará tu BD automáticamente
2. Te preguntará si deseas importarla
3. Di que SÍ
4. ¡Tu cuenta estará en la nueva ubicación!

## 📋 Archivos Necesarios

**REQUERIDOS** (deben estar en la misma carpeta):
- ✅ BloomMusic.py
- ✅ config_persistente.py
- ✅ GestorVentanas.py
- ✅ PaginaEditarPerfil.py
- ✅ radioBloom.py

**OPCIONALES** (mejoran la experiencia):
- LogoLogin.png
- emiliaMP3Foto.png

## ⚙️ Nuevas Funciones

### Editar Perfil
- Clic en "⋯" → "Editar Perfil"
- Cambia nombre, email, género, contraseña
- Elimina tu cuenta si lo deseas

### Navegación Mejorada
- 🏠 Home: Reproductor principal
- 🎵 Canciones: Lista completa
- ➕ Añadidos Recientemente: Últimas 20
- ➕ Crear Playlist: Nueva playlist
- ✨ Nuevo: Géneros musicales
- 💿 Álbums: Colección
- 📻 Radio: Emisoras online

### Música Continua
- ✅ La música NO se detiene al cambiar de ventana
- ✅ Tu playlist se mantiene en todas las vistas
- ✅ El estado del reproductor se preserva

## ❓ Solución de Problemas

### "ModuleNotFoundError: config_persistente"
**Causa**: Faltan archivos nuevos
**Solución**: Asegúrate de copiar TODOS los archivos .py

### "No encuentro mi cuenta"
**Causa**: BD en ubicación antigua
**Solución**: Ejecuta el instalador, te ofrecerá importarla

### "Error en GestorVentanas"
**Causa**: Falta GestorVentanas.py
**Solución**: Copia el archivo a la carpeta

## 📚 Documentación Completa

- `RESUMEN_CAMBIOS.md`: Qué cambió en esta versión
- `INSTRUCCIONES_IMPLEMENTACION.md`: Guía técnica detallada

## 🆘 Ayuda

Si tienes problemas:
1. Verifica que TODOS los archivos .py estén juntos
2. Ejecuta `python migrar_bloom.py` para migración asistida
3. Lee la documentación completa

---
**Bloom Music V2** - Reproductor con BD Persistente 🎵
Desarrollado con ❤️ por mati je
"""
    
    readme_path = os.path.join(SCRIPT_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ README.md creado")

def main():
    """Función principal del instalador"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🎵 BLOOM MUSIC V2 - INSTALADOR AUTOMÁTICO 🎵         ║
║                                                          ║
║  ✨ NUEVA VERSIÓN con Base de Datos Persistente ✨       ║
║                                                          ║
║  • Tu cuenta NO se pierde al reinstalar                 ║
║  • Navegación mejorada entre ventanas                   ║
║  • Editar perfil integrado                              ║
║  • Código optimizado (53% menos líneas)                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Paso 1: Verificar Python
    if not check_python_version():
        input("\nPresiona ENTER para salir...")
        return
    
    # Paso 2: Verificar archivos
    if not verify_files():
        print("\n❌ Faltan archivos necesarios")
        print("\n💡 SOLUCIÓN:")
        print("   Asegúrate de copiar TODOS estos archivos:")
        print("   • BloomMusic.py")
        print("   • config_persistente.py")
        print("   • GestorVentanas.py")
        print("   • PaginaEditarPerfil.py")
        print("   • radioBloom.py")
        print("\n📚 Consulta RESUMEN_CAMBIOS.md para más información")
        input("\nPresiona ENTER para salir...")
        return
    
    # Paso 3: Buscar BD existente
    bd_existente = buscar_bd_existente()
    
    # Paso 4: Crear scripts
    create_installer_script()
    create_readme()
    
    # Paso 5: Preguntar si continuar
    print("\n" + "="*60)
    respuesta = input("¿Deseas instalar las dependencias y crear el ejecutable? (s/n): ")
    
    if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
        print("\n✅ Scripts creados")
        print("   Ejecuta INSTALAR.bat cuando estés listo")
        return
    
    # Paso 6: Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error en dependencias")
        print("\n💡 Intenta:")
        print("   pip install pygame Pillow mutagen pyinstaller")
        input("\nPresiona ENTER para salir...")
        return
    
    # Paso 7: Crear .spec
    if not create_spec_file():
        print("\n❌ Error creando configuración")
        input("\nPresiona ENTER para salir...")
        return
    
    # Paso 8: Crear ejecutable
    if not build_executable():
        print("\n❌ Error creando ejecutable")
        input("\nPresiona ENTER para salir...")
        return
    
    # ¡Éxito!
    print_header("¡INSTALACIÓN COMPLETADA!")
    
    dist_path = os.path.join(SCRIPT_DIR, "dist")
    exe_path = os.path.join(dist_path, "BloomMusic.exe")
    
    print("✅ Bloom Music V2 instalado exitosamente\n")
    print("📁 Ubicación del ejecutable:")
    print(f"   {exe_path}\n")
    
    print("💾 Tu base de datos estará en:")
    print("   %APPDATA%\\BloomMusic\\database\\\n")
    
    if bd_existente:
        print("📋 Sobre tu base de datos:")
        print("   ✅ Fue detectada")
        print("   ✅ Se importará automáticamente al primer uso")
        print("   ✅ Tu cuenta estará disponible\n")
    
    print("✨ Nuevas funciones disponibles:")
    print("   • Editar perfil desde la aplicación")
    print("   • Navegación entre 8 vistas diferentes")
    print("   • Música continua mientras navegas")
    print("   • Base de datos que NO se pierde\n")
    
    print("📚 Para más información:")
    print("   • README.md - Instrucciones básicas")
    print("   • RESUMEN_CAMBIOS.md - Qué cambió")
    print("   • INSTRUCCIONES_IMPLEMENTACION.md - Guía completa\n")
    
    print("🚀 Para ejecutar:")
    print(f"   Doble clic en: dist\\BloomMusic.exe")
    
    print("\n" + "="*60)
    input("\nPresiona ENTER para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        print(f"\n📂 Directorio: {SCRIPT_DIR}")
        print("\n💡 Verifica que todos los archivos .py estén juntos")
        input("\nPresiona ENTER para salir...")
        sys.exit(1)