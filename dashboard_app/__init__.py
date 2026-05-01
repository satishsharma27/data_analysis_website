from pathlib import Path

from flask import Flask

from .routes import register_routes


def create_app() -> Flask:
    project_root = Path(__file__).resolve().parent.parent
    template_folder = project_root / "templates"
    static_folder = project_root / "static"

    server = Flask(
        __name__,
        static_folder=str(static_folder),
        template_folder=str(template_folder),
    )
    server.config["PROPAGATE_EXCEPTIONS"] = True

    register_routes(server)

    return server
