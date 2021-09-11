from ariadne import QueryType, make_executable_schema, graphql_sync
from flask import Flask, jsonify, request

from test_data import people
from type_defs import type_defs

query = QueryType()


@query.field('person')
def resolve_person(_, info, id: int = None, name: str = None, age: int = None, email: str = None):
    if id:
        person = people[id]
    elif name:
        person = next((p for p in people if p['name'] == name), None)
    elif age:
        person = next((p for p in people if p['age'] == age), None)
    elif email:
        person = next((p for p in people if p['email'] == email), None)
    else:
        raise KeyError('Search key not found')

    if not person:
        raise Exception('No person found matching request parameters')

    return person


schema = make_executable_schema(type_defs, query)
app = Flask(__name__)


@app.route('/')
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route('/graphql', methods=['POST'])
def graphql():
    data = request.get_json()

    _, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    status_code = 400 if 'errors' in result else 200

    return jsonify(result), status_code


if __name__ == '__main__':
    app.run('localhost', '8080', debug=True)
