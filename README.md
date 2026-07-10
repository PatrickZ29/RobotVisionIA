# Juez Logit  
### Sistema Inteligente de Arbitraje para Combates de Robótica

[![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)]()  
[![Backend](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)  
[![IA](https://img.shields.io/badge/IA-Gemini_API-4285F4?style=for-the-badge)]()  
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql)]()  
[![Hardware](https://img.shields.io/badge/Hardware-Raspberry_Pi_Zero_2W-C51A4A?style=for-the-badge&logo=raspberry-pi)]()  
[![M5Stack](https://img.shields.io/badge/M5Stack-ESP--NOW-orange?style=for-the-badge)]()  

---

## Descripción

**Juez Logit** es un sistema inteligente de apoyo al arbitraje para combates de robótica. Su objetivo es reducir la subjetividad en la toma de decisiones mediante el análisis de video, imágenes iniciales y finales de los robots, y criterios técnicos de evaluación.

El sistema permite registrar la batalla, enviar el video al backend, procesar la evidencia con inteligencia artificial y generar un resultado estructurado con el ganador, puntuaciones y justificación técnica. La decisión final puede ser utilizada como apoyo para el juez humano durante competencias de robótica de combate.

El proyecto integra una arquitectura compuesta por backend web, análisis con IA, almacenamiento de resultados, captura de video mediante Raspberry Pi, módulos físicos con M5Stack y un reloj digital para el control del tiempo de batalla.

---

## Capturas del sistema

<p align="center">
  <img src="assets/ui-main.png" width="60%">
</p>

<p align="center">
  <em>Interfaz principal del sistema Juez Logit</em>
</p>

<p align="center">
  <img src="assets/ui-results.png" width="80%">
</p>

<p align="center">
  <em>Visualización del resultado generado por la inteligencia artificial</em>
</p>

---

## Características principales

- Grabación de video mediante Raspberry Pi Zero 2 W.
- Control remoto de inicio, pausa, reanudación y detención de grabación.
- Carga manual o automática de videos de batalla.
- Análisis de video e imágenes mediante Gemini API.
- Evaluación por criterios técnicos: agresividad, condición, daño y control.
- Identificación de robots por nombre e imágenes de referencia.
- Exclusión del robot observador Juez Bot durante el análisis.
- Interfaz web desarrollada con HTML, CSS, JavaScript y Jinja2.
- Historial de batallas almacenado en PostgreSQL.
- Módulos físicos con M5Stack y comunicación ESP-NOW.
- Reloj del juez desarrollado en PyQt5 con comunicación serial USB.

---

## Arquitectura del sistema

<p align="center">
  <img src="assets/Aquitectura.png" width="650">
</p>

<p align="center">
  <em>Arquitectura general del sistema Juez Logit</em>
</p>

El sistema se organiza en los siguientes módulos:

1. **Cliente de captura:** Raspberry Pi Zero 2 W con cámara USB para grabar la batalla.
2. **Backend:** API desarrollada con FastAPI para recibir videos, controlar la grabación y procesar solicitudes.
3. **Servicio de IA:** integración con Gemini API para analizar video e imágenes.
4. **Base de datos:** PostgreSQL para almacenar historial de batallas y resultados.
5. **Interfaz web:** formulario para cargar evidencias, visualizar resultados y consultar historial.
6. **Módulos físicos:** dispositivos M5Stack para botones de estado y control del árbitro.
7. **Reloj del juez:** temporizador independiente desarrollado con PyQt5.

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Backend | FastAPI + Uvicorn |
| Frontend | HTML5, CSS3, JavaScript |
| Plantillas | Jinja2 |
| Inteligencia artificial | Gemini API |
| Base de datos | PostgreSQL |
| Cliente HTTP | Requests / HTTPX |
| Variables de entorno | python-dotenv |
| Captura de video | Raspberry Pi Zero 2 W + cámara USB |
| Procesamiento de video | FFmpeg |
| Módulos físicos | M5Stack Core2 + ESP-NOW |
| Reloj del juez | PyQt5 + comunicación serial |
| Despliegue | Render |

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/PatrickZ29/RobotVisionIA.git
cd RobotVisionIA
```

Crear y activar un entorno virtual:

```bash
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

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración de variables de entorno

Crear un archivo `.env` en la raíz del backend con la siguiente estructura:

```env
GEMINI_API_KEY=coloca_tu_api_key_aqui
GEMINI_MODEL=gemini-3.1-flash-lite

VIDEO_FOLDER=videos

DB_HOST=localhost
DB_PORT=5432
DB_NAME=robot_ai
DB_USER=postgres
DB_PASSWORD=1234
```

Para despliegue en Render o servicios similares, se puede utilizar:

```env
DATABASE_URL=postgresql://usuario:password@host:5432/base_datos
```

> No se recomienda subir archivos `.env` ni claves privadas al repositorio.

---

## Ejecución del backend

Ejecutar la aplicación con Uvicorn:

```bash
uvicorn main:app --reload
```

Abrir en el navegador:

```text
http://localhost:8000
```

Para verificar el estado del servidor:

```text
http://localhost:8000/health
```

---

## Flujo de funcionamiento

1. El juez inicia la grabación desde la interfaz web o módulo físico.
2. La Raspberry Pi consulta el estado del servidor.
3. La cámara graba la batalla en formato MP4.
4. El video se envía al backend mediante el endpoint `/upload`.
5. El usuario carga o confirma las evidencias en la interfaz web.
6. El backend envía el video e imágenes a Gemini API.
7. La IA analiza la batalla con base en criterios técnicos.
8. El sistema extrae el ganador y las puntuaciones.
9. El resultado se almacena en PostgreSQL.
10. La interfaz muestra el ganador, tiempo de procesamiento y análisis técnico.

---

## Motor de evaluación

El sistema evalúa a cada robot con una puntuación máxima de 40 puntos.

| Criterio | Puntaje máximo | Descripción |
|---|---:|---|
| Agresividad | 15 | Iniciativa ofensiva, presión y búsqueda de contacto. |
| Condición | 5 | Estado físico y funcional al finalizar la batalla. |
| Daño | 10 | Daño visible causado al oponente. |
| Control | 10 | Dominio de arena, orientación, empuje y posición táctica. |

El ganador se determina por el puntaje total. En caso de igualdad, se aplica desempate por daño, agresividad, control y condición. El empate solo se considera cuando no existe contacto efectivo, daño, control ni presión ofensiva clara.

---

## Ejemplo de resultado

```text
GANADOR: Robot A
```

| Robot A | Puntaje |
|---|---:|
| Agresividad | 12 |
| Condición | 4 |
| Daño | 8 |
| Control | 7 |
| Total | 31 |

| Robot B | Puntaje |
|---|---:|
| Agresividad | 8 |
| Condición | 2 |
| Daño | 5 |
| Control | 6 |
| Total | 21 |

---

## API Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/` | GET | Muestra la interfaz principal. |
| `/health` | GET | Verifica el estado del backend. |
| `/upload` | POST | Permite subir el video grabado por la Raspberry Pi. |
| `/analyze` | POST | Analiza el video e imágenes con inteligencia artificial. |
| `/historial` | GET | Consulta los últimos resultados almacenados. |
| `/check_status` | GET | Verifica si existe un video disponible para analizar. |
| `/start_recording` | GET | Inicia la grabación remota. |
| `/pause_recording` | GET | Pausa la grabación remota. |
| `/resume_recording` | GET | Reanuda la grabación remota. |
| `/stop_recording` | GET | Detiene la grabación remota. |
| `/recording_status` | GET | Consulta el estado actual de grabación. |

---

## Estructura del proyecto

```text
juez-logit/
│
├── main.py                         # Punto de entrada del backend
├── config.py                       # Configuración general del sistema
├── database.py                     # Conexión y operaciones con PostgreSQL
├── requirements.txt                # Dependencias del proyecto
├── .env.example                    # Ejemplo de variables de entorno
│
├── routers/
│   └── analyze_router.py           # Endpoints de carga, análisis e historial
│
├── services/
│   ├── gemini_service.py           # Servicio de análisis con Gemini
│   ├── parser_service.py           # Extracción de ganador y puntajes
│   ├── prompt_service.py           # Prompt técnico de evaluación
│   └── video_service.py            # Almacenamiento de videos
│
├── templates/
│   └── index.html                  # Interfaz web del sistema
│
├── videos/                         # Carpeta de videos grabados o cargados
│
├── raspberry/
│   └── raspberry_recording.py      # Captura y envío de video desde Raspberry Pi
│
├── reloj/
│   └── reloj_juez.py               # Reloj del juez con PyQt5
│
└── m5stack/
    ├── botones_competidor_1.py     # Botones de estado del competidor 1
    ├── botones_competidor_2.py     # Botones de estado del competidor 2
    └── modulo_arbitro_core2.py     # Módulo del árbitro en M5Stack Core2
```

---

## Módulos físicos

### Raspberry Pi Zero 2 W

La Raspberry Pi se encarga de capturar el video de la batalla mediante una cámara USB. El script consulta constantemente el estado del backend y ejecuta acciones de grabación según los comandos recibidos:

- Iniciar grabación.
- Pausar grabación.
- Reanudar grabación.
- Detener grabación.
- Unir segmentos de video.
- Enviar video final al backend.

### M5Stack Core2

Los módulos M5Stack se utilizan para la interacción física durante la batalla. El sistema emplea comunicación ESP-NOW para enviar estados entre dispositivos.

Funciones principales:

- Botones de estado para competidores.
- Pantalla de control del árbitro.
- Indicadores visuales de alerta.
- Envío de comandos de inicio y pausa.
- Comunicación con el módulo receptor.

### Reloj del juez

El reloj del juez fue desarrollado con PyQt5 y comunicación serial USB. Permite mostrar el tiempo restante de la batalla y controlar el temporizador mediante comandos externos.

Funciones:

- Inicio del temporizador.
- Pausa del temporizador.
- Reinicio manual.
- Visualización flotante sobre otras ventanas.
- Cambio visual al finalizar el tiempo.

---

## Despliegue

El backend puede desplegarse en Render como servicio web Python.

Comando de inicio recomendado:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Variables necesarias en el entorno de producción:

```env
GEMINI_API_KEY=clave_de_gemini
GEMINI_MODEL=gemini-3.1-flash-lite
DATABASE_URL=url_de_postgresql
VIDEO_FOLDER=videos
```

---

## Seguridad

Para evitar exposición de información sensible:

- No subir el archivo `.env`.
- No subir claves de Gemini al repositorio.
- No incluir credenciales reales en `config.py`.
- Usar variables de entorno para producción.
- Mantener `videos/`, `uploads/` y archivos temporales fuera de Git.

Ejemplo de `.gitignore`:

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

---

## Futuras mejoras

- [ ] Integrar detección automática de eventos importantes durante la batalla.
- [ ] Añadir transmisión en vivo del combate.
- [ ] Incorporar sensores de impacto o telemetría.
- [ ] Implementar dashboard con estadísticas de robots.
- [ ] Crear sistema de ranking de competidores.
- [ ] Añadir soporte para aplicación móvil.
- [ ] Comparar resultados entre diferentes modelos de inteligencia artificial.
- [ ] Mejorar el análisis en tiempo real con múltiples cámaras.

---

## Autor

**Patrick Neil Zamora Lascano**  
Universidad Tecnológica Indoamérica  
Carrera de Ingeniería en Tecnologías de la Información  

---

## Licencia

Este proyecto fue desarrollado con fines académicos como parte del trabajo de titulación relacionado con el sistema inteligente de arbitraje para robótica de combate.
