from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError

# ============================================================
# Aplicación de Biblioteca Personal con MariaDB y SQLAlchemy
# Autor: Kayder Murillo
# Descripción: Programa de línea de comandos que administra libros
# utilizando un ORM para conectar con una base de datos MariaDB.
# ============================================================

Base = declarative_base()

# ------------------------------------------------------------
# Definición del modelo de datos
# ------------------------------------------------------------
class Libro(Base):
    __tablename__ = "libros"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    estado = Column(String(20), nullable=False)
    
    __table_args__ = (
        CheckConstraint("estado IN ('Leído','No leído')", name="check_estado"),
    )

# ------------------------------------------------------------
# Conexión con MariaDB
# ------------------------------------------------------------
def crear_sesion():
    try:
        # Ajusta estos datos a tu entorno de MariaDB
        usuario = "root"
        contrasena = "1234"
        host = "localhost"
        base_datos = "biblioteca_db"
        
        cadena_conexion = f"mysql+pymysql://{usuario}:{contrasena}@{host}/{base_datos}"
        engine = create_engine(cadena_conexion, echo=False)
        
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()
    except OperationalError:
        print("Error: No se pudo conectar a la base de datos. Verifica las credenciales o el servidor MariaDB.")
        exit()
    except Exception as e:
        print(f"Error inesperado al conectar: {e}")
        exit()

# ------------------------------------------------------------
# Funciones CRUD
# ------------------------------------------------------------
def agregar_libro(session):
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (Leído/No leído): ")

    libro = Libro(titulo=titulo, autor=autor, genero=genero, estado=estado)
    session.add(libro)
    try:
        session.commit()
        print("Libro agregado correctamente.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al agregar libro:", e)

def actualizar_libro(session):
    ver_libros(session)
    id_libro = input("Ingrese el ID del libro que desea actualizar: ")
    libro = session.get(Libro, id_libro)
    if not libro:
        print("No se encontró un libro con ese ID.\n")
        return

    libro.titulo = input("Nuevo título: ")
    libro.autor = input("Nuevo autor: ")
    libro.genero = input("Nuevo género: ")
    libro.estado = input("Nuevo estado (Leído/No leído): ")
    try:
        session.commit()
        print("Libro actualizado exitosamente.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al actualizar libro:", e)

def eliminar_libro(session):
    ver_libros(session)
    id_libro = input("Ingrese el ID del libro que desea eliminar: ")
    libro = session.get(Libro, id_libro)
    if libro:
        session.delete(libro)
        try:
            session.commit()
            print("Libro eliminado.\n")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error al eliminar libro:", e)
    else:
        print("No se encontró un libro con ese ID.\n")

def ver_libros(session):
    libros = session.query(Libro).all()
    if libros:
        print("\nLISTADO DE LIBROS:")
        print("-" * 60)
        for libro in libros:
            print(f"ID: {libro.id} | Título: {libro.titulo} | Autor: {libro.autor} | Género: {libro.genero} | Estado: {libro.estado}")
        print("-" * 60 + "\n")
    else:
        print("No hay libros registrados.\n")

def buscar_libros(session):
    campo = input("Buscar por (titulo/autor/genero): ").lower()
    termino = input(f"Ingrese el {campo} que desea buscar: ")

    if campo not in ["titulo", "autor", "genero"]:
        print("Campo no válido. Intente con titulo, autor o genero.\n")
        return

    filtro = getattr(Libro, campo).like(f"%{termino}%")
    resultados = session.query(Libro).filter(filtro).all()

    if resultados:
        print("\nRESULTADOS DE BÚSQUEDA:")
        for libro in resultados:
            print(f"ID: {libro.id} | Título: {libro.titulo} | Autor: {libro.autor} | Género: {libro.genero} | Estado: {libro.estado}")
        print()
    else:
        print("No se encontraron libros que coincidan.\n")

# ------------------------------------------------------------
# Menú principal
# ------------------------------------------------------------
def menu():
    session = crear_sesion()
    while True:
        print("========= MENÚ BIBLIOTECA PERSONAL =========")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        print("=============================================")

        opcion = input("Seleccione una opción (1-6): ")
        print()

        if opcion == "1":
            agregar_libro(session)
        elif opcion == "2":
            actualizar_libro(session)
        elif opcion == "3":
            eliminar_libro(session)
        elif opcion == "4":
            ver_libros(session)
        elif opcion == "5":
            buscar_libros(session)
        elif opcion == "6":
            print("Saliendo del programa...")
            session.close()
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")

# ------------------------------------------------------------
# Ejecución principal
# ------------------------------------------------------------
if __name__ == "__main__":
    menu()
