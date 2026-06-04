import customtkinter as ctk
from tkinter import filedialog
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk

# ====================================================
# LOAD MODEL
# ====================================================
model = YOLO(r"C:\Users\ASUS\OneDrive\Desktop\PPE_project\best.pt")

# ====================================================
# APP SETTINGS
# ====================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("PPE Detection System")

app.geometry("1400x850")

app.configure(fg_color="#0f172a")

# ====================================================
# TITLE
# ====================================================
title = ctk.CTkLabel(
    app,
    text="🦺 PPE Detection System",
    font=("Arial", 38, "bold"),
    text_color="#38bdf8"
)

title.pack(pady=20)

# ====================================================
# MAIN FRAME
# ====================================================
main_frame = ctk.CTkFrame(
    app,
    width=1250,
    height=650,
    corner_radius=25,
    fg_color="#1e293b"
)

main_frame.pack(pady=20)

# ====================================================
# VIDEO DISPLAY
# ====================================================
video_label = ctk.CTkLabel(
    main_frame,
    text="",
    width=1150,
    height=600
)

video_label.pack(pady=20)

# ====================================================
# SHOW FRAME FUNCTION
# ====================================================
def show_frame(frame):

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(frame)

    img = img.resize((1150, 600))

    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk

    video_label.configure(image=imgtk)

# ====================================================
# PROCESS FRAME FUNCTION
# ====================================================
def process_frame(frame):

    frame = cv2.resize(frame, (640, 480))

    results = model.predict(
        frame,
        imgsz=320,
        conf=0.4,
        verbose=False
    )

    frame = results[0].plot()

    return frame

# ====================================================
# WEBCAM FUNCTION
# ====================================================
def start_webcam():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = process_frame(frame)

        show_frame(frame)

        app.update_idletasks()
        app.update()

    cap.release()

# ====================================================
# VIDEO FUNCTION
# ====================================================
def open_video():

    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi")]
    )

    if not file_path:
        return

    cap = cv2.VideoCapture(file_path)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = process_frame(frame)

        show_frame(frame)

        app.update_idletasks()
        app.update()

    cap.release()

# ====================================================
# IMAGE FUNCTION
# ====================================================
def upload_image():

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )

    if not file_path:
        return

    frame = cv2.imread(file_path)

    frame = process_frame(frame)

    show_frame(frame)

# ====================================================
# PHONE CAMERA FUNCTION
# ====================================================
def phone_camera():

    ip = ctk.CTkInputDialog(
        text="Enter Phone Camera URL\n\nExample:\nhttp://192.168.1.5:8080/video",
        title="Phone Camera"
    ).get_input()

    if not ip:
        return

    cap = cv2.VideoCapture(ip)

    if not cap.isOpened():
        print("❌ Cannot connect to phone camera")
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            print("❌ Failed to read phone camera")
            break

        frame = process_frame(frame)

        show_frame(frame)

        app.update_idletasks()
        app.update()

    cap.release()

# ====================================================
# BUTTON FRAME
# ====================================================
btn_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

btn_frame.pack(pady=20)

# ====================================================
# BUTTON STYLE
# ====================================================
btn_width = 220
btn_height = 55

# ====================================================
# WEBCAM BUTTON
# ====================================================
webcam_btn = ctk.CTkButton(
    btn_frame,
    text="📷 Webcam",
    command=start_webcam,
    width=btn_width,
    height=btn_height,
    corner_radius=20,
    font=("Arial", 18, "bold"),
    fg_color="#2563eb",
    hover_color="#1d4ed8"
)

webcam_btn.grid(row=0, column=0, padx=15)

# ====================================================
# VIDEO BUTTON
# ====================================================
video_btn = ctk.CTkButton(
    btn_frame,
    text="🎥 Video",
    command=open_video,
    width=btn_width,
    height=btn_height,
    corner_radius=20,
    font=("Arial", 18, "bold"),
    fg_color="#7c3aed",
    hover_color="#6d28d9"
)

video_btn.grid(row=0, column=1, padx=15)

# ====================================================
# IMAGE BUTTON
# ====================================================
image_btn = ctk.CTkButton(
    btn_frame,
    text="🖼 Upload Image",
    command=upload_image,
    width=btn_width,
    height=btn_height,
    corner_radius=20,
    font=("Arial", 18, "bold"),
    fg_color="#059669",
    hover_color="#047857"
)

image_btn.grid(row=0, column=2, padx=15)

# ====================================================
# PHONE CAMERA BUTTON
# ====================================================
phone_btn = ctk.CTkButton(
    btn_frame,
    text="📱 Phone Camera",
    command=phone_camera,
    width=btn_width,
    height=btn_height,
    corner_radius=20,
    font=("Arial", 18, "bold"),
    fg_color="#dc2626",
    hover_color="#b91c1c"
)

phone_btn.grid(row=0, column=3, padx=15)

# ====================================================
# RUN APP
# ====================================================
app.mainloop()  