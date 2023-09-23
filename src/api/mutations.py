from ariadne import ObjectType

from database import Person

mutation = ObjectType("Mutation")


@mutation.field("createPerson")
async def resolve_create_person(_, info, name: str, age: int = None, email: str = None):
    db = info.context["db"]
    person = Person(name=name, age=age, email=email)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@mutation.field("updatePerson")
async def resolve_update_person(_, info, id: int, name: str = None, age: int = None, email: str = None):
    db = info.context["db"]
    person = db.query(Person).filter(id=id).one()
    if not person:
        raise KeyError(f"Person {id} key not found")

    person.name = name
    person.age = age
    person.email = email
    return person


@mutation.field("deletePerson")
async def resolve_delete_person(_, info, id: int):
    db = info.context["db"]
    person = db.query(Person).filter(id=id).one()
    if not person:
        raise KeyError(f"Person {id} key not found")

    db.delete(person)
    return True
