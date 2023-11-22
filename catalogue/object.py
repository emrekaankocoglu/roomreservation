class Object:
    def __str__(self) -> str:
        return self.__class__.__name__ + ": " + str(self.__dict__)
    def __repr__(self) -> str:
        return self.__class__.__name__ + ": " + str(self.__dict__)
    