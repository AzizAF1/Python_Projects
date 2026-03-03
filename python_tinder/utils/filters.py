def filter_pets(pets, breed=None, age_range=None, awards=None):
    """
    Filter pets : breed, age range,  awarded competitions
    """
    filtered_pets = pets
    if breed:
        filtered_pets = [pet for pet in filtered_pets if pet.breed.lower() == breed.lower()]
    if age_range:
        filtered_pets = [pet for pet in filtered_pets if age_range[0] <= pet.age <= age_range[1]]
    if awards:
        filtered_pets = [pet for pet in filtered_pets if any(award in pet.awards for award in awards)]
    return filtered_pets
