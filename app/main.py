import fastapi

import routers.auth
import routers.clubs
import routers.organizations
import routers.tags
import routers.users

app = fastapi.FastAPI()

app.include_router(routers.auth.router)
app.include_router(routers.clubs.router)
app.include_router(routers.organizations.router)
app.include_router(routers.tags.router)
app.include_router(routers.users.router)


@app.get("/")
def root():
    return {"message": "Root of eduAPI"}


@app.middleware("http")
async def add_encoding_header(request: fastapi.Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response
