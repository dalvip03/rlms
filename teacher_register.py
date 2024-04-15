import random, tkinter as tk, paramiko, socket, time, sqlite3
from tkinter import Button, Entry, Label, ttk, messagebox
from plyer import notification
from teacher_course_interface import *
import mysql.connector 
from mysql.connector import Error


def open_teacher():
    # Define a common font
    common_font = ('Times', 12, "bold")

    # Function to generate a random CAPTCHA text
    def generate_captcha():
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        global captcha
        captcha = "".join(random.choice(characters) for _ in range(6))
        captcha_label.config(text=captcha)
    
    # Function to clear the entry fields
    def clear_entries():
        teacher_name_entry_login.delete(0, tk.END)
        teacher_id_entry.delete(0, tk.END)
        mobile_no_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        captcha_entry.delete(0, tk.END)
    
    # Function to handle the registration process with input validation
    def register_teacher():

        # Check if teacher already exists
        teacher_id = teacher_id_entry.get()
        query = "SELECT * FROM teachers WHERE teacher_id = %s"
        cursor.execute(query, (teacher_id,))
        existing_teacher = cursor.fetchone()
      
        # If teacher exists, show error message
        if existing_teacher:
          messagebox.showerror("Error", "Teacher with ID {} already exists.".format(teacher_id))
          return False
        
        # Otherwise, proceed with registration
        mobile_no = mobile_no_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        entered_captcha = captcha_entry.get()
    
        # Input validation
        if not teacher_id or not mobile_no or not email or not password:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return False
        elif not teacher_id.isdigit() or len(teacher_id) != 7:
            messagebox.showerror("Error", "teacher ID must be a 7-digit number.")
            return False
        elif not mobile_no.isdigit() or len(mobile_no) != 10:
            messagebox.showerror("Error", "Mobile number must be a 10-digit number.")
            return False
        elif "@" not in email or "." not in email or email.count("@") != 1:
            messagebox.showerror("Error", "Invalid email address.")
            return False
        elif entered_captcha != captcha:
            messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
            generate_captcha()
            return False
        else:
            # Registration successful
            # Store the data in the database
            query = "INSERT INTO teachers (teacher_id, mobile_no, email, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (teacher_id, mobile_no, email, password))
            connection.commit()

            # Show success message
            messagebox.showinfo("Registration Successful", "Teacher registered successfully!")
            return True
    
    # Create the main window
    root = tk.Tk()
    root.title("teacher Registration")
    root.state("zoomed")
    
    '''# Set the path to your ICO file
    icon_path = "C:/Users/kirti/Desktop/Avishkar/Kirti_logo.ico"
    # Change the favicon
    root.iconbitmap(icon_path)'''
    
    # Create a frame to contain all the elements
    main_frame = tk.Frame(root, borderwidth=2, relief="solid")
    main_frame.pack(pady=50)  # Add padding to center the frame vertically
    
    # Function to handle "Enter" key press and focus on the next entry
    
    def focus_next_entry(event, current_entry, next_entry):
        current_entry.focus_set()
        next_entry.focus_set()
    
    # Add an image to the left side
    '''image_path = "C:/Users/kcmitlab-19/Desktop/avishkar/Remote Lab Monitoring/Kirti_logo.png"  # Change this to the path of your image
    image = tk.PhotoImage(file=image_path)
    resized_image = image.subsample(5,5)
    image_label = tk.Label(main_frame, image=image)
    image_label.grid(row=1, column=0, rowspan=9, padx=10, pady=10)'''
    
    registration_label = tk.Label(main_frame, text="teacher Registration", font=("Times", 20, "bold"))
    registration_label.grid(row=0, column=3,padx=10, pady=10)
    
    teacher_name_label_login = tk.Label(main_frame, text="Teacher Name:",font=common_font)
    teacher_name_label_login.grid(row=1, column=2, padx=10, pady=10)
    teacher_name_entry_login = tk.Entry(main_frame)
    teacher_name_entry_login.grid(row=1, column=3, padx=10, pady=10)
    
    teacher_id_label = tk.Label(main_frame, text="Teacher ID (Roll N):",font=common_font)
    teacher_id_label.grid(row=2, column=2, padx=10, pady=10)
    teacher_id_entry = tk.Entry(main_frame)
    teacher_id_entry.grid(row=2, column=3, padx=10, pady=10)
    
    mobile_no_label = tk.Label(main_frame, text="Mobile No:",font=common_font)
    mobile_no_label.grid(row=3, column=2, padx=10, pady=10)
    mobile_no_entry = tk.Entry(main_frame)
    mobile_no_entry.grid(row=3, column=3, padx=10, pady=10)
    
    email_label = tk.Label(main_frame, text="Email:",font=common_font)
    email_label.grid(row=4, column=2, padx=10, pady=10)
    email_entry = tk.Entry(main_frame)
    email_entry.grid(row=4, column=3, padx=10, pady=10)
    
    password_label = tk.Label(main_frame, text="Password:",font=common_font)
    password_label.grid(row=5, column=2, padx=10, pady=10)
    password_entry = tk.Entry(main_frame, show="*")  # Mask the password
    password_entry.grid(row=5, column=3, padx=10, pady=10)
    
    # Generate and display CAPTCHA text
    captcha_label = Label(main_frame, text="", font=("Times", 17, "bold"), bg='mintcream', fg='red')
    captcha_label.grid(row=8, column=2, padx=10, pady=10)
    generate_captcha_button = Button(main_frame, text="Generate CAPTCHA", command=generate_captcha,font=common_font)
    generate_captcha_button.grid(row=8, column=3, padx=10, pady=10)
    
    # Label and Entry for user input
    captcha_label_entry = Label(main_frame, text="CAPTCHA:",font=common_font)
    captcha_label_entry.grid(row=7, column=2, padx=10, pady=10)
    captcha_entry = Entry(main_frame, font=("Times", "16", "bold"), width=10, fg='gray1')
    captcha_entry.grid(row=7, column=3, padx=10, pady=5)
    
    # Bind the "Enter" key for teacher_name_entry_login
    teacher_name_entry_login.bind("<Return>", lambda event, entry=teacher_id_entry: focus_next_entry(event, teacher_name_entry_login, entry))
    
    # Bind the "Enter" key for teacher_id_entry_login
    teacher_id_entry.bind("<Return>", lambda event, entry=mobile_no_entry: focus_next_entry(event, teacher_id_entry, entry))
    
    # Bind the "Enter" key for mobile_no_entry
    mobile_no_entry.bind("<Return>", lambda event, entry=email_entry: focus_next_entry(event, mobile_no_entry, entry))
    
    # Bind the "Enter" key for email_entry
    email_entry.bind("<Return>", lambda event, entry=password_entry: focus_next_entry(event, email_entry, entry))
    
    # Bind the "Enter" key for password_entry
    password_entry.bind("<Return>", lambda event, entry=captcha_entry: focus_next_entry(event, password_entry, entry))
    
    # Bind the "Enter" key for captcha_entry
    captcha_entry.bind("<Return>", )  # Assuming you want to submit the form on pressing Enter in the captcha_entry
    
    def vadidate_open_login():
        # Call course_validation to check if all fields are filled
        registeration_successful = register_teacher()
    
        # If validation is successful, open the teacher interface
        if registeration_successful:
            open_login_window()
    
    # Create buttons
    register_button = tk.Button(main_frame, text="Register", bg='green', fg='black',font=common_font, command=lambda: [vadidate_open_login(), root.destroy()])
    register_button.grid(row=9, column=3, padx=10, pady=10, columnspan=2, sticky="ew")
    # Bind the "Enter" key for password_entry
    
    clear_button = tk.Button(main_frame, text=" Clear", bg='red', fg='black',font=common_font, command=clear_entries)
    clear_button.grid(row=11, column=3, padx=10, pady=10, columnspan=2, sticky="ew")
    
    
    def open_login():
        # Call course_validation to check if all fields are filled
        login_successful = open_login_window()
    
    # If validation is successful, open the teacher interface
        if login_successful:
            root.destroy()
            open_login_window()
    
    login_button = tk.Button(main_frame, text="Login", bg='blue', fg='black',font=common_font, command=open_login)
    login_button.grid(row=10, column=3, padx=10, pady=10, columnspan=2,sticky="ew")
    
    # Center the frame in the window
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Function to open the login window
    def open_login_window():
    
        # Create the login window
        login_root = tk.Tk()
        login_root.title("teacher Login")
        login_root.state("zoomed")
    
            # Set the path to your ICO file
        '''icon_path = "C:/Users/kirti/Desktop/Avishkar/Kirti_logo.ico"
        # Change the favicon
        login_root.iconbitmap(icon_path)'''
    
        def join_class():
            teacher_name_entry = teacher_name_entry_login.get()  # Use nonlocal
            teacher_id = teacher_id_entry_login.get()
            password = password_entry_login.get()
            entered_captcha = captcha_entry.get()
    
                    # Input validation
            if not teacher_name_entry or not teacher_id or not password:
                messagebox.showerror("Error", "Please fill in all the fields.")
                return False
            elif not teacher_id.isdigit() or len(teacher_id) != 7:
                messagebox.showerror("Error", "teacher ID must be a 7-digit number.")
                return False
            elif entered_captcha != captcha.get():
                messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
                generate_captcha()
                return False
            else:
                # Registration successful
                messagebox.showinfo("Login Successful", "teacher Login successfully!")
                return True
        
        # Create a frame to contain all the elements
        login_frame = tk.Frame(login_root, borderwidth=2, relief="solid")
        login_frame.pack(pady=50)  # Add padding to center the frame vertically
    
        # Configure the columns and rows to expand and fill any extra space
        login_root.columnconfigure(0, weight=1)
        login_root.rowconfigure(0, weight=1)
    
        # Add your login window components to the frame
        # Create labels and entry widgets
        teacher_login = tk.Label(login_frame, text="teacher Login", font=("Times", 16))
        teacher_login.grid(row=0, column=1, padx=10, pady=10)
    
        teacher_name_label_login = tk.Label(login_frame, text="teacher Name:", font=common_font)
        teacher_name_label_login.grid(row=1, column=0, padx=10, pady=10)
        teacher_name_entry_login = ttk.Entry(login_frame, font=common_font)
        teacher_name_entry_login.grid(row=1, column=1, padx=10, pady=10)
    
        teacher_id_label_login = tk.Label(login_frame, text="teacher ID (7 digits):", font=common_font)
        teacher_id_label_login.grid(row=2, column=0, padx=10, pady=10)
        teacher_id_entry_login = ttk.Entry(login_frame)
        teacher_id_entry_login.grid(row=2, column=1, padx=10, pady=10)
    
        password_label_login = tk.Label(login_frame, text="Password:", font=common_font)
        password_label_login.grid(row=3, column=0, padx=10, pady=10)
        password_entry_login = ttk.Entry(login_frame, show="*")  # Mask the password
        password_entry_login.grid(row=3, column=1, padx=10, pady=10)
    
        # Generate and display CAPTCHA text
        captcha_label = Label(login_frame, text="", font=("Times", 17), bg='mintcream', fg='red')
        captcha_label.grid(row=5, column=0, padx=1, pady=1)
    
        # Label and Entry for user input
        captcha_label_entry = Label(login_frame, text="CAPTCHA:")
        captcha_label_entry.grid(row=4, column=0, padx=10, pady=10)
        captcha_entry = Entry(login_frame, font=("Times", "16"), width=10, fg='gray1')
        captcha_entry.grid(row=4, column=1, padx=10, pady=5)

        # Bind the "Enter" key for teacher_name_entry_login
        teacher_name_entry_login.bind("<Return>", lambda event, entry=teacher_id_entry: focus_next_entry(event, teacher_name_entry_login, entry))
        
        # Bind the "Enter" key for teacher_id_entry_login
        teacher_id_entry.bind("<Return>", lambda event, entry=password_entry: focus_next_entry(event, teacher_id_entry, entry))
        
        # Bind the "Enter" key for password_entry
        password_entry.bind("<Return>", lambda event, entry=captcha_entry: focus_next_entry(event, password_entry, entry))
        
        # Bind the "Enter" key for captcha_entry
        captcha_entry.bind("<Return>", )  # Assuming you want to submit the form on pressing Enter in the captcha_entry
        
        
        # Center the frame in the window
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
                
        # Function to generate a random CAPTCHA text
        def generate_captcha():
            characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            global captcha
            captcha = "".join(random.choice(characters) for _ in range(6))
            captcha_label.config(text=captcha)
    
        # Generate captcha button
        generate_captcha_button = Button(login_frame, text="Generate CAPTCHA", command=generate_captcha)
        generate_captcha_button.grid(row=5, column=1, padx=10, pady=10)
    
        # Create a back button that brings back to registration
        back_button_login = tk.Button(login_frame, text="Back", bg='red',fg='black',font=common_font, command=login_root.destroy)
        back_button_login.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    
        def vadidate_and_open_teacher():
            # Call course_validation to check if all fields are filled
            login_successful = join_class()
    
        # If validation is successful, open the teacher interface
            if login_successful:
                login_root.destroy()
                open_teacher_interface()
    
        # Rest of your registration window components
        join_class_button = tk.Button(login_frame, text="Join Class", bg='green',fg='black',font=common_font, command = open)
        join_class_button.grid(row=6, column=1, padx=10, pady=10 )
    
    # Start the Tkinter main loop
    root.mainloop()