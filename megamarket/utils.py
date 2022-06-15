from sqlalchemy import null

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
