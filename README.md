# Rappi Store Availability Dashboard

Dashboard interactivo para monitorear la disponibilidad de puntos de venta Rappi, construido con Streamlit y Python.

---

## Requisitos previos

- Python 3.9 o superior
- Una API key de [Groq](https://console.groq.com) (gratuita)
- Los archivos de datos CSV en tu máquina local

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JuanGonzalez2811/Rappi-dashboard.git
cd Rappi-dashboard
```

### 2. Crear un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar los datos

Los archivos CSV deben ubicarse en:

```
~/Downloads/Archivo/AVAILABILITY-data*.csv
```

Si tus archivos están en otra ruta, edita la variable `DATA_DIR` en `data_loader.py`:

```python
DATA_DIR = "/ruta/a/tu/carpeta"
```

### 5. Configurar la API key de Groq

Crea el archivo `.streamlit/secrets.toml` a partir del ejemplo incluido:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Abre el archivo y reemplaza el valor con tu key real:

```toml
GROQ_API_KEY = "gsk_tu_key_aqui"
```

> ⚠️ Este archivo está en `.gitignore` y nunca debe subirse al repositorio.

---

## Ejecutar el dashboard

```bash
streamlit run app.py
```

El dashboard abrirá automáticamente en `http://localhost:8501`.

---

## Despliegue en Streamlit Cloud (acceso remoto)

Para que otros usuarios accedan sin instalar nada:

1. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu cuenta de GitHub
2. Selecciona el repositorio `Rappi-dashboard` y el archivo `app.py`
3. En **Advanced settings → Secrets**, añade:
   ```toml
   GROQ_API_KEY = "gsk_tu_key_aqui"
   ```
4. Haz clic en **Deploy** — recibirás una URL pública compartible

---

## Estructura del proyecto

```
Rappi-dashboard/
├── app.py                          # Interfaz principal del dashboard
├── data_loader.py                  # Carga y procesamiento de archivos CSV
├── chatbot.py                      # Asistente IA (Llama 3.3 70B via Groq)
├── requirements.txt                # Dependencias Python
└── .streamlit/
    └── secrets.toml.example        # Plantilla para configurar la API key
```

---

## Funcionalidades

- **Tendencia** — línea de tiempo con media móvil de disponibilidad de tiendas
- **Patrones** — promedios por hora, día de semana y heatmap horario
- **Por día** — estadísticas diarias con tabla de detalle
- **Asistente IA** — chat en español para consultar los datos, powered by Llama 3.3 70B

---

## Datos

Métrica `synthetic_monitoring_visible_stores` — mide cada 10 segundos cuántos puntos de venta Rappi son visibles para los usuarios. Dataset: febrero 1–11, 2026.
