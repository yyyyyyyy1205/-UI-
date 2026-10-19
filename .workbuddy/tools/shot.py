import base64, json, os, subprocess, sys, time, urllib.request
import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9333
URL = "http://localhost:5180/"
OUT = r"E:\新建文件夹\exp2-vue\.workbuddy\exp2-report\screenshots"
PROFILE = r"E:\新建文件夹\exp2-vue\.workbuddy\tools\edge-profile"

os.makedirs(OUT, exist_ok=True)

proc = subprocess.Popen(
    [EDGE, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
     "--no-proxy-server", "--hide-scrollbars", "--force-device-scale-factor=2",
     "--remote-allow-origins=*",
     f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)

def wait_json(path, tries=60):
    for _ in range(tries):
        try:
            op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            return json.load(op.open(f"http://127.0.0.1:{PORT}{path}", timeout=2))
        except Exception:
            time.sleep(0.5)
    raise RuntimeError("devtools not reachable")

targets = wait_json("/json/list")
page = [t for t in targets if t["type"] == "page"][0]
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30,
                                 http_proxy_host=None, http_proxy_port=None)
_id = [0]


def send(method, params=None):
    _id[0] += 1
    ws.send(json.dumps({"id": _id[0], "method": method, "params": params or {}}))
    while True:
        data = json.loads(ws.recv())
        if data.get("id") == _id[0]:
            if "error" in data:
                raise RuntimeError(f"{method}: {data['error']}")
            return data.get("result", {})


send("Page.enable")
send("Runtime.enable")
send("Emulation.setDeviceMetricsOverride",
     {"width": 620, "height": 900, "deviceScaleFactor": 2, "mobile": False})
send("Page.navigate", {"url": URL})
time.sleep(4)


def js(expr):
    r = send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return r.get("result", {}).get("value")


def shot(name, full=True):
    r = send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": full})
    p = os.path.join(OUT, name)
    with open(p, "wb") as f:
        f.write(base64.b64decode(r["data"]))
    print("SAVED", p, os.path.getsize(p))


def click(text):
    q = json.dumps(text, ensure_ascii=False)
    expr = ("(function(){var t=" + q + ";var bs=document.querySelectorAll('button');"
            "for(var i=0;i<bs.length;i++){if(bs[i].innerText.trim().indexOf(t)>=0){"
            "bs[i].click();return 'ok:'+bs[i].innerText.trim();}}return 'notfound';})()")
    print("CLICK", text, "->", js(expr))


def fill_input(value):
    q = json.dumps(value, ensure_ascii=False)
    expr = ("(function(){var i=document.querySelector('input');"
            "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
            "s.call(i," + q + ");i.dispatchEvent(new Event('input',{bubbles:true}));return i.value;})()")
    print("INPUT", value, "->", js(expr))


print("title:", js("document.title"))
shot("01-overview.png")

fill_input("Vue")
time.sleep(1)
shot("02-search.png")

fill_input("")
time.sleep(0.6)

click("展开简介")
time.sleep(0.8)
shot("03-intro.png")

click("编辑信息")
time.sleep(0.8)
shot("04-edit.png")

click("取消")
time.sleep(0.6)
click("查看详情")
time.sleep(0.8)
shot("05-detail.png")

click("关闭")
time.sleep(0.6)
click("查看源码")
time.sleep(0.8)
shot("06-source.png")
click("关闭")
time.sleep(0.6)

click("暗色模式")
time.sleep(1.2)
shot("07-dark.png")
click("亮色模式")
time.sleep(1.0)
shot("08-light-restored.png")

ws.close()
try:
    proc.terminate()
except Exception:
    pass
print("DONE")
