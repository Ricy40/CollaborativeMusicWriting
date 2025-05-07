

class Score:
    def __init__(self):
        self.parts = []
        self.metadata = {}

    def add_part(self, part):
        self.parts.append(part)

    def get_part_by_id(self, id):
        for part in self.parts:
            if part.id == id:
                return part
        return None

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def __str__(self):
        return "Score: " + str(self.metadata) + " " + str(self.parts)