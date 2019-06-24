class Vehicle:
    occupied_space = 0

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.packages = [] # Paquetes asignados al vehículo