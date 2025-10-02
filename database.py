from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a tu base de datos Neon PostgreSQL
DATABASE_URL = "postgresql://neondb_owner:npg_bkrhtzwV76oS@ep-steep-cloud-adns5pw1-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Crea el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crea una clase de sesión configurada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase Base para los modelos ORM
Base = declarative_base()

# ----------------------------------------------------
# <-- CAMBIO CLAVE: La función get_db AHORA VIVE AQUÍ
# ----------------------------------------------------
# Dependencia para obtener la sesión de la base de datos en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

