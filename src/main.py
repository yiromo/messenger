from fastapi import FastAPI
import uvicorn
from admin.route import router as admin_router
from auth.route import router as auth_router
from chat.route import router as chat_router
from user.route import router as user_router
from config import settings
#from test import router as test
from fastapi.middleware.cors import CORSMiddleware
from migrate.migrate01 import migrate

origins = ["*"]

app = FastAPI()

#migrate()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"] if settings.IS_DEVELOPMENT else origins,
)


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(user_router)
#app.include_router()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)