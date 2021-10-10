class Section:
    def __init__(self, section_name: str):
        self.hits_counter = 0
        self.section_name = section_name

    def __hash__(self):
        return hash(self.section_name)

    def get_hits_count(self):
        return self.hits_counter

    def increase_hits_count(self, value):
        self.hits_counter += value

    def cleanup(self):
        self.hits_counter = 0
