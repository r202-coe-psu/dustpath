from dustpath import processor


def main():
    server = processor.create_server()
    server.run()
