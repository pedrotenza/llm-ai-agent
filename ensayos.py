class Car:
    def __init__(self, name):
        self.name = name          # 8 Leerzeichen (innerhalb __init__)

    def __repr__(self):
        return 'Car ({})'.format(self.name)   # 8 Leerzeichen (innerhalb __repr__)

vehicle = Car('VW Polo')
print(vehicle)   # Car (VW Polo)