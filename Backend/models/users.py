

class User:
    UserProfileId : int
    RegistrationDate : str
    Name : str
    Login : str
    Password : str
    Email : str

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

    def toTuple(self):
        return (
            self.UserProfileId,
            self.RegistrationDate,
            self.Name,
            self.Login,
            self.Password,
            self.Email
        )

    def toNamesFixture(self):
        return "{},{},{},{},{},{}".format(
            "UserProfileId",
            "RegistrationDate",
            "Name",
            "Login",
            "Password",
            "Email",
        )



