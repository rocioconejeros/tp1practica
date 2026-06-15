from fastapi import FastAPI, Depends
from dependencies import verify_api_token
from routers import usuarios, productos
# importo fastapi, routers y dependencias necesarias

app = FastAPI()
app.include_router(usuarios.router)
# Incluyo el router de usuarios sin dependencias

app.include_router(
    productos.router,
    dependencies=[Depends(verify_api_token)] 
)

# Incluyo el router de productos con la dependencia de verificación de token 
# los endpoints de productos pidan un token para acceder


