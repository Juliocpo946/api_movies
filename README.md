# Movie Night API

API REST profesional para gestión de películas, favoritos y calificaciones de usuarios. Construida con FastAPI, SQLAlchemy y PostgreSQL.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Juliocpo946/api_movies)

---

## Características

- **Autenticación JWT** - Sistema seguro de login y registro
- **Gestión de películas** - Búsqueda, trending y películas populares
- **Favoritos** - Sistema para marcar películas favoritas por usuario
- **Calificaciones** - Los usuarios pueden calificar películas
- **Base de datos PostgreSQL** - Integración con Neon Database
- **API REST completa** - Documentación automática con Swagger/OpenAPI
- **Deploy automático** - Configurado para Render.com

---

## Requisitos previos

- Python 3.11+
- PostgreSQL (o cuenta en Neon Database)
- Cuenta en [Render.com](https://render.com) (para deploy)
- API Key de TMDB (opcional, para integración con TheMovieDB)

---

## 🛠️ Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Juliocpo946/api_movies.git
cd api_movies
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
TMDB_API_KEY=tu_api_key_de_tmdb
TMDB_BASE_URL=https://api.themoviedb.org/3
DATABASE_URL=postgresql://usuario:password@host:5432/database
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

Documentación interactiva: `http://127.0.0.1:8000/docs`

---

## Deploy en Render

### Opción 1: Deploy automático (Recomendado)

Simplemente haz clic en el botón:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Juliocpo946/api_movies)

### Opción 2: Deploy manual

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura las siguientes opciones:
   - **Name**: `movie-night-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Agrega las variables de entorno en **"Environment"**:
   - `SECRET_KEY`
   - `TMDB_API_KEY`
   - `DATABASE_URL`
   - `ALGORITHM` = `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
6. Click en **"Create Web Service"**

---

## Estructura del proyecto

```
api_movies/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada de la aplicación
│   ├── core/
│   │   ├── config.py              # Configuración y variables de entorno
│   │   └── security.py            # Funciones de seguridad y JWT
│   ├── db/
│   │   ├── database.py            # Configuración de SQLAlchemy
│   │   └── models.py              # Modelos de base de datos
│   ├── crud/
│   │   ├── user.py                # Operaciones CRUD de usuarios
│   │   ├── movie.py               # Operaciones CRUD de películas
│   │   ├── favorite.py            # Operaciones CRUD de favoritos
│   │   └── rating.py              # Operaciones CRUD de calificaciones
│   ├── schemas/
│   │   ├── user.py                # Schemas Pydantic de usuarios
│   │   ├── movie.py               # Schemas Pydantic de películas
│   │   ├── favorite.py            # Schemas Pydantic de favoritos
│   │   ├── rating.py              # Schemas Pydantic de calificaciones
│   │   └── auth.py                # Schemas de autenticación
│   └── api/
│       ├── deps.py                # Dependencias compartidas
│       └── endpoints/
│           ├── auth.py            # Endpoints de autenticación
│           ├── movies.py          # Endpoints de películas
│           ├── favorites.py       # Endpoints de favoritos
│           └── ratings.py         # Endpoints de calificaciones
├── .env                           # Variables de entorno (no subir a Git)
├── .gitignore
├── requirements.txt
├── render.yaml                    # Configuración de Render
└── README.md
```

---

## Endpoints principales

### Autenticación
- `POST /users/register` - Registrar nuevo usuario
- `POST /users/login` - Login y obtener token JWT

### Películas
- `GET /movies/trending` - Top 10 películas trending
- `GET /movies/popular` - Películas populares (paginado)
- `GET /movies/search?query=...` - Buscar películas
- `GET /movies/{movie_id}` - Detalle de película

### Favoritos
- `GET /users/{user_id}/favorites` - Lista de favoritos del usuario
- `POST /users/{user_id}/favorites` - Agregar favorito
- `DELETE /users/{user_id}/favorites/{movie_id}` - Eliminar favorito

### Calificaciones
- `GET /users/{user_id}/ratings` - Calificaciones del usuario
- `POST /users/{user_id}/ratings` - Agregar/actualizar calificación
- `DELETE /users/{user_id}/ratings/{movie_id}` - Eliminar calificación

---

## Autenticación

La API usa **JWT (JSON Web Tokens)** para autenticación.

### Flujo de autenticación:

1. **Registro**: `POST /users/register`
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

2. **Login**: `POST /users/login`
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

3. **Respuesta con token**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

4. **Usar token en requests**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Testing

Para probar la API localmente:

1. Inicia el servidor: `uvicorn app.main:app --reload`
2. Abre tu navegador en: `http://127.0.0.1:8000/docs`
3. Usa la interfaz Swagger para probar los endpoints

---

## Seguridad

- Contraseñas hasheadas con **bcrypt**
- Tokens JWT con expiración configurable
- Validación de datos con **Pydantic**
- Variables sensibles en `.env` (no versionadas)
- Autorización por usuario para endpoints protegidos
