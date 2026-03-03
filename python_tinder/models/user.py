class User:
    """
    Represent user : username, pets, matches.
    """
    def __init__(self, username):
        self.username = username
        self.pets = []
        self.matches = []

    def add_pet(self, pet_profile):
        self.pets.append(pet_profile)

    def swipe_right(self, pet_profile):
        # In a real system, this would trigger some logic for matching
        print(f"{self.username} liked {pet_profile.name}")

    def swipe_left(self, pet_profile):
        print(f"{self.username} skipped {pet_profile.name}")

    def match_with(self, user):
        # Ensure mutual matching
        if user not in self.matches:
            self.matches.append(user)
        if self not in user.matches:
            user.matches.append(self)
        print(f"Match created between {self.username} and {user.username}")
