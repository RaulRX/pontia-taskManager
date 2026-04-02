# Task Management API

API REST para la gestion de notas/tareas desarrollada con **FastAPI**, **SQLAlchemy** y **SQLite**. Permite crear, consultar, modificar y eliminar notas con fecha de vencimiento, control de completado y validaciones de contenido.

## Tecnologias

| Tecnologia | Version | Uso |
|---|---|---|
| Python | 3.10+ | Runtime |
| FastAPI | 0.135.1 | Framework web |
| PostgreSQL | 14+ | Base de datos |
| psycopg2 | - | Driver PostgreSQL |
| SQLAlchemy | 2.0.48 | ORM (implementacion SQLite alternativa) |
| Pydantic | 2.12.5 | Validacion de schemas |
| Uvicorn | 0.41.0 | Servidor ASGI |
| Docker Compose | v2 | Orquestacion de servicios |

## Estructura del proyecto

```
TaskManager/
├── src/
│   └── taskmanager/
│       ├── main.py                          # Entry point
│       ├── api/
│       │   ├── Routers.py                   # Registro de rutas
│       │   ├── endpoints/
│       │   │   └── Notes_controller.py      # Controlador REST
│       │   ├── handler/
│       │   │   └── Exceptions.py            # Handlers globales de excepciones
│       │   └── schemas/
│       │       ├── Request.py               # Schemas de entrada (Pydantic)
│       │       └── Response.py              # Schemas de salida (Pydantic)
│       ├── domain/
│       │   └── Model.py                     # Modelo de dominio (Note)
│       ├── infrastructure/
│       │   ├── Configuration.py             # Configuracion de BD y sesiones
│       │   ├── Entity.py                    # Entidad ORM (Note_entity)
│       │   └── data/
│       │       └── Query.py                 # Queries SQL para PostgreSQL
│       ├── repository/
│       │   ├── INote_repository.py          # Interfaz abstracta del repositorio
│       │   ├── Repository_exception.py      # Excepciones de repositorio
│       │   ├── postgres/
│       │   │   └── Note_repository_impl.py  # Implementacion PostgreSQL (activa)
│       │   └── sqlite/
│       │       └── Note_repository_impl.py  # Implementacion SQLite (alternativa)
│       └── service/
│           ├── Service.py                   # Logica de negocio
│           ├── Service_exception.py         # Excepciones de servicio
│           ├── Note_mapper.py               # Mapper Model <-> Entity
│           └── Utils.py                     # Validaciones auxiliares
├── docker/
│   ├── docker-compose.yaml                  # Orquestacion de servicios
│   └── scripts/
│       └── init.sql                         # Script de inicializacion de PostgreSQL
├── tests/
│   └── test_python.py                       # Tests funcionales
├── Dockerfile
├── .env.example
├── requirements.txt
└── README.md
```

## Instalacion en local

### 1. Requisitos previos

- **Python 3.10** o superior instalado
- **pip** (incluido con Python)
- **Git** (para clonar el repositorio)

### 2. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd TaskManager
```

### 3. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv
```

```bash
# Activar en Windows (CMD)
venv\Scripts\activate

# Activar en Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activar en Linux/Mac
source venv/bin/activate
```

Una vez activado, veras el prefijo `(venv)` en tu terminal.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

Para actualizar las dependencias en el futuro:

```bash
pip install -r requirements.txt --upgrade
```

Para generar un nuevo `requirements.txt` tras instalar paquetes adicionales:

```bash
pip freeze > requirements.txt
```

### 5. Desactivar entorno virtual

```bash
deactivate
```

## Ejecutar la aplicacion

Desde la raiz del proyecto (`TaskManager/`), con el entorno virtual activado:

```bash
python -m src.taskmanager.main
```

La API se levantara en `http://127.0.0.1:8000`.

### Documentacion interactiva

Una vez ejecutando la aplicacion:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Ejecutar con Docker Compose

### Requisitos previos

- **Docker** instalado y en ejecucion
- **Docker Compose** v2 (incluido con Docker Desktop)

### Levantar los servicios

Desde la raiz del proyecto (`TaskManager/`):

```bash
docker compose -f docker/docker-compose.yaml up -d
```

- `-d` ejecuta los contenedores en segundo plano

La API se levantara en `http://localhost:8080`.

### Detener los servicios

```bash
docker compose -f docker/docker-compose.yaml down
```

### Ver logs de la aplicacion

```bash
docker logs task-manager -f
```

---

## Ejecutar tests

Los tests son un script de integracion que usa la libreria `requests` para interactuar con la API. Requieren que la aplicacion este ejecutandose previamente.

```bash
# Terminal 1: levantar la API
python -m src.taskmanager.main

# Terminal 2: ejecutar tests
python -m tests.test_python
```

Si todos los tests pasan, el script imprime `Todos los tests se han completado correctamente`. Si alguno falla, muestra el error de validacion correspondiente.

### Cobertura de los tests

| Codigo HTTP | Caso cubierto |
|---|---|
| `201` | Crear nota con datos validos |
| `200` | Obtener todas, obtener por ID, modificar nota, agregar contenido, eliminar por ID |
| `204` | Eliminar todas las notas, marcar como completada |
| `400` | Modificar nota con deadline en el pasado (validacion de negocio) |
| `404` | Obtener/modificar nota con ID inexistente |
| `422` | Campos faltantes, deadline invalido, ID no numerico, title demasiado largo, content vacio, tipo incorrecto en completed |

### Lista de tests

| Test | Endpoint | Tipo |
|---|---|---|
| `test_cleanup_inicial` | `DELETE /tasks` | Setup |
| `test_crear_nota_ok` | `POST /tasks` | OK |
| `test_crear_nota_ko_campos_faltantes` | `POST /tasks` | KO 422 |
| `test_crear_nota_ko_deadline_invalido` | `POST /tasks` | KO 422 |
| `test_obtener_todas_ok` | `GET /tasks` | OK |
| `test_obtener_por_id_ok` | `GET /tasks/{id}` | OK |
| `test_obtener_por_id_ko_no_existe` | `GET /tasks/{id}` | KO 404 |
| `test_obtener_por_id_ko_id_invalido` | `GET /tasks/{id}` | KO 422 |
| `test_modificar_nota_ok` | `PUT /tasks/{id}` | OK |
| `test_modificar_nota_ko_no_existe` | `PUT /tasks/{id}` | KO 404 |
| `test_modificar_nota_ko_title_largo` | `PUT /tasks/{id}` | KO 422 |
| `test_modificar_nota_ko_deadline_pasado` | `PUT /tasks/{id}` | KO 400 |
| `test_agregar_contenido_ok` | `PATCH /tasks/{id}/content` | OK |
| `test_agregar_contenido_ko_vacio` | `PATCH /tasks/{id}/content` | KO 422 |
| `test_completar_nota_ok` | `PATCH /tasks/{id}/completed` | OK |
| `test_completar_nota_ko_tipo_invalido` | `PATCH /tasks/{id}/completed` | KO 422 |
| `test_notas_expiradas_ok` | `GET /tasks/expirationNotes` | OK |
| `test_eliminar_por_id_ok` | `DELETE /tasks/{id}` | OK |
| `test_eliminar_por_id_ko_invalido` | `DELETE /tasks/{id}` | KO 422 |
| `test_eliminar_todas_ok` | `DELETE /tasks` | OK |

---

## Endpoints

Todos los endpoints estan bajo el prefijo `/tasks` y el tag `tasks`.

---

### POST `/tasks`

Crea una nueva nota.

**Request Body** (`application/json`):

| Campo | Tipo | Obligatorio | Restricciones | Descripcion |
|---|---|---|---|---|
| `title` | `string` | Si | 1-16 caracteres | Titulo de la nota |
| `content` | `string` | Si | 1-255 caracteres | Contenido de la nota |
| `deadline` | `string` | Si | Formato ISO: `YYYY-MM-DD` o `YYYY-MM-DDTHH:MM:SS` | Fecha de vencimiento |

**Ejemplo de request**:

```json
{
  "title": "Mi first note",
  "content": "Dear diary, today i was at home when ....",
  "deadline": "2026-03-21"
}
```

**Respuestas**:

| Codigo | Descripcion |
|---|---|
| `201 Created` | Nota creada correctamente (sin body) |
| `400 Bad Request` | Error de validacion de dominio (`ValueError`) |
| `422 Unprocessable Entity` | Error de validacion de schema (campos faltantes, formato incorrecto, longitud fuera de rango) |

---

### GET `/tasks`

Obtiene todas las notas.

**Request**: Sin parametros.

**Respuesta** (`200 OK`):

```json
{
  "notes": [
    {
      "id": 1,
      "title": "Mi first note",
      "content": "Dear diary, today i was at home when ....",
      "deadline_date": "2026-03-21T00:00:00",
      "completed": false,
      "created_date": "2026-03-24T10:30:00.123456"
    }
  ]
}
```

**Campos de respuesta**:

| Campo | Tipo | Descripcion |
|---|---|---|
| `notes` | `array[NoteResponse]` | Lista de notas |
| `notes[].id` | `int` | Identificador unico |
| `notes[].title` | `string \| null` | Titulo |
| `notes[].content` | `string \| null` | Contenido |
| `notes[].deadline_date` | `string \| null` | Fecha de vencimiento (ISO 8601) |
| `notes[].completed` | `bool` | Si la nota esta completada |
| `notes[].created_date` | `string \| null` | Fecha de creacion (ISO 8601) |

---

### GET `/tasks/expirationNotes`

Obtiene todas las notas cuya fecha de vencimiento ya ha pasado.

**Request**: Sin parametros.

**Respuesta** (`200 OK`):

```json
{
  "notes": [
    {
      "id": 2,
      "title": "Old note",
      "content": "This note has expired",
      "deadline_date": "2025-01-01T00:00:00",
      "completed": false,
      "created_date": "2024-12-01T10:00:00.000000"
    }
  ]
}
```

Devuelve un `NoteListResponse` con las notas cuyo `deadline_date` es anterior a la fecha/hora actual.

---

### GET `/tasks/{id}`

Obtiene una nota por su ID.

**Path Parameters**:

| Parametro | Tipo | Descripcion |
|---|---|---|
| `id` | `int` | ID de la nota |

**Respuesta** (`200 OK`):

```json
{
  "id": 1,
  "title": "Mi first note",
  "content": "Dear diary, today i was at home when ....",
  "deadline_date": "2026-03-21T00:00:00",
  "completed": false,
  "created_date": "2026-03-24T10:30:00.123456"
}
```

**Respuestas de error**:

| Codigo | Descripcion |
|---|---|
| `404 Not Found` | No existe nota con ese ID |
| `422 Unprocessable Entity` | ID no es un entero valido |

---

### PUT `/tasks/{id}`

Modifica una nota existente.

**Path Parameters**:

| Parametro | Tipo | Descripcion |
|---|---|---|
| `id` | `int` | ID de la nota a modificar |

**Request Body** (`application/json`):

| Campo | Tipo | Obligatorio | Restricciones | Descripcion |
|---|---|---|---|---|
| `title` | `string` | Si | 1-16 caracteres | Nuevo titulo |
| `content` | `string` | Si | 1-255 caracteres | Nuevo contenido |
| `deadline` | `string` | Si | Formato ISO (acepta timezone) | Nueva fecha de vencimiento |

**Ejemplo de request**:

```json
{
  "title": "Updated note",
  "content": "New content for this note",
  "deadline": "2026-04-15T18:00:00"
}
```

**Respuesta** (`200 OK`): Devuelve la nota modificada con el schema `NoteResponse`.

**Respuestas de error**:

| Codigo | Descripcion |
|---|---|
| `400 Bad Request` | La nota no es valida para modificar (campo invalido, sin espacio para contenido) |
| `404 Not Found` | No existe nota con ese ID |
| `422 Unprocessable Entity` | Error de validacion de schema |

---

### PATCH `/tasks/{id}/content`

Anade contenido adicional a una nota existente. El nuevo contenido se concatena al contenido actual.

**Path Parameters**:

| Parametro | Tipo | Descripcion |
|---|---|---|
| `id` | `int` | ID de la nota |

**Request Body** (`application/json`):

| Campo | Tipo | Obligatorio | Restricciones | Descripcion |
|---|---|---|---|---|
| `content` | `string` | Si | 1-255 caracteres | Contenido a anadir |

**Ejemplo de request**:

```json
{
  "content": "Additional content appended to the note"
}
```

**Respuesta** (`200 OK`): Devuelve el espacio restante para escribir en la nota (`int`).

```json
180
```

**Respuestas de error**:

| Codigo | Descripcion |
|---|---|
| `400 Bad Request` | Nota no valida para modificar |
| `404 Not Found` | No existe nota con ese ID |
| `422 Unprocessable Entity` | Error de validacion de schema |

---

### PATCH `/tasks/{id}/completed`

Marca una nota como completada o no completada.

**Path Parameters**:

| Parametro | Tipo | Descripcion |
|---|---|---|
| `id` | `int` | ID de la nota |

**Request Body** (`application/json`):

| Campo | Tipo | Obligatorio | Descripcion |
|---|---|---|---|
| `completed` | `bool` | Si | Estado de completado |

**Ejemplo de request**:

```json
{
  "completed": true
}
```

**Respuestas**:

| Codigo | Descripcion |
|---|---|
| `204 No Content` | Nota actualizada correctamente (sin body) |
| `404 Not Found` | No existe nota con ese ID |
| `409 Conflict` | Duplicidad en resultados |
| `422 Unprocessable Entity` | Error de validacion de schema |

---

### DELETE `/tasks`

Elimina todas las notas.

**Request**: Sin parametros.

**Respuestas**:

| Codigo | Descripcion |
|---|---|
| `204 No Content` | Todas las notas eliminadas (sin body) |

---

### DELETE `/tasks/{id}`

Elimina una nota por su ID.

**Path Parameters**:

| Parametro | Tipo | Descripcion |
|---|---|---|
| `id` | `int` | ID de la nota a eliminar |

**Respuesta** (`200 OK`):

```json
[1]
```

Devuelve una lista con los IDs eliminados exitosamente.

**Respuestas de error**:

| Codigo | Descripcion |
|---|---|
| `422 Unprocessable Entity` | ID no es un entero valido |

---

## Manejo de errores

La API centraliza el manejo de errores mediante exception handlers globales. Todas las respuestas de error siguen el formato:

```json
{
  "status": 404,
  "detail": "Note with id 99 not found"
}
```

| Excepcion | HTTP Status | Caso |
|---|---|---|
| `NotFoundException` | `404 Not Found` | Nota no encontrada por ID |
| `BadNoteException` | `400 Bad Request` | Nota no valida para la operacion |
| `DuplicationException` | `409 Conflict` | Duplicidad en resultados |
| `TextOverflowException` | `400 Bad Request` | Contenido excede el maximo permitido |
| `NonWritableException` | `409 Conflict` | La nota esta completada y no se puede escribir |
| `ValueError` | `422 Unprocessable Entity` | Dato de entrada invalido |
| `RequestValidationError` | `422 Unprocessable Entity` | Error de validacion de Pydantic |

## Base de datos

La aplicacion utiliza **PostgreSQL** como base de datos. La conexion se configura mediante variables de entorno (ver `.env.example`).

| Variable | Descripcion |
|---|---|
| `POSTGRES_HOST` | Host del servidor PostgreSQL |
| `POSTGRES_USER` | Usuario de la base de datos |
| `POSTGRES_PASSWORD` | Contrasena |
| `POSTGRES_PORT` | Puerto (por defecto `5432`) |
| `POSTGRES_DB` | Nombre de la base de datos |
| `POSTGRES_DB_TABLE` | Nombre de la tabla principal |

La forma recomendada de levantar la base de datos es mediante Docker Compose (ver seccion anterior).

### Esquema de la tabla `Note`

| Columna | Tipo | Nullable | Default | Descripcion |
|---|---|---|---|---|
| `id` | `INTEGER` | No (PK) | Autoincremental | Identificador unico |
| `title` | `VARCHAR(16)` | No | `""` | Titulo de la nota |
| `content` | `VARCHAR(255)` | No | `""` | Contenido de la nota |
| `completed` | `BOOLEAN` | No | `false` | Estado de completado |
| `created_date` | `DATETIME` | No | `datetime.now` | Fecha de creacion |
| `updated_date` | `DATETIME` | Si | `null` (auto en update) | Fecha de ultima modificacion |
| `deadline_date` | `DATETIME` | Si | - | Fecha de vencimiento |
