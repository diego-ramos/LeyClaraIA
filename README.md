# LeyClara.IA 📜⚖️

**LeyClara.IA** es un asistente legal inteligente diseñado para democratizar el acceso a la información jurídica. Su objetivo es tomar documentos legales complejos (leyes, contratos, sentencias) y explicarlos en un lenguaje sencillo y accesible para cualquier persona, "como si tuviera 5 años".

## 🧠 Arquitectura Técnica: RAG (Retrieval-Augmented Generation)

Este proyecto utiliza una arquitectura **RAG** en lugar de un chat simple con IA.

### ¿Por qué RAG?
Los modelos de lenguaje (LLMs) como GPT o Gemini tienen dos grandes limitaciones:
1.  **Alucinaciones:** Pueden inventar datos si no saben la respuesta.
2.  **Desconocimiento:** No conocen tus documentos privados o leyes locales específicas que no estaban en su entrenamiento.

RAG soluciona esto permitiendo que la IA "lea" tus documentos antes de responder. El flujo es:
1.  **Búsqueda (Retrieval):** El sistema busca en tu biblioteca los párrafos exactos que responden a tu pregunta.
2.  **Generación (Augmented Generation):** Envía esos párrafos a la IA y le dice: *"Usa SOLO esta información para responder al usuario"*. Esto garantiza respuestas precisas y basadas en evidencia real.

## 📚 El Rol de ChromaDB (Nuestra "Biblioteca")

Para que el sistema sea rápido y eficiente, utilizamos **ChromaDB**, una base de datos vectorial.

*   **El Problema:** No podemos enviarle un PDF de 500 páginas a la IA cada vez que hacemos una pregunta. Sería lento, costoso y excedería la memoria del modelo.
*   **La Solución (ChromaDB):**
    1.  Cuando subes un PDF, lo "cortamos" en pedazos pequeños.
    2.  Convertimos cada pedazo en una "huella digital matemática" (vector) usando la API de Google Embeddings.
    3.  Guardamos estos vectores en ChromaDB localmente.
    4.  Cuando preguntas, ChromaDB encuentra matemáticamente los 6 fragmentos más parecidos a tu pregunta en milisegundos, sin tener que volver a leer todo el documento.

## ✂️ Estrategia de Chunking (Fragmentación)

Una decisión crítica de diseño fue el tamaño de los "chunks" (fragmentos de texto).

*   **Configuración Actual:** 500 caracteres (con 100 de solapamiento).
*   **¿Por qué este tamaño?**
    *   Inicialmente probamos con 1000 caracteres, pero el sistema perdía detalles específicos (como números de artículos o títulos cortos) porque se "diluían" en tanto texto.
    *   Al reducirlo a **500 caracteres**, logramos un efecto "lupa": cada fragmento es más específico y preciso. Esto permite encontrar "agujas en un pajar" (detalles puntuales) con mucha mayor eficacia.

## 🧩 El Rol de LangChain (El "Pegamento")

**LangChain** es el framework que conecta todas las piezas del rompecabezas. Actúa como el orquestador que:

1.  **Carga y Procesa:** Usa herramientas para leer PDFs y dividirlos en chunks.
2.  **Conecta:** Sirve de puente entre tu base de datos local (ChromaDB) y la API de Google (Gemini).
3.  **Gestiona el Flujo:** Cuando haces una pregunta, LangChain ejecuta automáticamente una "cadena" de pasos: buscar contexto -> construir el prompt -> consultar a la IA -> entregar la respuesta.

Sin LangChain, tendríamos que escribir manualmente todo el código para conectar estos servicios dispares.

## 🛠️ Tecnologías

*   **Backend:** Python, FastAPI.
*   **IA:** Google Gemini 1.5 Flash (vía LangChain).
*   **Base de Datos:** ChromaDB (Vector Store).
*   **Frontend:** React, TailwindCSS.
*   **Infraestructura:** Docker & Docker Compose.

## 🚀 Cómo Ejecutarlo

### Desarrollo Local

1.  Clona el repositorio.
2.  Crea un archivo `.env` en la raíz con tus claves de API (ver `.env.example`).
3.  Crea un archivo `frontend/.env` con:
    ```env
    VITE_API_URL=http://localhost:8000
    ```
4.  Ejecuta:
    ```bash
    docker-compose up --build
    ```
5.  Abre `http://localhost:3000` y empieza a subir documentos.

### 🌐 Despliegue en la Nube

#### Opción 1: Google Compute Engine (Recomendado - Con Persistencia)

Para despliegue en producción con almacenamiento persistente:

```bash
# Ver instrucciones completas
cat .agent/workflows/deploy-to-gce.md
```

**Ventajas:**
- ✅ Datos persistentes (ChromaDB, documentos subidos)
- ✅ Costos predecibles (~$15-30/mes)
- ✅ Control total del servidor

#### Opción 2: Railway

Railway ofrece $5/mes de crédito gratuito, suficiente para proyectos pequeños/medianos.

**Guía Rápida:**
1. Crea una cuenta en [railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Sigue la guía: [`RAILWAY_DEPLOY.md`](RAILWAY_DEPLOY.md)
4. Usa el checklist: [`RAILWAY_CHECKLIST.md`](RAILWAY_CHECKLIST.md)

**Recursos:**
- 📖 [Guía Completa de Despliegue](.agent/workflows/deploy_to_railway.md)
- 🔧 [Variables de Entorno](RAILWAY_ENV_VARS.md)
- ✅ [Checklist de Despliegue](RAILWAY_CHECKLIST.md)

#### Opción 3: Google Cloud Run (Stateless)

Para despliegue rápido sin persistencia:

```bash
# Ver instrucciones
cat .agent/workflows/deploy_to_cloud_run.md
```

**Limitaciones:**
- ⚠️ Los datos se pierden al reiniciar
- ⚠️ No recomendado para producción

#### Otras Opciones

- **Render**: Alternativa gratuita similar a Railway
- **Fly.io**: Excelente para aplicaciones Docker
