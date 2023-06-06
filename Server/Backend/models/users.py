from models.model import Model

class User(Model):
    UserProfileId = "UserProfileId"
    RegistrationDate = "RegistrationDate"
    Name = "Name"
    Login = "Login"
    Password = "Password"
    Email = "Email"

    def __init__(self,
                 UserProfileId : int,
                 RegistrationDate : str,
                 Name : str,
                 Login : str,
                 Password : str,
                 Email : str):
        self.UserProfileId = UserProfileId
        self.RegistrationDate = RegistrationDate
        self.Name = Name
        self.Login = Login
        self.Password = Password
        self.Email = Email
