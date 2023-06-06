from fastapi import FastAPI

from src.modules.home.routes import router as home_router
from src.tenant.routes import router as tenant_router
from src.modules.book.routes import router as book_router
from src.modules.note.routes import router as note_router
from src.modules.sandbox.routes import router as sandbox_router
from src.modules.product.routes import router as product_router
from src.modules.order.routes import router as order_router


def register_app(app: FastAPI):
    app.include_router(home_router)
    app.include_router(tenant_router)
    app.include_router(book_router)
    app.include_router(note_router)
    app.include_router(sandbox_router)
    app.include_router(product_router)
    app.include_router(order_router)
