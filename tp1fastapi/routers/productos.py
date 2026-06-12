from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dependencies import verify_api_token
# Este router maneja los endpoints relacionados con los productos, incluyendo agregar y listar productos

router = APIRouter(prefix="/productos", tags=["Productos"]) 
db_productos = []
# Lista vacía al inicio para almacenar los productos agregados

class EstruProducto(BaseModel):
    nombre: str
    precio: Annotated[float, Field(gt=0)]
# El modelo EstruProducto define la estructura de los datos que se esperan al agregar un nuevo producto, 
# con validación para asegurar que el precio sea un número positivo

@router.post("/", status_code=201)
def agregar_producto(
    producto: EstruProducto, 
    _: Annotated[None, Depends(verify_api_token)]):
    nuevo = producto.model_dump()
    db_productos.append(nuevo)
    return {"message": "Producto agregado exitosamente", "producto": nuevo}
# El endpoint para agregar un nuevo producto recibe un objeto EstruProducto en el cuerpo de la solicitud,
# valida el token de autenticación mediante la dependencia, y si es válido, agrega el producto

@router.get("/")
def listar_productos():
    return {"productos": db_productos}
# El endpoint para listar productos devuelve la lista completa de productos almacenados en la base de datos simulada

