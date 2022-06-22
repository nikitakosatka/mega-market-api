from fastapi.openapi.utils import get_openapi

tags_metadata = [
    {
        "name": "Базовые задачи",
        "description": "Импорт, удаление и просмотр товаров и категорий",
    },
]


def change_doc_metadata(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Mega Market Open API",
            version="1.0",
            description="Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    app.openapi_tags = tags_metadata
