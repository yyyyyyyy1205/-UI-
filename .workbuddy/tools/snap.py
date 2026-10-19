import base64, json, os, subprocess, sys, time, urllib.request
import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9344
TARGET = sys.argv[1]
OUTPNG = sys.argv[2]
WIDTH = int(sys.argv[3]) if len(sys.argv) > 3 else 760
PROFILE = r"E:\新建文件夹\exp2-vue\.workbuddy\tools\edge-profile"

proc = subprocess.Popen(
    [EDGE, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
     "--no-proxy-server", "--hide-scrollbars", "--force-device-scale-factor=2",
     "--remote-allow-origins=*", "--allow-file-access-from-files",
     f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def wait_json(path, tries=60):
    for _ in range(tries):
        try:
            op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            return json.load(op.open(f"http://127.0.0.1:{PORT}{path}", timeout=2))
        except Exception:
            time.sleep(0.5)
    raise RuntimeError("devtools not reachable")

page = [t for t in wait_json("/json/list") if t["type"] == "page"][0]
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30,
                                 http_proxy_host=None, http_proxy_port=None)
_id = [0]

def send(method, params=None):
    _id[0] += 1
    ws.send(json.dumps({"id": _id[0], "method": method, "params": params or {}}))
    while True:
        d = json.loads(ws.recv())
        if d.get("id") == _id[0]:
            if "error" in d:
                raise RuntimeError(f"{method}: {d['error']}")
            return d.get("result", {})

send("Page.enable")
send("Emulation.setDeviceMetricsOverride",
     {"width": WIDTH, "height": 800, "deviceScaleFactor": 2, "mobile": False})
send("Page.navigate", {"url": TARGET})
time.sleep(3)
r = send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
with open(OUTPNG, "wb") as f:
    f.write(base64.b64decode(r["data"]))
print("SAVED", OUTPNG, os.path.getsize(OUTPNG))
ws.close()
try:
    proc.terminate()
except Exception:
    pass
