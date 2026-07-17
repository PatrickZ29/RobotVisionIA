🥊 Juez Bot
### Sistema Multimodal Integrado para Arbitraje Asistido por IA en Robótica de Combate

[![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)]()
[![Backend](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![IA](https://img.shields.io/badge/IA-Gemini_2.5_Flash-4285F4?style=for-the-badge)]()
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql)]()
[![Hardware](https://img.shields.io/badge/Hardware-Raspberry_Pi_Zero_2W-C51A4A?style=for-the-badge&logo=raspberry-pi)]()
[![M5Stack](https://img.shields.io/badge/M5Stack-ESP--NOW-orange?style=for-the-badge)]()
[![Paper](https://img.shields.io/badge/IEEE_Access-Publicado-00629B?style=for-the-badge)]()

---

## 📌 Descripción del Proyecto

**Juez Bot** es un sistema multimodal integrado de apoyo al arbitraje para combates de robótica, publicado como artículo científico en *IEEE Access*. Su objetivo es reducir la subjetividad en la toma de decisiones cuando un combate no termina por *knockout* (KO) o rendición, combinando terminales de campo, un módulo portátil de árbitro, un temporizador oficial, una unidad móvil de captura, una aplicación web, un backend, una base de datos y un servicio de inferencia multimodal en un flujo de trabajo trazable.

El sistema conserva las puntuaciones de agresividad, condición, daño y control para ambos robots, junto con el ganador propuesto y una justificación técnica, siempre sujeta a confirmación humana del árbitro (*human-in-the-loop*).

---

## 🖼️ Vista Rápida del Sistema

<p align="center">
  <img src="assets/demo.gif" width="80%" alt="Demostración GIF del sistema Juez Bot">
</p>

<p align="center">
  <a href="https://youtu.be/RK5Msci8DQw" target="_blank">
    <img src="https://img.youtube.com/vi/RK5Msci8DQw/hqdefault.jpg" width="75%" alt="Video demostrativo de Juez Bot">
  </a>
</p>

<p align="center"><em>Video demostrativo completo del funcionamiento del sistema</em></p>

---

## 🔌 Arquitectura del Sistema

<p align="center">
  <img src="assets/architecture.png" width="85%" alt="Arquitectura por capas de Juez Bot">
</p>
<p align="center"><em>Figura 1. Arquitectura por capas: dispositivos de campo, captura, servicios, persistencia e inferencia con IA.</em></p>

El sistema se organiza en siete capas, diseñadas para reducir el acoplamiento entre dispositivos y permitir reemplazar componentes sin modificar todo el flujo:

| Capa | Componente | Tecnología | Responsabilidad principal |
|---|---|---|---|
| Operadores | Terminal A y Terminal B | AtomS3, botones físicos | Confirmar estado *listo*, solicitar intervención y transmitir eventos al árbitro |
| Control de árbitro | Módulo de árbitro | M5Stack Core2, UIFlow, MicroPython | Iniciar, pausar, reanudar y detener el combate; recibir estados y mostrar alertas |
| Temporización | Temporizador oficial | Python, PyQt5 | Mostrar el tiempo reglamentario y ejecutar comandos del módulo de árbitro |
| Adquisición | Juez Bot (unidad móvil) | Sphero RVR+, Raspberry Pi Zero 2 W, cámara, FFmpeg | Capturar video, controlar segmentos de grabación y transferir el archivo al backend |
| Servicios | Backend | FastAPI, Uvicorn, Pydantic, HTTPX | Exponer endpoints, validar solicitudes y coordinar archivos, inferencia y persistencia |
| Presentación | Aplicación web | Jinja2, HTML, CSS, JavaScript | Registrar robots, cargar imágenes, ejecutar análisis, consultar historial |
| Persistencia | Base de datos | PostgreSQL, psycopg2 | Almacenar combates, evidencia, tiempos de proceso, puntuaciones y decisiones |
| Inferencia | Motor multimodal | Gemini 2.5 Flash vía REST API | Evaluar video e imágenes de referencia según los criterios de arbitraje |

---

## 🏟️ Disposición Física en la Arena

<p align="center">
  <img src="assets/arena-layout.png" width="75%" alt="Disposición física de los módulos en la arena de combate">
</p>
<p align="center"><em>Figura 2. Ubicación de terminales de operador, Juez Bot (unidad móvil de cámara), estación del árbitro y temporizador oficial, con enlaces ESP-NOW.</em></p>

- Los dos **terminales de operador** se ubican en las esquinas externas de la arena.
- **Juez Bot**, la unidad móvil de captura (Sphero RVR+ + Raspberry Pi Zero 2 W + cámara), se posiciona en una esquina interna con línea de visión sobre todo el combate.
- El **módulo de árbitro** (M5Stack Core2) y el **temporizador oficial** se ubican junto a la estación del árbitro, conectados por comunicación serial.
- Todos los enlaces de campo usan **ESP-NOW**, sin depender de la red WiFi local.

---

## 🧠 Flujo de Inferencia Multimodal

<p align="center">
  <img src="assets/inference-workflow.png" width="70%" alt="Flujo de inferencia multimodal de Juez Bot">
</p>
<p align="center"><em>Figura 3. Etapas de inferencia: validación de evidencia, codificación, construcción del prompt, evaluación por rúbrica, persistencia y confirmación del árbitro.</em></p>

1. **Validación de entrada** — se verifica disponibilidad y tipo de video/imágenes.
2. **Codificación de medios** — el video se codifica para su transmisión al servicio multimodal.
3. **Construcción del prompt** — identificación inequívoca de robots, reglas del área e instrucciones de comparación.
4. **Inferencia multimodal con IA** — Gemini 2.5 Flash evalúa el combate completo.
5. **Análisis estructurado de la respuesta** — validación por expresiones regulares y rangos.
6. **Extracción de criterios** — agresividad, daño, control y condición.
7. **Propuesta de ganador**.
8. **Persistencia** — en PostgreSQL, con la respuesta original íntegra para trazabilidad.
9. **Presentación web** del resultado.
10. **Confirmación del árbitro** — decisión final humana.

---

## 🧩 Tecnologías Utilizadas

| Tecnología | Versión | Aplicación |
|---|---|---|
| Python | 3.x | Captura, temporización y backend |
| FastAPI | 0.136.1 | API REST asíncrona |
| Uvicorn | 0.46.0 | Servidor ASGI |
| Pydantic | 2.13.4 | Validación de datos |
| Jinja2 | 3.1.6 | Renderizado de la interfaz |
| PostgreSQL | 9.4 | Persistencia |
| psycopg2 | 2.9.12 | Conexión SQL |
| Gemini | 2.5 Flash | Inferencia multimodal |
| HTTPX | 0.28.1 | Comunicación entre servicios |
| M5Stack AtomS3 / Core2 | — | Terminales de operador y módulo de árbitro |
| ESP-NOW | — | Comunicación inalámbrica de campo |
| Sphero RVR+ | — | Plataforma móvil de la unidad de captura |
| FFmpeg | — | Codificación de video (H.264, MP4) |
| PyQt5 | — | Reloj del juez con comunicación serial |
| Render | — | Despliegue del backend |

---

## 🚀 Funcionalidades Principales

| Funcionalidad | Descripción |
|---|---|
| 🎥 Captura móvil | Grabación de combate mediante Sphero RVR+ + Raspberry Pi Zero 2 W + cámara. |
| 🔴 Control remoto de grabación | Inicio, pausa, reanudación y detención sincronizados con el árbitro. |
| 🤖 Análisis multimodal | Evaluación de video e imágenes iniciales/finales mediante Gemini 2.5 Flash. |
| 🥋 Evaluación por rúbrica | Puntuación técnica en agresividad, condición, daño y control. |
| 🏷️ Identificación de robots | Reconocimiento inequívoco de Robot A / Robot B por nombre e imágenes. |
| 🖥️ Interfaz web | Registro de robots, carga de evidencia, resultados y verificación técnica. |
| 🗄️ Historial trazable | Registro completo en PostgreSQL, incluida la respuesta original del modelo. |
| 📡 Módulos físicos | Terminales AtomS3 y módulo árbitro M5Stack Core2 vía ESP-NOW. |
| ⏱️ Reloj oficial | Temporizador independiente en PyQt5 con comandos seriales. |
| 🧑‍⚖️ Árbitro en el bucle | El sistema propone; el árbitro humano confirma o corrige la decisión final. |

---

## 🚦 Motor de Evaluación

Cada robot se evalúa con un puntaje máximo de **40 puntos**:

| Criterio | Puntaje máximo | Descripción |
|---|---:|---|
| Agresividad | 15 | Iniciativa ofensiva, presión y búsqueda de contacto. |
| Condición | 5 | Estado físico y funcional al finalizar el combate. |
| Daño | 10 | Daño visible causado al oponente. |
| Control | 10 | Dominio de arena, orientación, empuje y posición táctica. |

El ganador se determina por puntaje total; en caso de igualdad se aplica desempate por daño → agresividad → control → condición. El empate solo se considera cuando no hay contacto efectivo ni presión ofensiva clara.

---

## 📊 Resultados de Validación (IEEE Access)

Validado en dos escenarios: 30 combates históricos del repositorio **BrettZone-NHRL** y 20 combates con decisión de jueces del evento **IEEE Pumabot 2026**.

| Escenario | n | Precisión (Acc.) | IC 95% (Wilson) | Bal. Acc. | Macro F1 | MCC |
|---|---:|---:|---|---:|---:|---:|
| BrettZone–NHRL | 30 | 86.7% | 70.3–94.7% | 86.1% | 86.1% | 0.722 |
| IEEE Pumabot 2026 | 20 | 90.0% | 69.9–97.2% | 89.0% | 89.0% | 0.780 |
| **Combinado** | 50 | **88.0%** | 76.2–94.4% | 87.3% | 87.3% | 0.745 |

### 🎯 Matriz de confusión combinada

| | Predicho A | Predicho B |
|---|---:|---:|
| **Oficial A** | 28 | 3 |
| **Oficial B** | 3 | 16 |

Los errores fueron simétricos (3 en cada dirección), sin evidencia de sesgo posicional hacia A o B.

### ⚖️ Contribución normalizada de criterios (dataset combinado)

| Criterio | Contribución |
|---|---:|
| Control | 33.6% |
| Agresividad | 32.3% |
| Daño | 21.7% |
| Condición | 12.4% |

El margen promedio entre puntajes fue de **14.80 puntos**. Cinco de los seis desacuerdos tuvieron márgenes ≥11 puntos, lo que confirma que un margen amplio **no** debe interpretarse como confianza calibrada — de ahí la importancia de mantener al árbitro en el bucle de decisión.

### 🗳️ Pruebas funcionales end-to-end

| Código | Prueba | Resultado documentado |
|---|---|---|
| F1 | Señalización de operadores | Estados y alertas mostrados en el M5Stack Core2 |
| F2 | Control del temporizador | Comandos seriales interpretados correctamente por el reloj PyQt5 |
| F3 | Sincronización de captura | Grabación (inicio/pausa/reanuda/detiene) verificada |
| F4 | Transferencia de evidencia | Videos e imágenes recibidos sin errores críticos |
| F5 | Inferencia multimodal | Respuesta con ganador y puntajes técnicos recibida y mostrada |
| F6 | Persistencia e historial | Resultados almacenados en PostgreSQL y consultables |
| F7 | Despliegue en evento | Operación conjunta de módulos físicos y lógicos durante IEEE Pumabot 2026 |

---

## 📡 Comunicación entre Módulos

| Origen | Destino | Canal | Datos | Propósito |
|---|---|---|---|---|
| Terminales A/B | Módulo de árbitro | ESP-NOW | Códigos de listo, alerta o rendición | Coordinar estado del competidor y solicitar intervención |
| Módulo de árbitro | Temporizador oficial | Serial | Inicio, pausa, reanudación, detención | Controlar el tiempo reglamentario desde el dispositivo portátil |
| Backend | Juez Bot | HTTP GET | Estados de grabación y pausa | Sincronizar captura con acciones del árbitro |
| Juez Bot | Backend | HTTP multipart | Video MP4 y metadatos | Transferir evidencia audiovisual |
| Aplicación web | Backend | HTTP multipart | Identificadores, video, imágenes iniciales/finales | Registrar el combate y solicitar inferencia |
| Backend | Servicio de IA | HTTPS / JSON | Instrucciones y archivos codificados | Ejecutar el análisis multimodal |
| Backend | PostgreSQL | SQL | Evidencia, puntajes, tiempos, estados | Garantizar persistencia y trazabilidad |
| Backend | Aplicación web | HTTP / JSON | Resultado, explicación, historial | Apoyar revisión y confirmación del árbitro |

---

## 🔄 Secuencia Operativa

1. Cada operador confirma que su robot está listo.
2. Cuando ambos estados son válidos, el árbitro inicia el temporizador y la grabación.
3. Durante el combate, los terminales pueden enviar alertas; el árbitro puede pausar o detener.
4. Al finalizar, Juez Bot transfiere el video y se agregan las imágenes finales disponibles.
5. El backend valida la evidencia y construye la solicitud multimodal.
6. Si hay KO o rendición confirmados, se aplica la **regla directa** (sin pasar por el modelo de IA).
7. Si el combate llega al límite de tiempo, se ejecuta el **análisis multimodal**.
8. El sistema extrae el ganador propuesto y las puntuaciones por criterio.
9. El resultado se almacena en PostgreSQL junto con la respuesta original del modelo.
10. La interfaz presenta el resultado; el árbitro confirma o corrige la decisión final.

### 🔁 Modelo de estados del combate

`waiting` → `ready` → `recording` ⇄ `paused` → `finished` → `processing` → `result available` → `validated`

---

## 🌐 API Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/` | GET | Muestra la interfaz principal. |
| `/health` | GET | Verifica el estado del backend. |
| `/upload` | POST | Sube el video grabado por Juez Bot. |
| `/analyze` | POST | Analiza video e imágenes con IA multimodal. |
| `/historial` | GET | Consulta los últimos resultados almacenados. |
| `/check_status` | GET | Verifica si existe un video disponible para analizar. |
| `/start_recording` | GET | Inicia la grabación remota. |
| `/pause_recording` | GET | Pausa la grabación remota. |
| `/resume_recording` | GET | Reanuda la grabación remota. |
| `/stop_recording` | GET | Detiene la grabación remota. |
| `/recording_status` | GET | Consulta el estado actual de grabación. |

---

## ⚙️ Instalación

```bash
git clone https://github.com/PatrickZ29/RobotVisionIA.git
cd RobotVisionIA
python -m venv venv
```

En Windows:
```bash
venv\Scripts\activate
```

En Linux o macOS:
```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuración de Variables de Entorno

```env
GEMINI_API_KEY=coloca_tu_api_key_aqui
GEMINI_MODEL=gemini-2.5-flash

VIDEO_FOLDER=videos

DB_HOST=localhost
DB_PORT=5432
DB_NAME=robot_ai
DB_USER=postgres
DB_PASSWORD=1234
```

Para despliegue en Render o servicios similares:
```env
DATABASE_URL=postgresql://usuario:password@host:5432/base_datos
```

> ⚠️ No se recomienda subir archivos `.env` ni claves privadas al repositorio.

---

## ▶️ Ejecución del Backend

```bash
uvicorn main:app --reload
```

```text
http://localhost:8000
http://localhost:8000/health
```

---

## ☁️ Despliegue

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

```env
GEMINI_API_KEY=clave_de_gemini
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=url_de_postgresql
VIDEO_FOLDER=videos
```

---

## 🛡️ Seguridad

```gitignore
venv/
.env
__pycache__/
*.pyc
uploads/
videos/
*.log
.DS_Store
.api_keys.py
```

- No subir `.env` ni claves de Gemini al repositorio.
- No incluir credenciales reales en `config.py`.
- Mantener `videos/`, `uploads/` y archivos temporales fuera de Git.

---

## 🌱 Limitaciones y Trabajo Futuro

- [ ] Cámaras sincronizadas para asociar cada criterio con evidencia temporal específica.
- [ ] Inferencia repetida para medir estabilidad y calibración de confianza.
- [ ] Comparación entre modelos y prompts (arbitraje por comité, ej. estilo EvalCouncil).
- [ ] Inferencia parcial en el borde (*edge*) para reducir dependencia de Internet.
- [ ] Esquemas JSON validados para respuestas del modelo.
- [ ] Evaluación de disponibilidad, pérdida de paquetes ESP-NOW y costo por combate.
- [ ] Mecanismos de apelación y revisión comprensibles para competidores y organizadores.

---

## 📄 Publicación Científica

Este proyecto fue publicado como artículo en **IEEE Access**:

> *An Integrated Multimodal System for AI-Assisted Refereeing in Combat Robotics*
> Patrick Zamora, Steven Curipallo, José Varela-Aldás — Centro de Investigación MIST, Universidad Tecnológica Indoamérica, Ambato, Ecuador.
> DOI: 10.1109/ACCESS.2026.XXXXXXX

---

## 👤 Autor

**Patrick Neil Zamora Lascano**
Universidad Tecnológica Indoamérica
Carrera de Ingeniería en Tecnologías de la Información

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos como parte del trabajo de titulación relacionado con el sistema inteligente de arbitraje para robótica de combate, validado durante el evento **IEEE Pumabot 2026**.

⭐ Proyecto académico de IA multimodal aplicada, IoT y arbitraje deportivo inteligente
