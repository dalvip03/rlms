import tkinter as tk
from tkinter import messagebox
from teacher_register import *

def teacher_button_click():
    messagebox.showinfo("Teacher Button Clicked", "Teacher button clicked")

def student_button_click():
    messagebox.showinfo("Student Button Clicked", "Student button clicked")

# Create the main window
interface_root = tk.Tk()
interface_root.title("RMLS")
interface_root.geometry("500x500")  # was 500x500
interface_root.state("zoomed")

# Create a frame to contain all the elements
frame = tk.Frame(interface_root, borderwidth=2, relief="solid", height=800, width=1200)
frame.pack(pady=50)  # Add padding to center the frame vertically

'''# Add an image to the left side
image_path = "C:/Users/PC NO 4/Desktop/harshal123/rlmslogo3.png"  # Change this to the path of your image
image = tk.PhotoImage(file=image_path)
resized_image = image.subsample(1, 1)
image_label = tk.Label(frame, image=resized_image)
image_label.grid(row=1, column=1, rowspan=8, padx=6, pady=6)

college_label.grid(row=0, column=1, padx=10, pady=10)'''

'''# Add an image to the topmost right corner
image_path = "C:/Users/PC NO 4/Desktop/harshal123/kirtilogo.png"  # Change this to the path of your image
image = tk.PhotoImage(file=image_path)
resized_image = image.subsample(3, 3)
image_label = tk.Label(frame, image=resized_image)
image_label.grid(row=0, column=2, padx=40, pady=10)'''

course_label = tk.Label(frame, text="REMOTE LAB\nMONITORING", font=("Times", 20, "bold"))
course_label.grid(row=1, column=2, padx=15, pady=15)

def command_t1():
    interface_root.destroy()
def command_t2():
    open_teacher()
def command_t3():
    command_t1()
    command_t2()

# Add buttons for Teacher and Student
teacher_button = tk.Button(frame, text="Teacher", command=command_t3)
teacher_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")#'#D0E6A5'

'''def command_s1():
    interface_root.destroy()
def command_s2():
    open_student()
def command_s3():
    command_s1()
    command_s2()

student_button = tk.Button(frame, text="Student", command=command_s3)
student_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")#'#FFDD94'''

# Run the Tkinter event loop
interface_root.mainloop()
