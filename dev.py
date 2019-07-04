from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
import subprocess
import time
import os

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
        # Child process run watchdog
        class Handler(FileSystemEventHandler):
            def rebuild(self):
                # TBD: rebuild minimal files in future
                subprocess.run(["python", "build.py"])

            def on_modified(self, event):
                self.rebuild()
                
        handler = Handler()
        observer = Observer()
        observer.schedule(handler, 'articles', recursive=True)
        observer.schedule(handler, 'templates', recursive=True)
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
