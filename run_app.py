import webview
import threading
from app import app

def run_flask():
    app.run(port=5000)

t = threading.Thread(target=run_flask)
t.daemon = True
t.start()

window = webview.create_window(
    "Vortex",
    "http://127.0.0.1:5000",
    width=420,      # عرض جوال
    height=820,     # طول جوال
    resizable=False # ❗ يمنع تكبير النافذة
)

webview.start()