class PetProfile:
    def __init__(self, name, breed, age, description, images=None):
        self.name = name
        self.breed = breed
        self.age = age
        self.description = description
        self.images = images if images else []
        self.family_history = []
        self.awards = []

    def add_family_member(self, relation, name, breed):
        self.family_history.append({"relation": relation, "name": name, "breed": breed})

    def add_award(self, award):
        self.awards.append(award)

    def get_summary(self):
        return {
            "Name": self.name,
            "Breed": self.breed,
            "Age": self.age,
            "Description": self.description
        }

    def get_family_tree(self):
        return self.family_history
