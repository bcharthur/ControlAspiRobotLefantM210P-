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

d = tinytuya.OutletDevice(dev_id=DEVICE_ID, address=DEVICE_IP, local_key=LOCAL_KEY)
d.set_version(TUYA_VERSION)
d.socketPersistent = True

# Mapping clavier
KEY_TO_CMD = {
    'Up': 'forward',
    'Down': 'backward',
    'Left': 'turn_left',
    'Right': 'turn_right',
}
pressed = set()

def send_direction(cmd):
    try:
        d.set_value('4', cmd)
    except Exception as e:
        print("[Erreur TinyTuya]", e)

def on_press(event):
    k = event.keysym
    if k in KEY_TO_CMD and k not in pressed:
        pressed.add(k)
        send_direction(KEY_TO_CMD[k])
        status_label.config(text=f"→ {k}")

def on_release(event):
    k = event.keysym
    if k in KEY_TO_CMD and k in pressed:
        pressed.remove(k)
        send_direction("stop")
        status_label.config(text="■ stop")

def keep_alive():
    import time
    while True:
        try:
            d.status()
        except: pass
        time.sleep(30)

def update_battery():
    import time
    while True:
        try:
            bat = d.status().get("dps", {}).get("6")
            if bat is not None:
                battery_label.config(text=f"🔋 {bat}%")
        except: pass
        time.sleep(5)

def start_clean():
    d.set_value('3', 'smart')
    d.set_value('2', True)
    status_label.config(text="🧹 Démarrage…")

def stop_clean():
    d.set_value('2', False)
    status_label.config(text="⏹️ Stop ménage")

def return_to_base():
    d.set_value('3', 'chargego')
    d.set_value('2', True)
    status_label.config(text="🏠 Retour à la base")

def cancel_return():
    d.set_value('2', False)
    status_label.config(text="❌ Annule retour")

# ─── UI ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Télécommande Lefant M210P")
root.geometry("450x340")
root.resizable(False, False)
root.bind('<KeyPress>', on_press)
root.bind('<KeyRelease>', on_release)
root.focus_set()

# Boutons de direction
btn_up    = tk.Button(root, text="↑", font=("Arial", 24))
btn_down  = tk.Button(root, text="↓", font=("Arial", 24))
btn_left  = tk.Button(root, text="←", font=("Arial", 24))
btn_right = tk.Button(root, text="→", font=("Arial", 24))
btn_stop  = tk.Button(root, text="■", font=("Arial", 18), bg="red", fg="white")

# Évènements manuels des boutons
btn_up.bind('<ButtonPress-1>', lambda e: on_press(type('E', (), {'keysym': 'Up'})))
btn_up.bind('<ButtonRelease-1>', lambda e: on_release(type('E', (), {'keysym': 'Up'})))
btn_down.bind('<ButtonPress-1>', lambda e: on_press(type('E', (), {'keysym': 'Down'})))
btn_down.bind('<ButtonRelease-1>', lambda e: on_release(type('E', (), {'keysym': 'Down'})))
btn_left.bind('<ButtonPress-1>', lambda e: on_press(type('E', (), {'keysym': 'Left'})))
btn_left.bind('<ButtonRelease-1>', lambda e: on_release(type('E', (), {'keysym': 'Left'})))
btn_right.bind('<ButtonPress-1>', lambda e: on_press(type('E', (), {'keysym': 'Right'})))
btn_right.bind('<ButtonRelease-1>', lambda e: on_release(type('E', (), {'keysym': 'Right'})))
btn_stop.config(command=lambda: send_direction('stop'))

status_label  = tk.Label(root, text="Prêt", font=("Arial", 14))
battery_label = tk.Label(root, text="🔋 -- %", font=("Arial", 12))

# Positionnement des boutons
btn_up.place(x=125, y=20, width=50, height=50)
btn_left.place(x=50, y=100, width=50, height=50)
btn_stop.place(x=125, y=100, width=50, height=50)
btn_right.place(x=200, y=100, width=50, height=50)
btn_down.place(x=125, y=180, width=50, height=50)

# Label état
status_label.place(x=0, y=260, width=300, height=40)
battery_label.place(x=360, y=10)

# Boutons action à droite
tk.Button(root, text="🧹 Ménage", width=12, command=start_clean).place(x=310, y=60)
tk.Button(root, text="⏹️ Stop", width=12, command=stop_clean).place(x=310, y=100)
tk.Button(root, text="🏠 Base", width=12, command=return_to_base).place(x=310, y=140)
tk.Button(root, text="❌ Annuler", width=12, command=cancel_return).place(x=310, y=180)

# Lancement des threads
threading.Thread(target=keep_alive, daemon=True).start()
threading.Thread(target=update_battery, daemon=True).start()

root.mainloop()
