from fastapi import FastAPI
import uvicorn
from admin.route import router as admin_router
from auth.route import router as auth_router
from chat.route import router as chat_router
from user.route import router as user_router
#from test import router as test
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(user_router)
#app.include_router()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)