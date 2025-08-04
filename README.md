# Sentinel OS Agent API

## Descripción

Este proyecto implementa una API en FastAPI para recibir, almacenar y consultar información de agentes que recopilan datos del sistema operativo. El agente envía información sobre el procesador, procesos en ejecución, usuarios con sesión abierta y detalles del sistema operativo. Los datos se almacenan en una base de datos SQLite utilizando SQLAlchemy.

## Estructura del Proyecto

```
os-agent/
├── src/
│   ├── agent/agent.py           # Script del agente para recopilar y enviar datos
│   └── api/
│       ├── app/
│       │   ├── main.py          # Endpoints de la API
│       │   ├── database.py      # Configuración de SQLAlchemy
│       │   ├── models.py        # Modelos de la base de datos
│       │   ├── schemas.py       # Modelos Pydantic para validación
│       │   ├── crud.py          # Lógica de interacción con la base de datos
│       ├── requirements.txt     # Dependencias de la API
│       └── Dockerfile           # Imagen Docker para la API
```

## Instalación

### Requisitos

- Python 3.11
- Docker (opcional)

### Instalación manual

1. Clona el repositorio.
2. Instala las dependencias de la API:
    ```bash
    cd src/api
    pip install -r requirements.txt
    ```
3. Inicializa la base de datos (opcional, se crea automáticamente al ejecutar la API).

### Instalación con Docker

1. Construye la imagen:
    ```bash
    docker build -t sentinel-api .
    ```
2. Ejecuta el contenedor:
    ```bash
    docker run -p 5000:5000 sentinel-api
    ```

## Uso

### Ejecutar la API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

### Endpoints

- **POST /api/agent_data**  
  Recibe datos del agente en formato JSON.  
  Ejemplo de estructura:
  ```json
  {
    "cpu_info": {
      "physical_cores": 4,
      "total_cores": 8,
      "max_frequency": 3500.0,
      "current_frequency": 3200.0,
      "cpu_usage_percent": 12.5
    },
    "processes": [
      {"pid": 1, "name": "systemd", "username": "root"}
    ],
    "users": [
      {"name": "user", "terminal": "pts/0", "host": "192.168.1.10", "started": 1627891234.0}
    ],
    "os_info": {
      "system": "Linux",
      "version": "5.15.0-75-generic",
      "hostname": "mi-servidor"
    }
  }
  ```

- **GET /api/agent_data**  
  Consulta los datos almacenados.  
  Permite filtrar por IP del cliente:
  ```
  /api/agent_data?client_ip=192.168.1.10
  ```

## Agente

El agente (`agent.py`) recopila información del sistema y la envía a la API.  
Configura la variable de entorno `API_TOKEN` antes de ejecutar el agente:

```bash
export API_TOKEN="tu_token"
python src/agent/agent.py
```

## Licencia

Consulta el archivo LICENSE para detalles de la licencia.

## Autores

Consulta el archivo AUTHORS para la lista