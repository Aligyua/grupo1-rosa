"""
BLOOM MUSIC - DESINSTALADOR
============================
Este script desinstala Bloom Music y limpia todos los archivos generados

⚠️  ADVERTENCIA: Este proceso NO es reversible
    Se eliminarán:
    - Ejecutables generados
    - Base de datos (usuarios y configuraciones)
    - Archivos de compilación
    - Dependencias de Python (opcional)

INSTRUCCIONES:
1. Cierra Bloom Music si está abierto
2. Ejecuta: python uninstall_BloomMusic.py
3. Sigue las instrucciones en pantalla
4. Confirma qué deseas eliminar
"""

import os
import sys
import shutil
import platform
import subprocess

# Obtener ruta del script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def print_header(text):
    """Imprime un header bonito"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_warning(text):
    """Imprime una advertencia"""
    print("\n⚠️  " + "="*56)
    print(f"   {text}")
    print("   " + "="*56 + "\n")

def get_size_mb(path):
    """Obtiene el tamaño de un archivo o carpeta en MB"""
    if os.path.isfile(path):
        return os.path.getsize(path) / (1024 * 1024)
    elif os.path.isdir(path):
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total += os.path.getsize(filepath)
        return total / (1024 * 1024)
    return 0

def scan_files():
    """Escanea y muestra todos los archivos que se pueden eliminar"""
    print_header("ESCANEANDO ARCHIVOS DE BLOOM MUSIC")
    
    files_to_delete = {
        'ejecutables': [],
        'compilacion': [],
        'base_datos': [],
        'configuracion': [],
        'logs': []
    }
    
    total_size = 0
    
    # Carpetas de compilación
    compilation_folders = ['build', 'dist', '__pycache__']
    for folder in compilation_folders:
        folder_path = os.path.join(SCRIPT_DIR, folder)
        if os.path.exists(folder_path):
            size = get_size_mb(folder_path)
            files_to_delete['compilacion'].append({
                'path': folder_path,
                'name': folder,
                'size': size,
                'type': 'folder'
            })
            total_size += size
    
    # Archivos de compilación
    compilation_files = ['BloomMusic.spec']
    for file in compilation_files:
        file_path = os.path.join(SCRIPT_DIR, file)
        if os.path.exists(file_path):
            size = get_size_mb(file_path)
            files_to_delete['compilacion'].append({
                'path': file_path,
                'name': file,
                'size': size,
                'type': 'file'
            })
            total_size += size
    
    # Base de datos
    db_files = ['Database_Bloom_Music.db', 'Database_Bloom_Music.db-journal']
    for file in db_files:
        file_path = os.path.join(SCRIPT_DIR, file)
        if os.path.exists(file_path):
            size = get_size_mb(file_path)
            files_to_delete['base_datos'].append({
                'path': file_path,
                'name': file,
                'size': size,
                'type': 'file'
            })
            total_size += size
    
    # Archivos de configuración
    config_files = ['README.md', 'INSTALAR.bat', 'instalar.sh']
    for file in config_files:
        file_path = os.path.join(SCRIPT_DIR, file)
        if os.path.exists(file_path):
            size = get_size_mb(file_path)
            files_to_delete['configuracion'].append({
                'path': file_path,
                'name': file,
                'size': size,
                'type': 'file'
            })
            total_size += size
    
    # Archivos cache de Python
    pycache_folders = []
    for root, dirs, files in os.walk(SCRIPT_DIR):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            if pycache_path not in [item['path'] for item in files_to_delete['compilacion']]:
                size = get_size_mb(pycache_path)
                files_to_delete['compilacion'].append({
                    'path': pycache_path,
                    'name': os.path.relpath(pycache_path, SCRIPT_DIR),
                    'size': size,
                    'type': 'folder'
                })
                total_size += size
    
    return files_to_delete, total_size

def display_scan_results(files_to_delete, total_size):
    """Muestra los resultados del escaneo"""
    print("📊 Archivos encontrados:\n")
    
    categories = {
        'compilacion': '🔧 Archivos de compilación',
        'base_datos': '💾 Base de datos',
        'configuracion': '📄 Archivos de configuración'
    }
    
    total_items = 0
    
    for category, title in categories.items():
        items = files_to_delete[category]
        if items:
            print(f"{title}:")
            for item in items:
                icon = "📁" if item['type'] == 'folder' else "📄"
                print(f"  {icon} {item['name']} ({item['size']:.2f} MB)")
            print()
            total_items += len(items)
    
    if total_items == 0:
        print("✅ No se encontraron archivos de Bloom Music para eliminar")
        return False
    
    print(f"📦 Total: {total_items} elemento(s) | {total_size:.2f} MB\n")
    return True

def delete_files(files_list):
    """Elimina los archivos y carpetas de la lista"""
    deleted_count = 0
    failed_count = 0
    
    for item in files_list:
        try:
            if item['type'] == 'folder':
                shutil.rmtree(item['path'])
                print(f"  ✅ Eliminada carpeta: {item['name']}")
            else:
                os.remove(item['path'])
                print(f"  ✅ Eliminado archivo: {item['name']}")
            deleted_count += 1
        except Exception as e:
            print(f"  ❌ Error eliminando {item['name']}: {e}")
            failed_count += 1
    
    return deleted_count, failed_count

def uninstall_dependencies():
    """Desinstala las dependencias de Python"""
    print_header("DESINSTALANDO DEPENDENCIAS DE PYTHON")
    
    dependencies = [
        "pygame",
        "Pillow",
        "mutagen",
        "pyinstaller"
    ]
    
    print("⚠️  Esto eliminará las siguientes librerías:")
    for dep in dependencies:
        print(f"   • {dep}")
    print("\n⚠️  NOTA: Si usas estas librerías en otros proyectos,")
    print("   NO las desinstales.\n")
    
    response = input("¿Deseas desinstalar las dependencias? (s/n): ")
    
    if response.lower() not in ['s', 'si', 'y', 'yes']:
        print("\n⏭️  Saltando desinstalación de dependencias")
        return True
    
    print("\n🔄 Desinstalando dependencias...")
    success_count = 0
    
    for dep in dependencies:
        print(f"\n📦 Desinstalando {dep}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "uninstall", dep, "-y"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"   ✅ {dep} desinstalado")
            success_count += 1
        except subprocess.CalledProcessError:
            print(f"   ⚠️  {dep} no está instalado o no se pudo desinstalar")
    
    print(f"\n✅ {success_count}/{len(dependencies)} dependencias desinstaladas")
    return True

def create_uninstall_batch():
    """Crea un script .bat/.sh para desinstalación rápida"""
    print_header("CREANDO SCRIPT DE DESINSTALACIÓN RÁPIDA")
    
    if platform.system() == "Windows":
        # Script para Windows
        bat_content = """@echo off
echo ========================================
echo   BLOOM MUSIC - DESINSTALADOR
echo ========================================
echo.
echo Cambiando al directorio del script...
cd /d "%~dp0"
echo.

python uninstall_BloomMusic.py

pause
"""
        bat_path = os.path.join(SCRIPT_DIR, "DESINSTALAR.bat")
        with open(bat_path, "w") as f:
            f.write(bat_content)
        print(f"✅ Script DESINSTALAR.bat creado en: {bat_path}")
    
    else:
        # Script para Linux/Mac
        sh_content = """#!/bin/bash
echo "========================================"
echo "  BLOOM MUSIC - DESINSTALADOR"
echo "========================================"
echo ""
echo "Cambiando al directorio del script..."
cd "$(dirname "$0")"
echo ""

python3 uninstall_BloomMusic.py
"""
        sh_path = os.path.join(SCRIPT_DIR, "desinstalar.sh")
        with open(sh_path, "w") as f:
            f.write(sh_content)
        
        # Dar permisos de ejecución
        os.chmod(sh_path, 0o755)
        print(f"✅ Script desinstalar.sh creado en: {sh_path}")

def backup_database():
    """Crea un respaldo de la base de datos antes de eliminarla"""
    db_path = os.path.join(SCRIPT_DIR, "Database_Bloom_Music.db")
    
    if not os.path.exists(db_path):
        return None
    
    print_header("RESPALDO DE BASE DE DATOS")
    print("Se encontró una base de datos con tus usuarios y configuraciones.\n")
    
    response = input("¿Deseas crear un respaldo antes de eliminarla? (s/n): ")
    
    if response.lower() not in ['s', 'si', 'y', 'yes']:
        return None
    
    try:
        # Crear carpeta de respaldos si no existe
        backup_folder = os.path.join(SCRIPT_DIR, "backup_bloom")
        os.makedirs(backup_folder, exist_ok=True)
        
        # Nombre del archivo de respaldo con fecha
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"Database_Bloom_Music_backup_{timestamp}.db"
        backup_path = os.path.join(backup_folder, backup_name)
        
        # Copiar base de datos
        shutil.copy2(db_path, backup_path)
        
        print(f"\n✅ Respaldo creado exitosamente:")
        print(f"   📁 {backup_path}")
        print(f"   💾 Tamaño: {get_size_mb(backup_path):.2f} MB")
        
        return backup_path
    
    except Exception as e:
        print(f"\n❌ Error creando respaldo: {e}")
        return None

def main():
    """Función principal del desinstalador"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        🗑️  BLOOM MUSIC - DESINSTALADOR 🗑️               ║
║                                                          ║
║  Este script eliminará Bloom Music y sus archivos       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print(f"📂 Trabajando en: {SCRIPT_DIR}\n")
    
    # Advertencia inicial
    print_warning("⚠️  ADVERTENCIA IMPORTANTE ⚠️")
    print("Este proceso eliminará:")
    print("  • Ejecutables compilados (.exe)")
    print("  • Base de datos (usuarios y configuraciones)")
    print("  • Archivos de compilación (build, dist, __pycache__)")
    print("  • Scripts de instalación")
    print("  • Opcionalmente: Dependencias de Python\n")
    print("⚠️  Los archivos de código fuente (.py) NO se eliminarán")
    print("⚠️  Las imágenes (LogoLogin.png, etc.) NO se eliminarán\n")
    
    response = input("¿Estás seguro de que deseas continuar? (s/n): ")
    
    if response.lower() not in ['s', 'si', 'y', 'yes']:
        print("\n❌ Desinstalación cancelada")
        return
    
    # Escanear archivos
    files_to_delete, total_size = scan_files()
    
    # Mostrar resultados
    if not display_scan_results(files_to_delete, total_size):
        print("\n✅ No hay nada que desinstalar")
        input("\nPresiona ENTER para salir...")
        return
    
    # Confirmar eliminación
    print_warning("CONFIRMACIÓN FINAL")
    response = input("¿Proceder con la eliminación? (s/n): ")
    
    if response.lower() not in ['s', 'si', 'y', 'yes']:
        print("\n❌ Desinstalación cancelada")
        return
    
    # Crear respaldo de base de datos
    backup_path = backup_database()
    
    # Proceso de eliminación
    print_header("ELIMINANDO ARCHIVOS")
    
    total_deleted = 0
    total_failed = 0
    
    # Eliminar por categorías
    for category in ['compilacion', 'base_datos', 'configuracion']:
        if files_to_delete[category]:
            print(f"\n🗑️  Eliminando {category}...")
            deleted, failed = delete_files(files_to_delete[category])
            total_deleted += deleted
            total_failed += failed
    
    # Resumen
    print_header("RESUMEN DE DESINSTALACIÓN")
    
    print(f"✅ Archivos eliminados: {total_deleted}")
    if total_failed > 0:
        print(f"❌ Errores: {total_failed}")
    print(f"💾 Espacio liberado: {total_size:.2f} MB")
    
    if backup_path:
        print(f"\n📦 Respaldo guardado en:")
        print(f"   {backup_path}")
    
    # Preguntar por dependencias
    print("\n" + "="*60)
    uninstall_dependencies()
    
    # Resultado final
    print_header("DESINSTALACIÓN COMPLETADA")
    
    print("✅ Bloom Music ha sido desinstalado\n")
    print("📁 Archivos que permanecen:")
    print("   • Código fuente (.py)")
    print("   • Imágenes (.png)")
    print("   • Este desinstalador (uninstall_BloomMusic.py)")
    if backup_path:
        print("   • Respaldo de base de datos (backup_bloom/)")
    
    print("\n💡 Para reinstalar Bloom Music:")
    print("   Ejecuta: python setup_bloom.py")
    
    print("\n🗑️  Para eliminar completamente:")
    print("   Borra manualmente esta carpeta completa")
    
    print("\n" + "="*60)
    
    # Preguntar si eliminar el desinstalador
    print("\n¿Deseas eliminar también este desinstalador? (s/n): ")
    response = input()
    
    if response.lower() in ['s', 'si', 'y', 'yes']:
        try:
            # Crear script para auto-eliminación
            if platform.system() == "Windows":
                delete_script = os.path.join(SCRIPT_DIR, "delete_uninstaller.bat")
                with open(delete_script, "w") as f:
                    f.write(f'''@echo off
timeout /t 2 /nobreak >nul
del "{os.path.abspath(__file__)}"
del "%~f0"
''')
                print("\n✅ El desinstalador se auto-eliminará al cerrar")
                subprocess.Popen(delete_script, shell=True)
            else:
                os.remove(__file__)
                print("\n✅ Desinstalador eliminado")
        except Exception as e:
            print(f"\n⚠️  No se pudo eliminar el desinstalador: {e}")
            print(f"   Puedes eliminarlo manualmente: {__file__}")
    
    input("\nPresiona ENTER para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Desinstalación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        print(f"\n📂 Directorio de trabajo: {SCRIPT_DIR}")
        input("\nPresiona ENTER para salir...")
        sys.exit(1)