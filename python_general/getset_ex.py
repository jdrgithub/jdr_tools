class Person:
    def __init__(self, name):
        self._name = name  # the underscore means "internal use"

    @property
    def name(self):
        print("Getting name...")
        return self._name

    @name.setter
    def name(self, value):
        print("Setting name...")
        self._name = value

# Usage
p = Person("Alice")
print(p.name)     # Triggers the getter
p.name = "Bob"    # Triggers the setter
print(p.name)     # Triggers the getter again
