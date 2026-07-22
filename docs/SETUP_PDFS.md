# ✅ PASOS PARA AGREGAR LOS 2 NUEVOS PDFs

## Estado Actual
```
❌ guía_del_docente_eva_periodo_p37.pdf         (FALTA)
❌ guía_del_estudiante_eva_periodo_p37.pdf      (FALTA)
✅ calendario_academico_ejemplo.pdf             (Ya existe)
✅ reglamento_academico_ejemplo.pdf             (Ya existe)
```

## 📋 Instrucciones

### Opción A: Copiar desde VS Code (RECOMENDADO)

1. **Descarga los PDFs** que compartiste en la conversación
   - `GUÍA DEL DOCENTE_EVA_PERIODO P37` 
   - `GUÍA DEL ESTUDIANTE_EVA_PERIODO P37`

2. **Abre el Explorador de archivos** en Windows
   - Navega a: `c:\proyecto_istte\rag-istte-widget\data\reglamentos\`

3. **Copia los PDFs** a esa carpeta

4. **Asegúrate que los nombres sean exactos:**
   ```
   guía_del_docente_eva_periodo_p37.pdf
   guía_del_estudiante_eva_periodo_p37.pdf
   ```
   
   ⚠️ Nota: Los nombres deben tener las tildes (á, é, í, ó, ú)

5. **Verifica en VS Code**
   - Abre la terminal en VS Code
   - Ejecuta:
     ```bash
     python scripts/manage_pdfs.py check
     ```
   - Deberías ver "✅" al lado de ambos archivos

### Opción B: Usar el Explorador de VS Code

1. En VS Code, haz clic derecho en la carpeta `data/reglamentos/`
2. Selecciona "Abrir en el Explorador de archivos"
3. Copia los PDFs descargados a esa carpeta

---

## 🚀 Una vez copiad los PDFs

### Paso 1: Verifica que están en la carpeta

```bash
python scripts/manage_pdfs.py check
```

**Resultado esperado:**
```
✅ guía_del_docente_eva_periodo_p37.pdf
✅ guía_del_estudiante_eva_periodo_p37.pdf
```

### Paso 2: Ejecuta la ingesta

```bash
python scripts/ingest.py
```

**Espera a que termine** (puede tomar 2-5 minutos dependiendo del tamaño)

**Resultado esperado:**
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

### Paso 3: El servidor se recargará automáticamente

Espera a ver en el terminal:
```
INFO:     Application startup complete.
```

---

## 🧪 Pruebas después de la ingesta

Ve al navegador: **http://127.0.0.1:8000/widget/**

Prueba estas preguntas:

1. **"¿Cómo accedo a Tu Aula Virtual ISTTE?"**
   - Debe mencionar: https://eva.tecnovirtual.edu.ec/my/

2. **"¿Cuáles son los bloques de aprendizaje?"**
   - Debe mencionar: Generalidades, Unidades de Estudio, Actividades, Evaluaciones

3. **"¿Cuáles son los pasos para cargar una actividad?"**
   - Debe mencionar los 7 pasos del procedimiento

4. **"¿Qué es el Portafolio del Estudiante?"**
   - Debe mencionar: Recolectar evidencias de aprendizaje

---

## 🆘 Si algo sale mal

### Los PDFs no aparecen en la carpeta
- Verifica que los descargaste en la carpeta correcta
- Comprueba que tengas permisos de escritura
- Abre una terminal en Windows y copia manualmente:
  ```powershell
  Copy-Item "ruta\del\descarga\guía*.pdf" "c:\proyecto_istte\rag-istte-widget\data\reglamentos\"
  ```

### El script ingest.py tiene errores
- Verifica que Ollama esté corriendo (modelos nomic-embed-text y llama3.2)
- Ejecuta: `ollama ls`
- Si faltan modelos, descárgalos:
  ```bash
  ollama pull nomic-embed-text
  ollama pull llama3.2
  ```

### El asistente no responde con información de los nuevos PDFs
- Verifica que la ingesta completó sin errores
- Borra la carpeta `chroma_db/` y vuelve a ejecutar `ingest.py`
- Reinicia el servidor

---

## 📊 Información de lo que se ingesta

| Documento | Páginas | Contenido |
|-----------|---------|----------|
| Guía Docente | 7 | Estructura del aula, componentes, actividades |
| Guía Estudiante | 8 | Acceso, navegación, procedimientos, tutorías |
| Calendario Académico | ? | Fechas importantes, horarios |
| Reglamento Académico | ? | Normas y políticas |

**Total esperado: ~70-100 fragmentos de texto enriquecidos**
