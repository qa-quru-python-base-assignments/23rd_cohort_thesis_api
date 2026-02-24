pet_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
        "name": {"type": "string"},
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"},
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
        "status": {"type": "string"},
    },
    "required": ["id", "name", "photoUrls"],
}

pet_list_item_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "category": {
            "type": ["object", "null"],
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": ["string", "null"]},
            },
        },
        "name": {"type": ["string", "null"]},
        "photoUrls": {
            "type": "array",
            "items": {"type": ["string", "null"]},
        },
        "tags": {
            "type": "array",
            "items": {
                "type": ["object", "null"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": ["string", "null"]},
                },
            },
        },
        "status": {"type": ["string", "null"]},
    },
    "required": ["id"],
}

pets_list_response_schema = {
    "type": "array",
    "items": pet_list_item_schema,
}

create_pet_request_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
        "name": {"type": "string"},
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"},
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
        "status": {"type": "string"},
    },
    "required": ["name", "photoUrls"],
}
