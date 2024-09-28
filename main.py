from fastapi import FastAPI
from dotenv import load_dotenv

from .routes import admin_routers, user_routes, auth_routers, comment_routers, post_routers
from .db import Base,engine

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_routers.authRouters)
app.include_router(admin_routers.adminRoutes)
app.include_router(user_routes.userRouters)

app.include_router(post_routers.postRouters)
app.include_router(comment_routers.commentRouters)