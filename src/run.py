import os

from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from fastapi import FastAPI, Request, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Server, Config as UvicornConfig

from api.queries import query
from api.mutations import mutation
from config import Config
from database import get_database_session

current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(current_dir, "api")
schema_path = os.path.join(api_dir, "schema.graphql")
type_defs = [load_schema_from_path(schema_path)]

schema = make_executable_schema(type_defs, [query, mutation])


def get_context_value(request_or_ws: Request | WebSocket, _data) -> dict:
    return {
        "request": request_or_ws,
        "db": request_or_ws.scope["db"],
    }


graphql_app = GraphQL(
    schema,
    debug=True,
    context_value=get_context_value
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.SERVER_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@app.get("/health_check")
async def root():
    return "ok"


@app.get("/graphql/")
@app.options("/graphql/")
async def handle_graphql_explorer(
    request: Request,
    db=Depends(get_database_session),
):
    request.scope["db"] = db
    return await graphql_app.handle_request(request)


@app.post("/graphql/")
async def handle_graphql_query(
    request: Request,
    db=Depends(get_database_session),
):
    request.scope["db"] = db
    return await graphql_app.handle_request(request)


if __name__ == '__main__':
    config = UvicornConfig(
        app=app, port=Config.SERVER_PORT, host=Config.SERVER_HOST
    )
    server = Server(config)
    server.run()
