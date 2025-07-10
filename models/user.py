class User:
    def __init__(self, user_id, name, email, is_admin=False, password=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.is_admin = is_admin
        self.password = password  # Add this line

    def __str__(self):
        return f"{self.name} ({'Admin' if self.is_admin else 'User'})"
