from typing import Annotated
from fastapi import Query, HTTPException
# Esta función se encarga de verificar el token de autenticación en las solicitudes 
# a los endpoints protegidos

def verify_api_token(token: Annotated[str, Query()]):
    if token != "nivel-intermedio-2026":
        raise HTTPException(status_code=401, detail="token invalido o no autorizado")
# Si el token es correcto, la función no hace nada y permite que la solicitud continúe 