# GraphQL and Ariadne Demo
Quick demo app to try out GraphQL and Ariadne with python flask

### Example Request

```
{ 
    person(id: 1) {
        name
        age
        email
    }
}
```

### Example response

```
{
    "data": {
        "person": {
            "age": 37,
            "email": "pete-jenkins@mail.com",
            "name": "Peter Jenkins"
        }
    }
}
```


### Example Error Response

```
{
    "data": {
        "person": null
    },
    "errors": [
        {
            "extensions": {
                "exception": {
                    "context": {
                        "_": "None",
                        "age": "374",
                        "email": "None",
                        "id": "None",
                        "info": "GraphQLResolv...0210368B3310>)",
                        "name": "None",
                        "person": "None"
                    },
                    "stacktrace": [
                        "Traceback (most recent call last):",
                        "  File \"C:\\Users\\Daithi\\PycharmProjects\\ariadne-demo\\venv\\lib\\site-packages\\graphql\\execution\\execute.py\", line 617, in resolve_field",
                        "    result = resolve_fn(source, info, **args)",
                        "  File \"C:\\Users\\Daithi\\PycharmProjects\\ariadne-demo\\run.py\", line 24, in resolve_person",
                        "    raise Exception('No person found matching request parameters')",
                        "Exception: No person found matching request parameters"
                    ]
                }
            },
            "locations": [
                {
                    "column": 5,
                    "line": 2
                }
            ],
            "message": "No person found matching request parameters",
            "path": [
                "person"
            ]
        }
    ]
}
```
