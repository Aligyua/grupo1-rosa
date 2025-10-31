#!/usr/bin/env python3
"""
BLOOM MUSIC V2 - INSTALADOR PARA LINUX (Con BD Persistente)
============================================================
Compatible con Python 3.13+ y PEP 668

NUEVAS CARACTERÍSTICAS:
- ✅ Base de datos persistente (no se pierde al reinstalar)
- ✅ Detecta e importa BD existente automáticamente
- ✅ Sistema modular de navegación
- ✅ Editar perfil integrado

REQUISITOS:
- Python 3.8+
- python3-venv, python3-full
- Conexión a internet
"""

import subprocess
import sys
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

VENV_DIR = os.path.join(SCRIPT_DIR, "venv_bloom")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

print(f"📂 Trabajando en: {SCRIPT_DIR}\n")

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    print_header("VERIFICANDO VERSIÓN DE PYTHON")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8+")
        print("   sudo apt install python3 python3-pip python3-venv")
        return False
    
    if version.major == 3 and version.minor >= 13:
        print(f"ℹ️  Python {version.major}.{version.minor} - Usará entorno virtual (PEP 668)")
    
    print("✅ Versión correcta")
    return True

def check_venv_support():
    print_header("VERIFICANDO SOPORTE DE ENTORNO VIRTUAL")
    try:
        import venv
        print("✅ Módulo venv disponible")
        return True
    except ImportError:
        print("❌ Módulo venv no encontrado")
        print("\n💡 Instálalo:")
        print("   sudo apt install python3-venv python3-full")
        return False

def buscar_bd_existente():
    """Busca una base de datos existente"""
    print_header("BUSCANDO BASE DE DATOS EXISTENTE")
    
    bd_local = os.path.join(SCRIPT_DIR, "Database_Bloom_Music.db")
    
    if os.path.exists(bd_local):
        size = os.path.getsize(bd_local) / 1024
        print(f"✅ Base de datos encontrada!")
        print(f"   📁 {bd_local}")
        print(f"   💾 Tamaño: {size:.2f} KB")
        
        print("\n💡 La nueva versión guarda la BD en:")
        print("   ~/.config/BloomMusic/database/")
        
        print("\n📋 Beneficios:")
        print("   ✅ Tu cuenta NO se pierde al reinstalar")
        print("   ✅ BD protegida en ubicación del sistema")
        
        respuesta = input("\n¿Usar esta base de datos? (s/n): ")
        
        if respuesta.lower() in ['s', 'si', 'y', 'yes']:
            print("✅ Se importará automáticamente")
            return bd_local
        else:
            print("⚠️  Se creará una nueva BD")
            return None
    else:
        print("ℹ️  No se encontró BD existente")
        print("   Se creará una nueva en ubicación persistente")
        return None

def create_virtual_environment():
    print_header("CREANDO ENTORNO VIRTUAL")
    
    if os.path.exists(VENV_DIR):
        print(f"ℹ️  Entorno virtual existe: {VENV_DIR}")
        response = input("¿Recrearlo? (s/n): ")
        if response.lower() in ['s', 'si', 'y', 'yes']:
            print("🗑️  Eliminando anterior...")
            shutil.rmtree(VENV_DIR)
        else:
            print("✅ Usando existente")
            return True
    
    print(f"🔧 Creando en: {VENV_DIR}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("✅ Entorno virtual creado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Instala python3-venv:")
        print("   sudo apt install python3-venv python3-full")
        return False

def check_system_dependencies():
    print_header("VERIFICANDO DEPENDENCIAS DEL SISTEMA")
    print("ℹ️  Pygame requiere librerías del sistema\n")
    
    try:
        result = subprocess.run(['which', 'apt'], capture_output=True)
        has_apt = result.returncode == 0
    except:
        has_apt = False
    
    if has_apt:
        print("🔍 Sistema Debian/Ubuntu detectado")
        response = input("\n¿Instalar dependencias del sistema? (s/n): ")
        
        if response.lower() in ['s', 'si', 'y', 'yes']:
            packages = [
                'python3-dev', 'python3-venv', 'python3-full',
                'libsdl2-dev', 'libsdl2-mixer-dev', 'libsdl2-image-dev',
                'libsdl2-ttf-dev', 'libfreetype6-dev', 'build-essential'
            ]
            
            print("\n📦 Instalando...")
            try:
                cmd = ['sudo', 'apt', 'install', '-y'] + packages
                subprocess.check_call(cmd)
                print("✅ Dependencias instaladas")
            except:
                print("⚠️  Algunas dependencias fallaron")
        else:
            print("\n⚠️  Saltando instalación de sistema")
    
    return True

def install_dependencies():
    print_header("INSTALANDO DEPENDENCIAS DE PYTHON")
    
    if not os.path.exists(VENV_PYTHON):
        print("❌ Entorno virtual no encontrado")
        return False
    
    print("🔄 Actualizando pip...")
    try:
        subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL)
        print("✅ pip actualizado\n")
    except:
        print("⚠️  No se pudo actualizar pip\n")
    
    dependencies = ["pygame", "Pillow", "mutagen", "pyinstaller"]
    
    for dep in dependencies:
        print(f"📦 Instalando {dep}...")
        try:
            subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", dep])
            print(f"   ✅ {dep} instalado")
        except:
            print(f"   ❌ Error con {dep}")
            if dep == "pygame":
                print("   💡 Instala dependencias de sistema primero")
            return False
    
    print("\n✅ Todas las dependencias instaladas")
    return True

def create_spec_file():
    print_header("CREANDO CONFIGURACIÓN DE PYINSTALLER")
    
    logo_exists = os.path.exists(os.path.join(SCRIPT_DIR, 'LogoLogin.png'))
    foto_exists = os.path.exists(os.path.join(SCRIPT_DIR, 'emiliaMP3Foto.png'))
    
    datas_list = []
    if logo_exists:
        datas_list.append("('LogoLogin.png', '.')")
    if foto_exists:
        datas_list.append("('emiliaMP3Foto.png', '.')")
    
    # Módulos necesarios
    modulos = [
        'radioBloom.py',
        'config_persistente.py',
        'GestorVentanas.py',
        'PaginaEditarPerfil.py'
    ]
    
    for modulo in modulos:
        if os.path.exists(os.path.join(SCRIPT_DIR, modulo)):
            datas_list.append(f"('{modulo}', '.')")
    
    datas_string = ",\n        ".join(datas_list)
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
    
    print(f"✅ Archivo .spec creado")
    return True

def build_executable():
    print_header("CREANDO EJECUTABLE")
    print("⚙️  Compilando... (varios minutos)\n")
    
    try:
        spec_file = os.path.join(SCRIPT_DIR, "BloomMusic.spec")
        pyinstaller_path = os.path.join(VENV_DIR, "bin", "pyinstaller")
        
        if not os.path.exists(pyinstaller_path):
            print("❌ PyInstaller no encontrado")
            return False
        
        subprocess.check_call([pyinstaller_path, spec_file, "--clean"])
        print("\n✅ Ejecutable creado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        return False

def verify_files():
    print_header("VERIFICANDO ARCHIVOS DEL PROYECTO")
    print(f"📂 Buscando en: {SCRIPT_DIR}\n")
    
    required_files = [
        "BloomMusic.py",
        "config_persistente.py",
        "GestorVentanas.py",
        "PaginaEditarPerfil.py",
        "radioBloom.py"
    ]
    
    optional_files = ["LogoLogin.png", "emiliaMP3Foto.png"]
    
    all_ok = True
    
    print("📋 Archivos REQUERIDOS:")
    for file in required_files:
        if os.path.exists(os.path.join(SCRIPT_DIR, file)):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NO ENCONTRADO")
            all_ok = False
    
    print("\n📋 Archivos OPCIONALES:")
    for file in optional_files:
        if os.path.exists(os.path.join(SCRIPT_DIR, file)):
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} no encontrado")
    
    return all_ok

def create_desktop_entry():
    print_header("CREANDO INTEGRACIÓN CON EL ESCRITORIO")
    
    exe_path = os.path.join(SCRIPT_DIR, "dist", "BloomMusic")
    logo_path = os.path.join(SCRIPT_DIR, "LogoLogin.png")
    
    if not os.path.exists(logo_path):
        logo_path = ""
    
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Bloom Music V2
Comment=Reproductor de música con BD persistente
Exec={exe_path}
Icon={logo_path}
Terminal=false
Categories=AudioVideo;Audio;Player;
Keywords=music;audio;player;mp3;
"""
    
    desktop_file = os.path.join(SCRIPT_DIR, "BloomMusic.desktop")
    with open(desktop_file, "w") as f:
        f.write(desktop_content)
    
    os.chmod(desktop_file, 0o755)
    print(f"✅ Archivo .desktop creado")
    print(f"\n💡 Para añadirlo al menú:")
    print(f"   cp {desktop_file} ~/.local/share/applications/")
    return desktop_file

def create_launcher_script():
    print_header("CREANDO SCRIPT DE LANZAMIENTO")
    
    launcher_content = """#!/bin/bash
# Bloom Music V2 Launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
exec ./dist/BloomMusic "$@"
"""
    
    launcher_path = os.path.join(SCRIPT_DIR, "bloom_music.sh")
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
    
    os.chmod(launcher_path, 0o755)
    print(f"✅ Script creado: bloom_music.sh")
    return launcher_path

def create_readme():
    print_header("CREANDO DOCUMENTACIÓN")
    
    readme_content = """# BLOOM MUSIC V2 - Linux (BD Persistente)

## 🎵 Nueva Versión - Características

✅ **BD Persistente**: Tu cuenta NO se pierde
✅ **Navegación mejorada**: Sin perder datos
✅ **Editar perfil**: Gestiona tu cuenta
✅ **Código optimizado**: 53% menos líneas

## 🚀 Ejecutar

### Opción 1: Directo
```bash
./dist/BloomMusic
```

### Opción 2: Script
```bash
./bloom_music.sh
```

### Opción 3: Menú
```bash
cp BloomMusic.desktop ~/.local/share/applications/
```

## 💾 Base de Datos

Ubicación: `~/.config/BloomMusic/database/`

**Beneficios:**
- ✅ NO se pierde al reinstalar
- ✅ Actualiza sin perder datos
- ✅ Protegida en ubicación estándar

## 📋 Archivos Requeridos

- BloomMusic.py
- config_persistente.py
- GestorVentanas.py
- PaginaEditarPerfil.py
- radioBloom.py

## 🔧 Dependencias Sistema

```bash
sudo apt install python3-dev python3-venv python3-full \\
  libsdl2-dev libsdl2-mixer-dev build-essential
```

## ✨ Nuevas Funciones

- **Editar perfil**: Menú "⋯" → "Editar Perfil"
- **8 vistas**: Home, Canciones, Recientes, Crear Playlist, etc.
- **Música continua**: Sigue sonando entre vistas

## 📚 Más Info

- RESUMEN_CAMBIOS.md: Qué cambió
- INSTRUCCIONES_IMPLEMENTACION.md: Guía completa

---
**Bloom Music V2** - Con BD Persistente 🎵
"""
    
    readme_path = os.path.join(SCRIPT_DIR, "README_LINUX.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ README_LINUX.md creado")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🎵 BLOOM MUSIC V2 - INSTALADOR LINUX 🎵              ║
║                                                          ║
║  ✨ Con Base de Datos Persistente ✨                     ║
║  Compatible con Python 3.13+ (PEP 668)                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Paso 1: Verificar Python
    if not check_python_version():
        input("\nENTER para salir...")
        return
    
    # Paso 2: Verificar venv
    if not check_venv_support():
        input("\nENTER para salir...")
        return
    
    # Paso 3: Verificar archivos
    if not verify_files():
        print("\n❌ Faltan archivos necesarios")
        print("\n💡 Copia TODOS estos archivos:")
        print("   • BloomMusic.py")
        print("   • config_persistente.py")
        print("   • GestorVentanas.py")
        print("   • PaginaEditarPerfil.py")
        print("   • radioBloom.py")
        input("\nENTER para salir...")
        return
    
    # Paso 4: Buscar BD existente
    bd_existente = buscar_bd_existente()
    
    # Paso 5: Dependencias sistema
    check_system_dependencies()
    
    # Paso 6: Crear venv
    if not create_virtual_environment():
        input("\nENTER para salir...")
        return
    
    # Paso 7: Crear docs
    create_readme()
    
    # Paso 8: Preguntar si continuar
    print("\n" + "="*60)
    respuesta = input("¿Instalar dependencias y crear ejecutable? (s/n): ")
    
    if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
        print("\n✅ Entorno creado, docs listas")
        print("\n💡 Para continuar: python3 setup_bloom_linux.py")
        return
    
    # Paso 9: Instalar deps
    if not install_dependencies():
        print("\n❌ Error en dependencias")
        input("\nENTER para salir...")
        return
    
    # Paso 10: Crear .spec
    if not create_spec_file():
        print("\n❌ Error en config")
        input("\nENTER para salir...")
        return
    
    # Paso 11: Crear ejecutable
    if not build_executable():
        print("\n❌ Error creando ejecutable")
        input("\nENTER para salir...")
        return
    
    # Paso 12: Crear integraciones
    launcher_path = create_launcher_script()
    desktop_file = create_desktop_entry()
    
    # ¡Éxito!
    print_header("¡INSTALACIÓN COMPLETADA!")
    
    exe_path = os.path.join(SCRIPT_DIR, "dist", "BloomMusic")
    
    print("✅ Bloom Music V2 instalado\n")
    print("📁 Ejecutable:")
    print(f"   {exe_path}\n")
    
    if os.path.exists(exe_path):
        os.chmod(exe_path, 0o755)
        print("✅ Permisos configurados\n")
    
    print("📁 Archivos creados:")
    print(f"   • {exe_path}")
    print(f"   • {launcher_path}")
    print(f"   • {desktop_file}")
    print(f"   • {VENV_DIR}/ (entorno virtual)")
    print("   • README_LINUX.md")
    
    print("\n💾 Tu BD estará en:")
    print("   ~/.config/BloomMusic/database/\n")
    
    if bd_existente:
        print("📋 Tu BD existente:")
        print("   ✅ Fue detectada")
        print("   ✅ Se importará al primer uso")
        print("   ✅ Tu cuenta estará disponible\n")
    
    print("🚀 Para ejecutar:\n")
    print("   Opción 1: ./dist/BloomMusic")
    print("   Opción 2: ./bloom_music.sh\n")
    
    print("✨ Nuevas funciones:")
    print("   • Editar perfil desde la app")
    print("   • 8 vistas de navegación")
    print("   • Música continua entre vistas")
    print("   • BD que NO se pierde\n")
    
    print("=" * 60)
    
    response = input("\n¿Añadir al menú de aplicaciones? (s/n): ")
    if response.lower() in ['s', 'si', 'y', 'yes']:
        apps_dir = os.path.expanduser("~/.local/share/applications")
        os.makedirs(apps_dir, exist_ok=True)
        shutil.copy(desktop_file, apps_dir)
        print("\n✅ Añadido al menú")
    
    input("\nENTER para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print(f"\n📂 Directorio: {SCRIPT_DIR}")
        import traceback
        traceback.print_exc()
        input("\nENTER para salir...")
        sys.exit(1)