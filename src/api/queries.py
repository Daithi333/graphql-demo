from ariadne import ObjectType

from database import Person

query = ObjectType("Query")


@query.field('person')
def resolve_person(_, info, id: int = None, name: str = None, age: int = None, email: str = None):
    db = info.context["db"]

    filters = {}
    if id is not None:
        filters["id"] = id
    if name is not None:
        filters["name"] = name
    if age is not None:
        filters["age"] = age
    if email is not None:
        filters["email"] = email

    if not filters:
        raise KeyError('At least one search key must be provided')

    person = db.query(Person).filter_by(**filters).one_or_none()
    if not person:
        raise Exception('No person found matching request parameters')

    return person


@query.field('people')
def resolve_people(_, info):
    db = info.context["db"]
    return db.query(Person).all()
