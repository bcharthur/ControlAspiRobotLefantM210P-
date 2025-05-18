# main.py

import threading
import tkinter as tk
from LefantM210P import LefantM210P

robot = LefantM210P()
pressed = set()
KEY_TO_CMD = {
    'Up': 'forward',
    'Down': 'backward',
    'Left': 'turn_left',
    'Right': 'turn_right',
}

def send_direction(cmd):
    robot.send_direction(cmd)

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

def update_battery_label(bat):
    battery_label.config(text=f"🔋 {bat}%")

# ─── UI ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Télécommande Lefant M210P")
root.geometry("450x340")
root.resizable(False, False)
root.bind('<KeyPress>', on_press)
root.bind('<KeyRelease>', on_release)
root.focus_set()

btn_up    = tk.Button(root, text="↑", font=("Arial", 24))
btn_down  = tk.Button(root, text="↓", font=("Arial", 24))
btn_left  = tk.Button(root, text="←", font=("Arial", 24))
btn_right = tk.Button(root, text="→", font=("Arial", 24))
btn_stop  = tk.Button(root, text="■", font=("Arial", 18), bg="red", fg="white")

# Boutons de direction (clicks souris)
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

btn_up.place(x=125, y=20, width=50, height=50)
btn_left.place(x=50, y=100, width=50, height=50)
btn_stop.place(x=125, y=100, width=50, height=50)
btn_right.place(x=200, y=100, width=50, height=50)
btn_down.place(x=125, y=180, width=50, height=50)

status_label.place(x=0, y=260, width=300, height=40)
battery_label.place(x=360, y=10)

tk.Button(root, text="🧹 Ménage", width=12, command=lambda: [robot.start_clean(), status_label.config(text="🧹 Démarrage…")]).place(x=310, y=60)
tk.Button(root, text="⏹️ Stop", width=12, command=lambda: [robot.stop_clean(), status_label.config(text="⏹️ Stop ménage")]).place(x=310, y=100)
tk.Button(root, text="🏠 Base", width=12, command=lambda: [robot.return_to_base(), status_label.config(text="🏠 Retour à la base")]).place(x=310, y=140)
tk.Button(root, text="❌ Annuler", width=12, command=lambda: [robot.cancel_return(), status_label.config(text="❌ Annule retour")]).place(x=310, y=180)

# Threads
threading.Thread(target=robot.keep_alive, daemon=True).start()
threading.Thread(target=lambda: robot.update_battery_loop(update_battery_label), daemon=True).start()

root.mainloop()
