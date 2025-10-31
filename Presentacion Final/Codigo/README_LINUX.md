# BLOOM MUSIC V2 - Linux (BD Persistente)

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
sudo apt install python3-dev python3-venv python3-full \
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
