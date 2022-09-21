from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
import os
import pathlib
import subprocess
import time

HOST = '0.0.0.0'
PORT = 4000

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    print('Now launching dev webserver on {}:{}...'.format(HOST, PORT))

    server_address = ('0.0.0.0', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    pid = os.fork()

    if pid == 0:
        class TemplateHandler(FileSystemEventHandler):
            def on_modified(self, event):
                suffix = pathlib.Path(event.src_path).suffix
                if suffix != '.html':
                    return

                subprocess.run(["python", "build.py"])
                
        class ArticleHandler(FileSystemEventHandler):
            def on_modified(self, event):
                path = pathlib.Path(event.src_path)

                if path.suffix != '.md':
                    return

                subprocess.run(["python", "build.py", path.name.split('.')[0]])
                
        observer = Observer()
        observer.schedule(TemplateHandler(), 'templates', recursive=True)
        observer.schedule(ArticleHandler(), 'articles', recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        # I'm a parent, http server.
        build_dir = os.path.join(os.path.dirname(__file__), '_build')
        os.chdir(build_dir)
        run()
