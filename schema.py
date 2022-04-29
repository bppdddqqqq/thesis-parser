category_schema = {
        "type": "object",
        "properties": {
            "mandatory": {
                "type": "boolean",
            },
            "type": {
                "type": "string",
            },
            "title": {
                "type": "string",
            },
            "description": {
                "type": "string",
            },
            "hint": {
                "type": "string",
            },
        },
    }

enabler_schema = {
        "type": "Object",
        "properties": {
            "applyCategories": {
                "type": "string[]"
            },
            "unapplyCategories": {
                "type": "string[]"
            },
            "unapplyAll": {
                "type": "boolean"
            }
        }
    }
