# 🚀 Railway - Referencia Rápida

## 📋 Variables de Entorno - Copiar y Pegar

### Backend Service
```env
GOOGLE_API_KEY=
YOUTUBE_API_KEY=
CHROMA_DB_DIR=/app/chroma_db
PYTHONUNBUFFERED=1
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Service
```env
VITE_API_URL=
```

---

## ⚙️ Configuración de Servicios

### Backend
- **Root Directory**: `backend`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Volume Mount Path**: `/app/chroma_db`

### Frontend
- **Root Directory**: `frontend`
- **Build Command**: (automático con Dockerfile)
- **Start Command**: (automático con Dockerfile)

---

## 🔗 URLs a Copiar

### Después de desplegar Backend:
```
Backend URL: _________________________________
```
→ Pegar en `VITE_API_URL` del frontend

### Después de desplegar Frontend:
```
Frontend URL: _________________________________
```
→ Agregar a `ALLOWED_ORIGINS` del backend:
```env
ALLOWED_ORIGINS=http://localhost:3000,https://tu-frontend-url.railway.app
```

---

## ✅ Checklist Rápido

- [ ] Backend desplegado
- [ ] Backend URL copiada
- [ ] Frontend desplegado con `VITE_API_URL` correcto
- [ ] Frontend URL copiada
- [ ] `ALLOWED_ORIGINS` actualizada en backend
- [ ] Volume agregado a backend (`/app/chroma_db`)
- [ ] Probado: `https://backend-url/health` responde `{"status": "ok"}`
- [ ] Probado: Frontend carga correctamente
- [ ] Probado: Subir documento funciona
- [ ] Probado: Chat funciona

---

## 🆘 Comandos de Verificación

### Verificar Backend
```bash
curl https://tu-backend-url.railway.app/health
# Debe responder: {"status":"ok"}
```

### Ver Logs en Railway
1. Click en el servicio
2. Tab "Logs"
3. Buscar errores en rojo

---

## 📞 Links Útiles

- Railway Dashboard: https://railway.app/dashboard
- Documentación: https://docs.railway.app
- Status: https://status.railway.app

---

**Tiempo estimado total**: 15-20 minutos ⏱️
