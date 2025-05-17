#!/usr/bin/env python3
import tinytuya
import threading
import tkinter as tk

# ─── CONFIG ────────────────────────────────────────────────────────────────
DEVICE_ID    = "bf2b2fab90fe1fcd14dx1u"
DEVICE_IP    = "192.168.1.64"
LOCAL_KEY    = "wK)XqX(tawQ]`xs("
TUYA_VERSION = 3.4
# ────────────────────────────────────────────────────────────────────────────

# Initialisation du device
d = tinytuya.OutletDevice(
    dev_id=DEVICE_ID,
    address=DEVICE_IP,
    local_key=LOCAL_KEY
)
d.set_version(TUYA_VERSION)
d.socketPersistent = True

# mapping des touches → valeurs DPS
KEY_TO_CMD = {
    'Up':    'forward',
    'Down':  'backward',
    'Left':  'turn_left',
    'Right': 'turn_right',
}

pressed = set()

def send_direction(cmd: str):
    """Envoie la commande de direction via la DPS 4."""
    try:
        d.set_value('4', cmd)
    except Exception as e:
        print("Erreur TinyTuya:", e)

def on_press(event):
    ks = event.keysym
    if ks in KEY_TO_CMD and ks not in pressed:
        pressed.add(ks)
        send_direction(KEY_TO_CMD[ks])
        status_label.config(text=f"→ {ks}")

def on_release(event):
    ks = event.keysym
    # dès qu'on relâche une flèche, on stop
    if ks in KEY_TO_CMD and ks in pressed:
        pressed.remove(ks)
        send_direction('stop')
        status_label.config(text="■ stop")

def keep_alive():
    """Pour maintenir la connexion alive."""
    import time
    while True:
        try:
            d.status()
        except:
            pass
        time.sleep(30)

# ─── Création de la fenêtre ────────────────────────────────────────────────
root = tk.Tk()
root.title("Télécommande Lefant M210P")
root.geometry("300x340")
root.resizable(False, False)
root.bind('<KeyPress>',   on_press)
root.bind('<KeyRelease>',  on_release)
root.focus_set()

# boutons graphiques (optionnel)
btn_up    = tk.Button(root, text="↑", font=("Arial", 24))
btn_down  = tk.Button(root, text="↓", font=("Arial", 24))
btn_left  = tk.Button(root, text="←", font=("Arial", 24))
btn_right = tk.Button(root, text="→", font=("Arial", 24))
btn_stop  = tk.Button(root, text="■", font=("Arial", 18), bg="red", fg="white")

# on lie boutons → events clavier
btn_up.bind('<ButtonPress-1>',   lambda e: on_press(type('E',(),{'keysym':'Up'})))
btn_up.bind('<ButtonRelease-1>', lambda e: on_release(type('E',(),{'keysym':'Up'})))
btn_down.bind('<ButtonPress-1>',   lambda e: on_press(type('E',(),{'keysym':'Down'})))
btn_down.bind('<ButtonRelease-1>', lambda e: on_release(type('E',(),{'keysym':'Down'})))
btn_left.bind('<ButtonPress-1>',   lambda e: on_press(type('E',(),{'keysym':'Left'})))
btn_left.bind('<ButtonRelease-1>', lambda e: on_release(type('E',(),{'keysym':'Left'})))
btn_right.bind('<ButtonPress-1>',   lambda e: on_press(type('E',(),{'keysym':'Right'})))
btn_right.bind('<ButtonRelease-1>', lambda e: on_release(type('E',(),{'keysym':'Right'})))
btn_stop.config(command=lambda: send_direction('stop'))

status_label = tk.Label(root, text="Prêt", font=("Arial", 14), anchor='center')

# Placement
btn_up.place(x=125, y= 20, width=50, height=50)
btn_left.place(x= 50, y=100, width=50, height=50)
btn_stop.place(x=125, y=100, width=50, height=50)
btn_right.place(x=200, y=100, width=50, height=50)
btn_down.place(x=125, y=180, width=50, height=50)
status_label.place(x=0, y=260, width=300, height=40)

# démarre le thread keep-alive
threading.Thread(target=keep_alive, daemon=True).start()

root.mainloop()
