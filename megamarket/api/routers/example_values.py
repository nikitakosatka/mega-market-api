from sqlalchemy import null

from megamarket.schemas import Error

imports_request_example = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
            "name": "Оффер",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333",
            "price": 234,
            "type": "OFFER"
        }
    ],
    "updateDate": "2022-05-28T21:12:01.000Z"
}

nodes_response_example = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
    "name": "Категория",
    "type": "CATEGORY",
    "parentId": null,
    "date": "2022-05-28T21:12:01.000Z",
    "price": 6,
    "children": [
        {
            "name": "Оффер 1",
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "price": 4,
            "date": "2022-05-28T21:12:01.000Z",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111"
        },
        {
            "name": "Подкатегория",
            "type": "CATEGORY",
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
            "date": "2022-05-26T21:12:01.000Z",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "price": 8,
            "children": [
                {
                    "name": "Оффер 2",
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
                    "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333",
                    "date": "2022-05-26T21:12:01.000Z",
                    "price": 8,
                    "type": "OFFER"
                }
            ]
        }
    ]
}

error_400_example = {
    "code": 400,
    "message": "Validation Failed"
}

error_404_example = {
    "code": 404,
    "message": "Item not found"
}

imports_responses = {
    200: {
        "description": "Items were imported",
        "content": {
            "application/json": {
                "example": 200}
        }
    },
    400: {
        "model": Error,
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": error_400_example}
        }
    }
}

delete_responses = {
    200: {
        "description": "Item was successfully deleted",
        "content": {
            "application/json": {
                "example": 200}
        }
    },
    400: {
        "model": Error,
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": error_400_example}
        }
    },
    404: {
        "model": Error,
        "description": "Item not found",
        "content": {
            "application/json": {
                "example": error_404_example}
        }
    }
}

nodes_responses = {
    200: {
        "description": "Item requested by ID",
        "content": {
            "application/json": {
                "example": nodes_response_example}
        }
    },
    400: {
        "model": Error,
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": error_400_example}
        }
    },
    404: {
        "model": Error,
        "description": "Item not found",
        "content": {
            "application/json": {
                "example": error_404_example}
        }
    }
}

sales_response_example = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
            "name": "Оффер",
            "date": "2022-05-28T21:12:01.000Z",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333",
            "price": 234,
            "type": "OFFER"
        }
    ]
}

sales_responses = {
    200: {
        "description": "Items requested by date",
        "content": {
            "application/json": {
                "example": sales_response_example}
        }
    },
    400: {
        "model": Error,
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": error_400_example}
        }
    }
}
