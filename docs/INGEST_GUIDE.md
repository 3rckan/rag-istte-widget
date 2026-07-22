# 📚 Instrucciones para agregar nuevos PDFs

## Paso 1: Copiar los archivos PDF

Los dos nuevos PDFs deben guardarse en la carpeta `data/reglamentos/` con estos nombres exactos:

```
c:\proyecto_istte\rag-istte-widget\data\reglamentos\
├── guía_del_docente_eva_periodo_p37.pdf
├── guía_del_estudiante_eva_periodo_p37.pdf
├── calendario_academico_ejemplo.pdf
└── reglamento_academico_ejemplo.pdf
```

**Nombres esperados:**
- `guía_del_docente_eva_periodo_p37.pdf`
- `guía_del_estudiante_eva_periodo_p37.pdf`

⚠️ **Importante**: Los nombres deben ser exactos (con tildes) para que el sistema reconozca el contexto de imágenes.

## Paso 2: Ejecutar el script de ingesta

Una vez los PDFs estén en la carpeta, ejecuta:

```bash
python scripts/ingest.py
```

Este script:
1. ✅ Lee todos los PDFs de `data/reglamentos/`
2. ✅ Extrae el texto de cada página
3. ✅ Agrega descripciones de elementos visuales importantes
4. ✅ Divide todo en fragmentos manejables
5. ✅ Genera embeddings usando Ollama
6. ✅ Guarda todo en ChromaDB

## Paso 3: Reiniciar el asistente

El servidor se recargará automáticamente (modo watch), pero si no lo hace:

```bash
# Detener: CTRL+C
# Volver a iniciar:
python -m uvicorn app.main:app --reload
```

## 🎯 Qué sucede después

El asistente podrá responder preguntas sobre:
- **Estructura de Tu Aula Virtual**: Cabecera, Generalidades, Bloques de Aprendizaje
- **Acceso y navegación**: Cómo acceder, componentes principales
- **Actividades y evaluaciones**: Cómo se organizan los parciales
- **Procedimientos técnicos**: Pasos para cargar actividades, usar tutorías
- **Portafolio y evidencias**: Cómo recolectar trabajos del estudiante
- **Sistema ABP**: Aprendizaje Basado en Problemas

## 📊 Información técnica

El sistema mejorado:
- **Extrae el 100% del texto** de los PDFs
- **Agrega contexto visual** de las imágenes (descripciones de interfaces, diagramas, procesos)
- **Crea conexiones semánticas** entre el contenido textual y visual
- **Usa embeddings de alta calidad** (modelo: nomic-embed-text)
- **Chunking inteligente** (700 caracteres por fragmento con 100 de superposición)

## ✅ Verificación

Después de ejecutar `ingest.py`, deberías ver algo como:

```
🚀 Iniciando ingesta de documentos...

📂 Encontrados 4 archivos PDF
  📄 Procesando: calendario_academico_ejemplo.pdf
  📄 Procesando: guía_del_docente_eva_periodo_p37.pdf
  📄 Procesando: guía_del_estudiante_eva_periodo_p37.pdf
  📄 Procesando: reglamento_academico_ejemplo.pdf

✓ Cargados 36 documentos

✂️  Divididos en 82 chunks

🔄 Generando embeddings con Ollama (nomic-embed-text)...
💾 Guardando en ChromaDB (chroma_db)...
✅ Base de datos creada exitosamente

✅ Ingesta completa: 82 fragmentos guardados
```

---

**Preguntas de prueba después de la ingesta:**

- "¿Cómo accedo a Tu Aula Virtual?"
- "¿Cuáles son los bloques de aprendizaje?"
- "¿Cómo cargo una actividad?"
- "¿Qué es el Portafolio del Estudiante?"
- "¿Cómo solicito una tutoría?"
