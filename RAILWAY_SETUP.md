# 🔧 Railway Setup - Variables de Entorno

## 📋 Paso 1: Variables del Backend

Cuando despliegues el **Backend** en Railway, ve a:
**Backend Service → Variables → Raw Editor** y pega esto:

```env
GOOGLE_API_KEY=tu_google_api_key_aqui
YOUTUBE_API_KEY=tu_youtube_api_key_aqui
CHROMA_DB_DIR=/app/chroma_db
PYTHONUNBUFFERED=1
ALLOWED_ORIGINS=http://localhost:3000
```

> **Nota**: Actualizarás `ALLOWED_ORIGINS` después de desplegar el frontend para incluir la URL de Railway.

### ⚠️ IMPORTANTE: Reemplaza los valores

- **`GOOGLE_API_KEY`**: Tu API key de Google Gemini
  - Obtén una en: https://makersuite.google.com/app/apikey
  
- **`YOUTUBE_API_KEY`**: Tu API key de YouTube Data API
  - Obtén una en: https://console.cloud.google.com/apis/credentials

### ✅ Cómo obtener tus valores actuales

Si ya tienes un archivo `.env` local, copia los valores de ahí.

---

## 📋 Paso 2: Variables del Frontend

Cuando despliegues el **Frontend** en Railway, necesitas configurar la URL del backend.

**Frontend Service → Variables → Raw Editor** y pega esto:

```env
VITE_API_URL=https://tu-backend-url.railway.app
```

### ⚠️ IMPORTANTE: Obtén la URL del Backend primero

1. Despliega el **Backend** primero
2. Ve a **Backend Service → Settings → Networking**
3. Click en **"Generate Domain"**
4. Copia la URL (ejemplo: `https://leyclara-ia-backend-production.up.railway.app`)
5. Usa esa URL en `VITE_API_URL` del frontend

---

## 📋 Paso 3: Actualizar CORS del Backend

Después de desplegar el **Frontend**, actualiza las variables del backend:

1. Ve a **Frontend Service → Settings → Networking**
2. Copia la URL del frontend (ejemplo: `https://leyclara-ia-frontend-production.up.railway.app`)
3. Ve a **Backend Service → Variables**
4. Actualiza `ALLOWED_ORIGINS` para incluir ambas URLs:

```env
ALLOWED_ORIGINS=http://localhost:3000,https://leyclara-ia-frontend-production.up.railway.app
```

> **Nota**: Separa múltiples URLs con comas (sin espacios)

Railway redesplegará automáticamente el backend con la nueva configuración.

---

## 🎯 Ejemplo Completo

### Backend Variables (ejemplo)
```env
GOOGLE_API_KEY=AIzaSyABC123def456GHI789jkl012MNO345pqr
YOUTUBE_API_KEY=AIzaSyXYZ789abc012DEF345ghi678JKL901mno
CHROMA_DB_DIR=/app/chroma_db
PYTHONUNBUFFERED=1
ALLOWED_ORIGINS=http://localhost:3000,https://leyclara-ia-frontend-production.up.railway.app
```

### Frontend Variables (ejemplo)
```env
VITE_API_URL=https://leyclara-ia-backend-production.up.railway.app
```

---

## 🔒 Seguridad

✅ **SÍ hacer:**
- Guardar tus API keys en un lugar seguro (gestor de contraseñas)
- Usar variables de entorno en Railway (no hardcodear en el código)
- Regenerar keys si las compartes accidentalmente

❌ **NO hacer:**
- Commitear el archivo `.env` a Git (ya está en `.gitignore` ✅)
- Compartir tus API keys públicamente
- Usar las mismas keys en múltiples proyectos

---

## 📝 Checklist de Variables

### Backend
- [ ] `GOOGLE_API_KEY` configurada
- [ ] `YOUTUBE_API_KEY` configurada
- [ ] `CHROMA_DB_DIR=/app/chroma_db` configurada
- [ ] `PYTHONUNBUFFERED=1` configurada

### Frontend
- [ ] Backend desplegado primero
- [ ] URL del backend copiada
- [ ] `VITE_API_URL` configurada con la URL correcta

---

## 🆘 Troubleshooting

### Error: "API key not valid"
- Verifica que copiaste la key completa (sin espacios)
- Asegúrate de que la API está habilitada en Google Cloud Console

### Error: "Frontend can't connect to backend"
- Verifica que `VITE_API_URL` tiene la URL correcta
- Asegúrate de que el backend está desplegado y corriendo
- Revisa los logs del backend para errores CORS

### Error: "ChromaDB not persisting data"
- Asegúrate de agregar un Volume en Railway
- Mount path debe ser: `/app/chroma_db`
- Verifica que `CHROMA_DB_DIR` apunta a la misma ruta

---

## 🎉 Siguiente Paso

Una vez configuradas las variables:
1. Railway desplegará automáticamente
2. Revisa los **Logs** para confirmar que todo está bien
3. Genera el dominio público
4. ¡Prueba tu app!

**Continúa con**: [`RAILWAY_CHECKLIST.md`](RAILWAY_CHECKLIST.md) ✅
