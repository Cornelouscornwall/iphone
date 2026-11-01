import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# Try importing PIL safely
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("WARNING: Pillow module not found. Install it with 'pip install Pillow' to display PNG images.")

# ==========================================================
# PROJECT: LOCKDOWN
# ==========================================================

# -------------------------
# COLOURS
# -------------------------

BG = "#101820"
PANEL = "#192936"
PANEL_LIGHT = "#263D4D"
ACCENT = "#00C2A8"
TEXT = "#EAF2F5"
MUTED = "#91A6B2"
RED = "#E05252"
YELLOW = "#E6B84C"

# -------------------------
# GAME VARIABLES
# -------------------------

current_room = "entrance"
inventory = []

generator_powered = False
battery_used = False

wrong_attempts = 0
game_over = False
game_won = False

image_cache = {}

# -------------------------
# ROOM DATA
# -------------------------

rooms = {
    "entrance": {
        "name": "MAIN ENTRANCE",
        "description": "You are inside an abandoned underground research facility. Emergency lights flicker above you. The main exit is locked. You need to restore power and find a way out.",
        "exits": {
            "NORTH": "laboratory",
            "EAST": "storage"
        },
        "items": []
    },

    "laboratory": {
        "name": "RESEARCH LABORATORY",
        "description": "Broken computers and scientific equipment cover the laboratory. A portable battery has been left on a desk.",
        "exits": {
            "SOUTH": "entrance",
            "EAST": "security"
        },
        "items": ["battery"]
    },

    "storage": {
        "name": "STORAGE ROOM",
        "description": "Old equipment and maintenance supplies fill the storage room. You notice a spare electrical fuse and a small note.",
        "exits": {
            "WEST": "entrance",
            "NORTH": "generator"
        },
        "items": ["fuse", "code note"]
    },

    "security": {
        "name": "SECURITY ROOM",
        "description": "Security monitors line the walls. A keycard sits beside the control desk.",
        "exits": {
            "WEST": "laboratory",
            "NORTH": "control"
        },
        "items": ["keycard"]
    },

    "generator": {
        "name": "GENERATOR ROOM",
        "description": "A large generator occupies the centre of the room. It is offline and needs a replacement fuse.",
        "exits": {
            "SOUTH": "storage",
            "EAST": "control"
        },
        "items": []
    },

    "control": {
        "name": "CONTROL ROOM",
        "description": "The main control console is inactive. A backup power terminal sits beside it. A locked door leads to the escape chamber.",
        "exits": {
            "SOUTH": "security",
            "WEST": "generator",
            "NORTH": "escape"
        },
        "items": []
    },

    "escape": {
        "name": "ESCAPE CHAMBER",
        "description": "You have reached the final escape chamber. A keypad controls the emergency exit. Enter the correct four-digit code to escape.",
        "exits": {
            "SOUTH": "control"
        },
        "items": []
    }
}

# -------------------------
# IMAGE FILES
# -------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------
# MAIN WINDOW
# -------------------------

root = tk.Tk()
root.title("PROJECT: LOCKDOWN")
root.geometry("1150x800")
root.minsize(950, 700)
root.configure(bg=BG)

# ==========================================================
# USER INTERFACE HELPERS
# ==========================================================

def make_button(parent, text, command, colour=ACCENT):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=colour,
        fg=TEXT,
        activebackground="#087F73",
        activeforeground=TEXT,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=9
    )


def log_message(message):
    log_box.config(state="normal")
    log_box.insert("end", message + "\n")
    log_box.see("end")
    log_box.config(state="disabled")


def get_room():
    return rooms[current_room]


# ==========================================================
# ROOM ILLUSTRATIONS
# ==========================================================

def draw_room_image():

    canvas.delete("all")

    # 1. Attempt loading image file (checks script directory or images/ folder)
    image_paths = [
        os.path.join(SCRIPT_DIR, current_room + ".png"),
        os.path.join(SCRIPT_DIR, "images", current_room + ".png")
    ]

    target_path = None
    for path in image_paths:
        if os.path.exists(path):
            target_path = path
            break

    if target_path and HAS_PIL:
        try:
            if current_room not in image_cache:
                image = Image.open(target_path)
                image = image.convert("RGB")
                image = image.resize((850, 245), Image.Resampling.LANCZOS)
                image_cache[current_room] = ImageTk.PhotoImage(image)

            canvas.create_image(
                0, 0,
                image=image_cache[current_room],
                anchor="nw"
            )
            # Store reference to prevent Python garbage collection
            canvas.image_ref = image_cache[current_room]
            return

        except Exception as e:
            print(f"Error rendering image {target_path}: {e}")
    else:
        # Print diagnostic message to console if image isn't found
        print(f"DEBUG: Image '{current_room}.png' not found in: {SCRIPT_DIR}")

    # 2. Fallback: Draw procedural canvas shapes if PNG fails or doesn't exist
    width = 850
    height = 245

    # Background
    canvas.create_rectangle(
        0, 0, width, height,
        fill="#142B38",
        outline=""
    )

    # Floor
    canvas.create_rectangle(
        0, 185, width, height,
        fill="#263640",
        outline=""
    )

    # Ceiling lights
    for x in [100, 320, 540, 760]:
        canvas.create_rectangle(
            x - 35, 12, x + 35, 22,
            fill=YELLOW,
            outline=""
        )

    # Side walls
    canvas.create_rectangle(
        0, 0, 12, height,
        fill="#314957",
        outline=""
    )

    canvas.create_rectangle(
        width - 12, 0, width, height,
        fill="#314957",
        outline=""
    )

    # Room-specific illustrations

    if current_room == "entrance":

        # Main door
        canvas.create_rectangle(
            325, 45, 525, 185,
            fill="#405563",
            outline=TEXT,
            width=3
        )

        canvas.create_rectangle(
            345, 60, 505, 175,
            fill="#192936",
            outline=ACCENT,
            width=2
        )

        canvas.create_oval(
            475, 110, 490, 125,
            fill=YELLOW,
            outline=""
        )

        canvas.create_text(
            425, 90,
            text="EXIT LOCKED",
            fill=RED,
            font=("Arial", 14, "bold")
        )

        canvas.create_text(
            425, 215,
            text="MAIN ENTRANCE",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )

    elif current_room == "laboratory":

        # Laboratory bench
        canvas.create_rectangle(
            100, 125, 750, 155,
            fill="#536B79",
            outline=TEXT
        )

        canvas.create_rectangle(
            140, 155, 160, 195,
            fill="#536B79"
        )

        canvas.create_rectangle(
            680, 155, 700, 195,
            fill="#536B79"
        )

        # Equipment
        for x in [200, 350, 500, 650]:
            canvas.create_rectangle(
                x, 70, x + 55, 125,
                fill="#193C4C",
                outline=ACCENT,
                width=2
            )

            canvas.create_line(
                x + 10, 85, x + 45, 85,
                fill=ACCENT,
                width=2
            )

        canvas.create_text(
            425, 215,
            text="RESEARCH EQUIPMENT",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )

    elif current_room == "storage":

        # Storage boxes
        for x, y in [(100, 90), (220, 120), (350, 75),
                     (500, 110), (650, 80)]:

            canvas.create_rectangle(
                x, y, x + 90, y + 75,
                fill="#795B3E",
                outline=YELLOW,
                width=2
            )

            canvas.create_line(
                x + 45, y, x + 45, y + 75,
                fill=YELLOW
            )

        canvas.create_text(
            425, 215,
            text="MAINTENANCE STORAGE",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )

    elif current_room == "security":

        # Monitors
        for x in [150, 350, 550]:
            canvas.create_rectangle(
                x, 45, x + 125, 125,
                fill="#07141C",
                outline=ACCENT,
                width=3
            )

            canvas.create_text(
                x + 62, 85,
                text="NO SIGNAL",
                fill=RED,
                font=("Arial", 10, "bold")
            )

        # Desk
        canvas.create_rectangle(
            100, 150, 750, 175,
            fill="#536B79"
        )

        canvas.create_text(
            425, 215,
            text="SECURITY SYSTEM",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )

    elif current_room == "generator":

        # Generator body
        canvas.create_rectangle(
            285, 65, 565, 180,
            fill="#344B58",
            outline=YELLOW,
            width=4
        )

        # Generator vents
        for y in [85, 105, 125, 145]:
            canvas.create_line(
                315, y, 535, y,
                fill=MUTED,
                width=4
            )

        canvas.create_text(
            425, 105,
            text="GENERATOR",
            fill=TEXT,
            font=("Arial", 14, "bold")
        )

        canvas.create_text(
            425, 215,
            text="POWER SYSTEM",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )

        if generator_powered:
            canvas.create_text(
                425, 40,
                text="POWER ONLINE",
                fill=ACCENT,
                font=("Arial", 13, "bold")
            )
        else:
            canvas.create_text(
                425, 40,
                text="POWER OFFLINE",
                fill=RED,
                font=("Arial", 13, "bold")
            )

    elif current_room == "control":

        # Control panels
        for x in [110, 340, 570]:
            canvas.create_rectangle(
                x, 55, x + 165, 165,
                fill="#07141C",
                outline=ACCENT,
                width=3
            )

            for i in range(3):
                canvas.create_oval(
                    x + 20 + i * 40, 75,
                    x + 32 + i * 40, 87,
                    fill=ACCENT
                )

            canvas.create_line(
                x + 20, 115, x + 140, 115,
                fill=YELLOW,
                width=2
            )

        canvas.create_text(
            425, 215,
            text="MAIN CONTROL SYSTEM",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )

    elif current_room == "escape":

        # Escape door
        canvas.create_rectangle(
            300, 35, 550, 190,
            fill="#405563",
            outline=ACCENT,
            width=4
        )

        canvas.create_rectangle(
            320, 55, 530, 170,
            fill="#192936",
            outline=TEXT,
            width=2
        )

        # Keypad
        canvas.create_rectangle(
            575, 80, 680, 165,
            fill="#07141C",
            outline=YELLOW,
            width=3
        )

        for x in [595, 620, 645]:
            for y in [100, 120, 140]:
                canvas.create_oval(
                    x, y, x + 10, y + 10,
                    fill=ACCENT
                )

        canvas.create_text(
            425, 215,
            text="EMERGENCY EXIT",
            fill=TEXT,
            font=("Arial", 12, "bold")
        )


# ==========================================================
# INVENTORY
# ==========================================================

def take_item(item):

    if game_over or game_won:
        return

    if item not in get_room()["items"]:
        return

    get_room()["items"].remove(item)
    inventory.append(item)

    log_message("ITEM COLLECTED: " + item.upper())

    update_screen()


def use_item(item):

    global generator_powered
    global battery_used

    if game_over or game_won:
        return

    if item not in inventory:
        return

    if item == "fuse" and current_room == "generator":

        generator_powered = True
        inventory.remove("fuse")

        log_message("GENERATOR POWER RESTORED!")

        messagebox.showinfo(
            "POWER RESTORED",
            "The generator is now running!"
        )

    elif item == "battery" and current_room == "control":

        battery_used = True
        inventory.remove("battery")

        log_message("BACKUP BATTERY ACTIVATED!")

        messagebox.showinfo(
            "BACKUP POWER",
            "The backup battery has been connected."
        )

    elif item == "keycard":

        log_message(
            "The keycard grants access to restricted areas."
        )

    elif item == "code note":

        messagebox.showinfo(
            "EMERGENCY CODE",
            "The note reads:\n\nEMERGENCY ESCAPE CODE: 4312"
        )

    else:

        log_message(
            "You cannot use the " + item + " here."
        )

    update_screen()


# ==========================================================
# MOVEMENT
# ==========================================================

def move_player(direction):

    global current_room

    if game_over or game_won:
        return

    exits = get_room()["exits"]

    if direction not in exits:
        return

    destination = exits[direction]

    # Keycard requirement
    if current_room == "security" and destination == "control":

        if "keycard" not in inventory:
            messagebox.showwarning(
                "ACCESS DENIED",
                "You need the security keycard."
            )
            return

    # Generator requirement
    if current_room == "generator" and destination == "control":

        if not generator_powered:
            messagebox.showwarning(
                "ACCESS DENIED",
                "Restore generator power first."
            )
            return

    # Escape requirements
    if destination == "escape":

        if not generator_powered:
            messagebox.showwarning(
                "ACCESS DENIED",
                "You need to restore generator power."
            )
            return

        if not battery_used:
            messagebox.showwarning(
                "ACCESS DENIED",
                "You need to activate the backup battery."
            )
            return

    current_room = destination

    log_message(
        "MOVED " + direction + " TO "
        + get_room()["name"]
    )

    update_screen()


# ==========================================================
# ESCAPE CODE
# ==========================================================

def enter_code():

    global wrong_attempts
    global game_over
    global game_won

    if game_over or game_won:
        return

    code = simpledialog.askstring(
        "ESCAPE KEYPAD",
        "Enter the four-digit emergency code:",
        parent=root
    )

    if code is None:
        return

    if code.strip() == "4312":

        game_won = True

        log_message("ACCESS GRANTED. EXIT UNLOCKED.")

        messagebox.showinfo(
            "MISSION COMPLETE",
            "You successfully escaped the facility!\n\nMISSION COMPLETE."
        )

    else:

        wrong_attempts += 1
        remaining = 3 - wrong_attempts

        log_message("INCORRECT CODE.")

        if remaining > 0:

            messagebox.showwarning(
                "INCORRECT CODE",
                str(remaining) + " attempts remaining."
            )

        else:

            game_over = True

            log_message("PERMANENT SECURITY LOCKDOWN.")

            messagebox.showerror(
                "GAME OVER",
                "You entered the wrong code three times.\n\nThe facility is now locked down."
            )

    update_screen()


# ==========================================================
# RESTART
# ==========================================================

def restart_game():

    global current_room
    global inventory
    global generator_powered
    global battery_used
    global wrong_attempts
    global game_over
    global game_won

    current_room = "entrance"
    inventory = []

    generator_powered = False
    battery_used = False

    wrong_attempts = 0
    game_over = False
    game_won = False

    rooms["laboratory"]["items"] = ["battery"]
    rooms["storage"]["items"] = ["fuse", "code note"]
    rooms["security"]["items"] = ["keycard"]

    image_cache.clear()

    log_box.config(state="normal")
    log_box.delete("1.0", "end")
    log_box.config(state="disabled")

    log_message("GAME RESTARTED.")
    log_message("Welcome to PROJECT: LOCKDOWN.")

    update_screen()


# ==========================================================
# FACILITY MAP
# ==========================================================

def show_map():

    window = tk.Toplevel(root)
    window.title("FACILITY MAP")
    window.geometry("700x550")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="FACILITY MAP",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=ACCENT
    ).pack(pady=15)

    map_canvas = tk.Canvas(
        window,
        width=650,
        height=450,
        bg=PANEL,
        highlightthickness=0
    )
    map_canvas.pack(padx=15, pady=10)

    positions = {
        "entrance": (110, 220),
        "laboratory": (110, 90),
        "storage": (300, 220),
        "security": (300, 90),
        "generator": (500, 220),
        "control": (500, 90),
        "escape": (500, 360)
    }

    connections = [
        ("entrance", "laboratory"),
        ("entrance", "storage"),
        ("laboratory", "security"),
        ("storage", "generator"),
        ("security", "control"),
        ("generator", "control"),
        ("control", "escape")
    ]

    for first, second in connections:

        x1, y1 = positions[first]
        x2, y2 = positions[second]

        map_canvas.create_line(
            x1, y1, x2, y2,
            fill=MUTED,
            width=3
        )

    for room_id, position in positions.items():

        x, y = position

        colour = ACCENT if room_id == current_room else PANEL_LIGHT

        map_canvas.create_rectangle(
            x - 70, y - 25,
            x + 70, y + 25,
            fill=colour,
            outline=TEXT,
            width=2
        )

        map_canvas.create_text(
            x, y,
            text=rooms[room_id]["name"],
            fill=TEXT,
            font=("Arial", 8, "bold"),
            width=130
        )


# ==========================================================
# HELP
# ==========================================================

def show_help():

    messagebox.showinfo(
        "HOW TO PLAY",
        "PROJECT: LOCKDOWN\n\n"
        "OBJECTIVE:\n"
        "Escape the underground research facility.\n\n"
        "CONTROLS:\n"
        "1. Use the direction buttons to move.\n"
        "2. Collect items using TAKE ITEM.\n"
        "3. Use items from your inventory.\n"
        "4. Open the facility map to see the layout.\n\n"
        "ITEMS:\n"
        "Battery - Control room backup power.\n"
        "Fuse - Generator power.\n"
        "Keycard - Security access.\n"
        "Code note - Reveals the escape code.\n\n"
        "ESCAPE CODE: 4312\n"
        "You have three attempts."
    )


# ==========================================================
# BUILD INTERFACE
# ==========================================================

# HEADER

header = tk.Frame(root, bg="#0A1118", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="PROJECT: LOCKDOWN",
    font=("Arial", 24, "bold"),
    bg="#0A1118",
    fg=ACCENT
).pack(side="left", padx=25, pady=18)

tk.Label(
    header,
    text="UNDERGROUND RESEARCH FACILITY",
    font=("Arial", 10, "bold"),
    bg="#0A1118",
    fg=MUTED
).pack(side="right", padx=25)


# MAIN LAYOUT

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=15, pady=15)

sidebar = tk.Frame(main, bg=PANEL, width=250)
sidebar.pack(side="left", fill="y", padx=(0, 15))
sidebar.pack_propagate(False)

content = tk.Frame(main, bg=BG)
content.pack(side="right", fill="both", expand=True)


# SIDEBAR

tk.Label(
    sidebar,
    text="PLAYER STATUS",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=ACCENT
).pack(anchor="w", padx=15, pady=(20, 10))

status_label = tk.Label(
    sidebar,
    text="STATUS: ACTIVE",
    bg=PANEL,
    fg=ACCENT,
    font=("Arial", 10, "bold")
)
status_label.pack(anchor="w", padx=15, pady=5)

power_label = tk.Label(
    sidebar,
    text="GENERATOR: OFFLINE",
    bg=PANEL,
    fg=RED
)
power_label.pack(anchor="w", padx=15, pady=5)

battery_label = tk.Label(
    sidebar,
    text="BACKUP: INACTIVE",
    bg=PANEL,
    fg=RED
)
battery_label.pack(anchor="w", padx=15, pady=5)

tk.Label(
    sidebar,
    text="INVENTORY",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=ACCENT
).pack(anchor="w", padx=15, pady=(25, 10))

inventory_frame = tk.Frame(sidebar, bg=PANEL)
inventory_frame.pack(fill="x", padx=10)

tk.Label(
    sidebar,
    text="SYSTEM CONTROLS",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=ACCENT
).pack(anchor="w", padx=15, pady=(25, 10))

make_button(
    sidebar, "FACILITY MAP", show_map, PANEL_LIGHT
).pack(fill="x", padx=15, pady=5)

make_button(
    sidebar, "HOW TO PLAY", show_help, PANEL_LIGHT
).pack(fill="x", padx=15, pady=5)

make_button(
    sidebar, "RESTART GAME", restart_game, "#24516A"
).pack(fill="x", padx=15, pady=5)

make_button(
    sidebar, "QUIT GAME", root.destroy, RED
).pack(fill="x", padx=15, pady=5)


# ROOM TITLE

room_title = tk.Label(
    content,
    text="MAIN ENTRANCE",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=ACCENT
)
room_title.pack(anchor="w", pady=(5, 10))


# ROOM IMAGE CANVAS (Fixed size and layout anchor)
canvas = tk.Canvas(
    content,
    width=850,
    height=245,
    bg="#142B38",
    highlightthickness=0
)
canvas.pack(anchor="w", pady=5)


# IMAGE CAPTION

visual_caption = tk.Label(
    content,
    text="FACILITY ENVIRONMENT",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=MUTED
)
visual_caption.pack(anchor="w", pady=5)


# ROOM DESCRIPTION

description_label = tk.Label(
    content,
    text="",
    font=("Arial", 11),
    bg=PANEL,
    fg=TEXT,
    justify="left",
    anchor="nw",
    padx=15,
    pady=12,
    wraplength=800
)
description_label.pack(fill="x", pady=10)


# ROOM ITEMS

tk.Label(
    content,
    text="ITEMS IN THIS ROOM",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg=ACCENT
).pack(anchor="w", pady=5)

room_items_frame = tk.Frame(content, bg=BG)
room_items_frame.pack(fill="x")


# MOVEMENT

tk.Label(
    content,
    text="MOVEMENT",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg=ACCENT
).pack(anchor="w", pady=(12, 5))

movement_frame = tk.Frame(content, bg=BG)
movement_frame.pack(fill="x")


# ESCAPE KEYPAD BUTTON AREA

keypad_frame = tk.Frame(content, bg=BG)
keypad_frame.pack(fill="x")


# MISSION LOG

tk.Label(
    content,
    text="MISSION LOG",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg=ACCENT
).pack(anchor="w", pady=(12, 5))

log_box = tk.Text(
    content,
    height=5,
    bg="#0A1118",
    fg=TEXT,
    font=("Consolas", 9),
    relief="flat",
    wrap="word"
)
log_box.pack(fill="both", expand=True)

log_box.config(state="disabled")


# ==========================================================
# UPDATE SCREEN
# ==========================================================

def update_screen():

    room = get_room()

    room_title.config(text=room["name"])
    description_label.config(text=room["description"])

    # Draw room illustration or load PNG
    draw_room_image()

    visual_caption.config(
        text=room["name"] + " | FACILITY SECTOR"
    )

    # Update status

    if game_won:
        status_label.config(
            text="STATUS: MISSION COMPLETE",
            fg=ACCENT
        )

    elif game_over:
        status_label.config(
            text="STATUS: LOCKDOWN",
            fg=RED
        )

    else:
        status_label.config(
            text="STATUS: ACTIVE",
            fg=ACCENT
        )

    power_label.config(
        text="GENERATOR: "
        + ("ONLINE" if generator_powered else "OFFLINE"),
        fg=ACCENT if generator_powered else RED
    )

    battery_label.config(
        text="BACKUP: "
        + ("ACTIVE" if battery_used else "INACTIVE"),
        fg=ACCENT if battery_used else RED
    )

    # INVENTORY

    for widget in inventory_frame.winfo_children():
        widget.destroy()

    if not inventory:

        tk.Label(
            inventory_frame,
            text="Inventory empty",
            bg=PANEL,
            fg=MUTED
        ).pack(anchor="w", padx=5, pady=5)

    for item in inventory:

        item_frame = tk.Frame(
            inventory_frame,
            bg=PANEL_LIGHT
        )
        item_frame.pack(fill="x", pady=3)

        tk.Label(
            item_frame,
            text=item.upper(),
            bg=PANEL_LIGHT,
            fg=TEXT,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=7, pady=7)

        tk.Button(
            item_frame,
            text="USE",
            command=lambda selected=item: use_item(selected),
            bg=ACCENT,
            fg=BG,
            font=("Arial", 8, "bold"),
            relief="flat"
        ).pack(side="right", padx=5, pady=4)

    # ROOM ITEMS

    for widget in room_items_frame.winfo_children():
        widget.destroy()

    if room["items"]:

        for item in room["items"]:

            item_frame = tk.Frame(
                room_items_frame,
                bg=PANEL
            )
            item_frame.pack(fill="x", pady=3)

            tk.Label(
                item_frame,
                text=item.upper(),
                bg=PANEL,
                fg=TEXT,
                font=("Arial", 10, "bold")
            ).pack(side="left", padx=10, pady=8)

            tk.Button(
                item_frame,
                text="TAKE ITEM",
                command=lambda selected=item: take_item(selected),
                bg=ACCENT,
                fg=BG,
                font=("Arial", 8, "bold"),
                relief="flat"
            ).pack(side="right", padx=10, pady=5)

    else:

        tk.Label(
            room_items_frame,
            text="No items available.",
            bg=BG,
            fg=MUTED
        ).pack(anchor="w")

    # MOVEMENT BUTTONS

    for widget in movement_frame.winfo_children():
        widget.destroy()

    if not game_over and not game_won:

        for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:

            if direction in room["exits"]:

                make_button(
                    movement_frame,
                    direction,
                    lambda d=direction: move_player(d),
                    PANEL_LIGHT
                ).pack(side="left", padx=5, pady=5)

    # ESCAPE BUTTON

    for widget in keypad_frame.winfo_children():
        widget.destroy()

    if current_room == "escape" and not game_over and not game_won:

        make_button(
            keypad_frame,
            "ENTER ESCAPE CODE",
            enter_code,
            ACCENT
        ).pack(fill="x", pady=8)


# ==========================================================
# START GAME
# ==========================================================

log_message("PROJECT: LOCKDOWN INITIALISED.")
log_message("Welcome to the underground research facility.")
log_message("Find the equipment needed to escape.")

update_screen()

root.mainloop()