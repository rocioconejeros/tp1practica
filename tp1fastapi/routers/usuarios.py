from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field
# Este router maneja los endpoints relacionados con los usuarios, incluyendo registro
# listado y obtención de detalles de un usuario específico

router = APIRouter(prefix="/users", tags=["Usuarios"])  # Todos los endpoints empiezan con /users
db_usuarios = []  # lista vacía al inicio

@router.get("/")
def listar_usuarios(): # Endpoint para listar todos los usuarios registrados
    return db_usuarios # Devuelve la lista completa de usuarios



class Usuario(BaseModel):
    username: Annotated[str, Field(min_length=5)] 
    edad: Annotated[int, Field(ge=18)]

# Endpoint para registrar un nuevo usuario. Recibe un objeto Usuario en el cuerpo de la solicitud,
# valida que el username tenga al menos 5 caracteres y que la edad sea mayor o igual a 18

@router.post("/", status_code=201)
def registrar_usuario(nuevo_usuario: Annotated[Usuario, Field(description="Datos del nuevo usuario")]):
# Antes de registrar, verifico que el username no exista ya en la base de datos
    for u in db_usuarios:
        if u["username"] == nuevo_usuario.username:
            raise HTTPException(status_code=400, detail="Usuario ya existe")

# Al registrar un nuevo usuario, convierto el modelo a un diccionario y lo agrego a la base de datos simulada
    nuevo = nuevo_usuario.model_dump()
    db_usuarios.append(nuevo)
    return {"message": "Usuario registrado exitosamente", "usuario": nuevo}
#   Devuelve un mensaje de éxito junto con los datos del usuario registrado

@router.get("/{user_id}") # Endpoint para obtener los detalles de un usuario específico
def obtener_usuario(
    user_id: Annotated[int, Path(gt=0)], 
    categoria: Annotated[str, Query(min_length=3)] = "general"
# El endpoint recibe un user_id como parte de la ruta, que debe ser un entero mayor a 0, y una categoría opcional como query parameter con una longitud mínima de 3 caracteres
# Si el usuario existe, devuelve sus detalles junto con la categoría solicitada. Si el usuario no existe, devuelve un error 404
):
    if user_id < 1 or user_id > len(db_usuarios):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Dado que los índices de la lista comienzan en 0, restamos 1 al user_id para obtener el usuario correcto

    usuario = db_usuarios[user_id - 1]
    return {"usuario": usuario, "categoria": categoria}
# Si el user_id es válido, se devuelve un diccionario con los detalles del usuario y la categoría solicitada. Si no, se lanza una excepción HTTP 404 indicando que el usuario no fue encontrado
