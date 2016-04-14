import cerberus
import dateutil.parser

def validate_iso_datetime(field, value, error):
    try:
        dateutil.parser.parse(value)
    except ValueError:
        error(field, "invalid iso format")

team_schema = {
    "name": {"type": "string", "minlength": 1, 'required': True},
    "days_of_week": {"type": "list", "schema": {'type': 'integer'}, 'required': True},
    "send_time": {"validator": validate_iso_datetime, 'required': True},
    "summary_time": {"validator": validate_iso_datetime, 'required': True},
}

user_schema = {
    "first_name": {"type": "string", "minlength": 1, 'required': True},
    "last_name": {"type": "string", "minlength": 1, 'required': True},
    'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'required': True},
    'roles': {'type': 'list', 'required': True, 'schema': {'type':'dict', 
                    'schema': {'id': {'type': ['integer', 'string'], 'required': True}, 'name': {'type': 'string', 'required': True} } } }
}

question_schema = {
    'question': {"type": "string", "minlength": 1, 'required': True},
}