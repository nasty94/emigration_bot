class User:
    def __init__(self, id):
        self.id = id
        self.additional_info = None
        self.age = None
        self.gender = None
        self.profession = None
        self.country = None
        self.current_question=None
        self.previous_question = None
        self.children = False

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.id != other.id:
            return False
        return True

    def __hash__(self):
        return self.id