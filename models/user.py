class User:
    def __init__(self, user_id, name, email, is_admin=False):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.name} ({'Admin' if self.is_admin else 'User'})"
