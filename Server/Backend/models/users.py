from Server.Backend.models.model import Model

class User(Model):
    RegistrationDate = "RegistrationDate"
    Name = "Name"
    Login = "Login"
    Password = "Password"
    Email = "Email"

    def __init__(self,
                 RegistrationDate : str,
                 Name : str,
                 Login : str,
                 Password : str,
                 Email : str):
        self.RegistrationDate = RegistrationDate
        self.Name = Name
        self.Login = Login
        self.Password = Password
        self.Email = Email
