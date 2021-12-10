from dustpath import web


def main():
    app = web.create_app()

    app.run(
            debug=True,
            host='0.0.0.0',
            port=8080
    )
