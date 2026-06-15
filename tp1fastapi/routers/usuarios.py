from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field
# Este router maneja los endpoints relacionados con los usuarios, incluyendo registro
# listas y los detalles del usuario seleccionado

router = APIRouter(prefix="/users", tags=["Usuarios"])  # Todos los endpoints empiezan con /users
db_usuarios = []  # lista vacía al inicio. Base de datos donde pondre los usuarios

@router.get("/")
def listar_usuarios(): # Endpoint para poner todos los usuarios en la base de datos ya creada
    return db_usuarios # Devuelve la lista completa de usuarios



class Usuario(BaseModel):
    username: Annotated[str, Field(min_length=5)] 
    edad: Annotated[int, Field(ge=18)]

# Endpoint para registrar al nuevo usuario. Recibe un objeto Usuario en el cuerpo de la solicitud,
# valida que el username tenga mas de 5 caracteres y que la edad sea mayor o igual a 18

@router.post("/", status_code=201)
def registrar_usuario(nuevo_usuario: Annotated[Usuario, Field(description="Datos del nuevo usuario")]):
# Antes de registrar, verifico que el usuario no exista antes en la base de datos
    for u in db_usuarios:
        if u["username"] == nuevo_usuario.username:
            raise HTTPException(status_code=400, detail="Usuario ya existe")

# Al registrar un nuevo usuario, convierto el modelo a un diccionario y lo agrego a la base de datos
    nuevo = nuevo_usuario.model_dump()
    db_usuarios.append(nuevo)
    return {"message": "Usuario registrado exitosamente", "usuario": nuevo}
#   Devuelve un mensaje de éxito junto con los datos del usuario registrado

@router.get("/{user_id}") # Endpoint para obtener los detalles de un usuario en específico
def obtener_usuario(
    user_id: Annotated[int, Path(gt=0)], 
    categoria: Annotated[str, Query(min_length=3)] = "general"
# El endpoint recibe un user_id como parte de la ruta, entero, positivo y una categoría opcional como query parameter longitud mas de 3
# Si el usuario existe, devuelve detalles con la categoría. Si el usuario no existe devuelve un error 404
):
    if user_id < 1 or user_id > len(db_usuarios):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # indices de la lista empieza con 0, restamos 1 al user_id para obtener el usuario

    usuario = db_usuarios[user_id - 1]
    return {"usuario": usuario, "categoria": categoria}
# user_id es válido, devuelve el diccionario con detalles del usuario y la categoría. Si no, se lanza una excepción HTTP 404 que es un usuario que no se encontro
