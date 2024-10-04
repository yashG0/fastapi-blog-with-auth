from fastapi import FastAPI
from dotenv import load_dotenv
from .routes import admin_routers, user_routes, auth_routers, comment_routers, post_routers
from .db import Base,engine


load_dotenv()

app = FastAPI(title="BlogHub API",
    description="""
    BlogHub is a powerful and user-friendly blogging platform API built with FastAPI.

    Key Features:
    * User authentication and authorization
    * Create, read, update, and delete blog posts
    * Comment system for engaging discussions
    * Tag and category management for content organization
    * User profile management
    * Search functionality for posts and users
    * Analytics for post views and user engagement

    This API provides a robust backend for building modern, responsive blogging applications.
    It's designed with scalability and performance in mind, leveraging FastAPI's asynchronous capabilities.

    For detailed documentation on each endpoint, please refer to the OpenAPI schema below.
    """,)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routers.authRouters)
app.include_router(admin_routers.adminRoutes)
app.include_router(user_routes.userRouters)

app.include_router(post_routers.postRouters)
app.include_router(comment_routers.commentRouters)