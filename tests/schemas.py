COMPANIES_LIST_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'company_id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'},
                },
                'required': ['company_id', 'name', 'created_at', 'updated_at'],
                'additionalProperties': False
            }
        }
    },
    'required': ['data'],
    'additionalProperties': False
}


COMPANY_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'company_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'updated_at': {'type': 'string', 'format': 'date-time'},
            },
            'required': ['company_id', 'name', 'created_at', 'updated_at'],
            'additionalProperties': False
        }
    },
    'required': ['data'],
    'additionalProperties': False
}


EMPLOYEES_LIST_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'employee_id': {'type': 'integer'},
                    'company_id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'},
                },
                'required': [
                    'employee_id', 'company_id', 'name', 'created_at',
                    'updated_at'
                ],
                'additionalProperties': False
            }
        }
    },
    'required': ['data'],
    'additionalProperties': False
}


EMPLOYEE_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'employee_id': {'type': 'integer'},
                'company_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'updated_at': {'type': 'string', 'format': 'date-time'},
            },
            'required': [
                'employee_id', 'company_id', 'name', 'created_at', 'updated_at'
            ],
            'additionalProperties': False
        }
    },
    'required': ['data'],
    'additionalProperties': False
}


PRODUCTS_LIST_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'product_id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'price': {'type': 'number'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'},
                },
                'required': [
                    'product_id', 'price', 'name', 'created_at', 'updated_at'
                ],
                'additionalProperties': False
            }
        }
    },
    'required': ['data'],
    'additionalProperties': False
}


PRODUCT_RESPONSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'product_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'price': {'type': 'number'},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'updated_at': {'type': 'string', 'format': 'date-time'},
            },
            'required': [
                'product_id', 'price', 'name', 'created_at', 'updated_at'
            ],
            'additionalProperties': False
        }
    },
    'required': ['data'],
    'additionalProperties': False
}
