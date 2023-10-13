from firebase_admin import auth
from ExpenseManager import ExpenseManager
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel, CTkFrame
from tkinter import messagebox
from Account import account_creation
import smtplib
from cryptography.fernet import Fernet
class account_window():
    def __init__(self):
    # Create the main window
        self.window = CTk()
        self.window.configure(fg_color="white")
        self.window.title("Login")
        self.button_canvas = CTkFrame(self.window, fg_color="white")
        self.entry_canvas = CTkFrame(self.window, fg_color="white")
        self.entry_canvas.pack()
        self.button_canvas.pack(pady=(15, 0))
        self.account = account_creation()
        # Create username label and entry
        username_label = CTkLabel(self.entry_canvas, text="Email:", text_color="black")
        username_label.grid(column=1, row=0, pady=(15,0))
        self.username_entry = CTkEntry(self.entry_canvas)
        self.username_entry.grid(column=1, row=1, padx=85)

        # Create password label and entry
        password_label = CTkLabel(self.entry_canvas, text="Password:", text_color="black")
        password_label.grid(column=1, row=2)
        self.password_entry = CTkEntry(self.entry_canvas, show="*")
        self.password_entry.grid(column=1, row=3)

        # Create login button
        login_button = CTkButton(self.button_canvas, text="Login", command=self.login)
        login_button.grid(column=0, row=0, pady=(0, 15), padx=5)

        create_account_button = CTkButton(self.button_canvas, text="Create Account", command=self.create_account)
        create_account_button.grid(column=1, row=0, pady=(0, 15), padx=5)

        forgot_password_button = CTkButton(self.button_canvas, text="Forgot Password", command=self.forgot_password)
        forgot_password_button.grid(column=2, row=0, pady=(0, 15), padx=5)

        self.initialize_firebase()
        # Run the main loop
        self.window.mainloop()

    def login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()
        try:
            with open(f"{email}.txt", "rb") as file:
                encrypted_password = file.readline()
            with open(f"{email}_Data.txt", "rb") as file:
                key = file.readline()
                print(encrypted_password)
                fernet = Fernet(key)
                # Decrypt the encrypted password
                decrypted_data = fernet.decrypt(encrypted_password).decode()
                print(decrypted_data)
                print(password)
                # Compare the entered password with the decrypted password
                if password == decrypted_data:
                    print("Login successful!")
                    self.window.destroy()
                    expense = ExpenseManager()
                    # Perform further actions here after successful login
                else:
                    self.error_length = CTkLabel(self.button_canvas, text="Password incorrect", text_color="black")
                    self.error_length.grid(column=0, row=1, columnspan=3)
        except(FileNotFoundError):
            try:
                self.error_length.destroy()
            finally:
                self.error_length = CTkLabel(self.button_canvas, text="The account associated with this\nemail does not exist", text_color="black", justify="center")
                self.error_length.grid(column=0, row=1, columnspan=3)


    def create_account(self):
        if len(self.username_entry.get()) < 5 or len(self.password_entry.get()) < 5:
            try:
                self.error_length.destroy()
            finally:
                self.error_length = CTkLabel(self.button_canvas, text="Account Email or Password not long enough", text_color="black")
                self.error_length.grid(column=0, row=1, columnspan=3)
        else:
            username = self.username_entry.get()
            password = self.password_entry.get()
            key = Fernet.generate_key()
            print(key)
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode())
            print(encrypted_password)
            with open(f"{username}.txt", "wb") as file:
                file.write(encrypted_password)
            with open(f"{username}_Data.txt", "wb") as file:
                file.write(key)
            self.account.create_firebase_account(username, password)
            try:
                self.error_length.destroy()
            finally:
                self.error_length = CTkLabel(self.button_canvas, text="Account successfully created", text_color="black")
                self.error_length.grid(column=0, row=1, columnspan=3)


    def initialize_firebase(self):
        pass

    def forgot_password(self):
        email = self.username_entry.get()
        try:
            # Send password reset email using Firebase Auth
            link = auth.generate_password_reset_link(email)

            # Show a message indicating that a password reset email has been sent
            messagebox.showinfo("Forgot Password", "A password reset email has been sent to your email address.")
            self.send_custom_email(email, link)
        except auth.UserNotFoundError:
            # Handle the case when the provided email does not exist in the Firebase Auth user database
            messagebox.showerror("Forgot Password", "The provided email does not exist in our records.")
        except Exception as e:
            # Handle other possible errors during the password reset process
            messagebox.showerror("Forgot Password", f"An error occurred: {str(e)}")

    def send_custom_email(self, recipient, reset_link):


        # Gmail account credentials
        sender_email = 'ENTER_SENDER_EMAIL_HERE'
        sender_password = "EMAIL_PASSWORD_HERE"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=sender_password)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=recipient,
                                msg=f"Subject:Password Reset Link\n\nClick the link below to reset your password:\n\n{reset_link}")
            print("Password reset email sent successfully.")

