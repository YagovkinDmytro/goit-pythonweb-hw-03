import mimetypes
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from datetime import datetime
import json
from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = 'templates'
DATA_FILE = 'storage/data.json'
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file(f'{TEMPLATES_DIR}/index.html')
        elif pr_url.path == '/message':
            self.send_html_file(f'{TEMPLATES_DIR}/message.html')
        elif pr_url.path == '/read':
            html = self.get_person_html()
            self.send_html_content(html)
        else:
            if Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)
    
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data_info ={data_time: {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}}
        self.save_to_json(data_info, f'{DATA_FILE}')
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
    
    def send_html_content(self, html, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def save_to_json(self, data_dict, file_path):
        data_path = Path(file_path)
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        
        if data_path.exists():
            try:
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass

        data.update(data_dict)

        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_person_html(self):
        data_path = Path(f'{DATA_FILE}')
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data = {}
    
        if data_path.exists():
            try:
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass
        
        env = Environment(loader=FileSystemLoader(f'{TEMPLATES_DIR}'))
        template = env.get_template("persons.html")
        output = template.render(persons=data.values())
        return output
        

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_addres = ('', 3000)
    http = server_class(server_addres, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    run()