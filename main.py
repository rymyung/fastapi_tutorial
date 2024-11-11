from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
# from user.interface.controllers.user_controller import router as user_routers
from user.interface.controllers import user_controller
from containers import Container
import uvicorn

app = FastAPI()
container = Container()
container.init_resources()
container.wire(modules=[user_controller])
app.include_router(user_controller.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "errors": exc.errors()}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
