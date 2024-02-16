import fastapi

import routers.clubs
import routers.tags

app = fastapi.FastAPI()

app.include_router(routers.clubs.router)
app.include_router(routers.tags.router)


@app.get("/")
def root():
    return {"message": "Root of eduAPI"}


@app.middleware("http")
async def add_encoding_header(request: fastapi.Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response
