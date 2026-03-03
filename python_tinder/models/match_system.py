class MatchSystem:
    def __init__(self):
        self.all_users = []
        self.matches = []

    def add_user(self, user):
        self.all_users.append(user)

    def find_matches(self, user):
        potential_matches = []
        for other_user in self.all_users:
            if other_user != user:
                for pet in other_user.pets:
                    potential_matches.append(pet)
        return potential_matches

    def create_match(self, user1, user2):
        self.matches.append((user1, user2))
        user1.match_with(user2)
