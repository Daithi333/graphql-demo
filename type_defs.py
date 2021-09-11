from ariadne import gql

type_defs = gql("""
    type Query {
        person(id: Int, name: String, age: Int, email: String): Person
    }
    type Person {
        id: Int!
        name: String!
        age: Int
        email: String
    }
""")
