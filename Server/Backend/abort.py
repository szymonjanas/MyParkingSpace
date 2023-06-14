from flask import make_response, abort as fabort
import json

def abort(status_code, message):
    response = make_response(json.dumps({"error" : message}))
    response.status_code = status_code
    response.content_type = "application/json"
    fabort(response)
