from dustpath import controller


def main():
    server = controller.create_server()
    server.run()
