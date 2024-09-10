class DHT22:
    def __init__(self, pin): ...

    def measure(self): ...

    def temperature(self):
        return 25.3

    def humidity(self):
        return 46.2


DHT11 = DHT22
