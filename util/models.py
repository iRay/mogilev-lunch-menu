class User:
    id = ""
    username = ""
    first_name = ""
    last_name = ""
    text = ""

    def __str__(self):
        return f"{self.id}, {self.username}, {self.first_name}, {self.last_name}, {self.text}"
