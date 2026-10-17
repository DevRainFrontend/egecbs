import http.server
import socketserver
import urllib.parse
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ADMIN_DIR = os.path.join(BASE_DIR, "admin")

# Always ensure working directory is BASE_DIR
os.chdir(BASE_DIR)

class CBSAdminHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def translate_path(self, path):
        # Handle /admin routes
        url_path = urllib.parse.urlparse(path).path
        if url_path == "/admin" or url_path == "/admin/":
            return os.path.join(ADMIN_DIR, "index.html")
        elif url_path.startswith("/admin/"):
            rel_path = url_path[7:].lstrip("/")
            return os.path.join(ADMIN_DIR, rel_path)
        elif url_path == "/" or url_path == "":
            return os.path.join(BASE_DIR, "ege_cbs.html")
        return super().translate_path(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        url_path = url_parsed.path
        query = urllib.parse.parse_qs(url_parsed.query)

        # REST API: /api/datasets
        if url_path == "/api/datasets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            files_info = []
            if os.path.exists(DATA_DIR):
                for fname in sorted(os.listdir(DATA_DIR)):
                    fpath = os.path.join(DATA_DIR, fname)
                    if os.path.isfile(fpath):
                        size = os.path.getsize(fpath)
                        items = 0
                        if fname.endswith(".json"):
                            try:
                                with open(fpath, "r", encoding="utf-8") as f:
                                    d = json.load(f)
                                    if isinstance(d, list):
                                        items = len(d)
                                    elif isinstance(d, dict) and "provinces" in d:
                                        items = len(d["provinces"])
                            except: pass
                        elif fname.endswith(".js"):
                            try:
                                with open(fpath, "r", encoding="utf-8") as f:
                                    txt = f.read()
                                    # Robust extraction of item count in JS files
                                    match = re.search(r'=\s*(\[[\s\S]*?\])\s*;?\s*(?:window|$)', txt)
                                    if match:
                                        try:
                                            arr = json.loads(match.group(1))
                                            items = len(arr)
                                        except:
                                            items = len(re.findall(r'\[\s*(?:"|{)', txt))
                                    else:
                                        items = len(re.findall(r'\[\s*(?:"|{)', txt))
                            except: pass
                        files_info.append({"name": fname, "size": size, "items": items})

            self.wfile.write(json.dumps(files_info, ensure_ascii=False).encode("utf-8"))
            return

        # REST API: /api/dataset?file=<fname>
        if url_path == "/api/dataset":
            fname = query.get("file", ["schools.json"])[0]
            fname = os.path.basename(fname)
            fpath = os.path.join(DATA_DIR, fname)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            if os.path.exists(fpath):
                size = os.path.getsize(fpath)
                with open(fpath, "r", encoding="utf-8") as f:
                    raw = f.read()
                parsed = []
                if fname.endswith(".json"):
                    try:
                        parsed = json.loads(raw)
                    except: pass
                elif fname.endswith(".js"):
                    try:
                        match = re.search(r'=\s*(\[[\s\S]*?\])\s*;?\s*(?:window|$)', raw)
                        if match:
                            parsed = json.loads(match.group(1))
                    except: pass

                resp = {"file": fname, "size": size, "raw": raw, "parsed": parsed}
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"error": "File not found"}, ensure_ascii=False).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        url_path = urllib.parse.urlparse(self.path).path

        if url_path == "/api/dataset":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                fname = os.path.basename(data.get("file", ""))
                content = data.get("content", "")

                if not fname:
                    raise Exception("Missing file name")

                fpath = os.path.join(DATA_DIR, fname)

                # Save the file content
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)

                # If JSON file updated, also update corresponding JS file (except harita.js which has functions)
                if fname.endswith(".json"):
                    key = fname[:-5] # e.g. schools
                    if key != "harita":
                        js_fname = key + ".js"
                        js_fpath = os.path.join(DATA_DIR, js_fname)
                        try:
                            parsed_json = json.loads(content)
                            parsed_str = json.dumps(parsed_json, ensure_ascii=False)
                            js_content = "window.CBS_DATA = window.CBS_DATA || {};\nwindow." + key + " = " + parsed_str + ";\nwindow.CBS_DATA." + key + " = window." + key + ";\n"
                            with open(js_fpath, "w", encoding="utf-8") as js_f:
                                js_f.write(js_content)
                            print("Synced " + js_fname + " automatically.")
                        except Exception as ex:
                            print("Warning syncing JS file: " + str(ex))

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "file": fname}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        super().do_POST()

def start_server():
    ports = [3000, 3001, 3002]
    for port in ports:
        try:
            handler = CBSAdminHandler
            handler.extensions_map.update({
                ".js": "application/javascript",
                ".json": "application/json",
                ".css": "text/css",
                ".html": "text/html"
            })
            httpd = socketserver.TCPServer(("", port), handler)
            print("==================================================")
            print(f" Ege CBS Sunucusu Başlatıldı!                      ")
            print(f" Harita Sayfası : http://localhost:{port}/         ")
            print(f" Admin Paneli   : http://localhost:{port}/admin/   ")
            print("==================================================")
            httpd.serve_forever()
            break
        except OSError as e:
            print(f"Port {port} dolu, sonraki port deneniyor... ({e})")
            continue

if __name__ == "__main__":
    start_server()
