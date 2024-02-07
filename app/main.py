import fastapi

import routers.clubs

app = fastapi.FastAPI()

app.include_router(routers.clubs.router)


@app.get("/")
def root():
    return {"message": "Root of eduAPI"}
