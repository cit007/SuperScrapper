class Config:
    def __init__(self, max=5):
        self.__max = max

    @property
    def max(self):
        return self.__max

    @max.setter
    def max(self, max):
        self.__max = max


config = Config(max=5)
