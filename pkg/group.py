class Group:
    def __init__(self, name, members, vehicle, csvfile):
        self.__name = name
        self.__members = members
        self.__vehicle = vehicle
        self.__csvfile = csvfile

    def __str__(self):
        return self.__name + "\nmembri:" + " ".join(self.__members) \
               + "\nveicolo utilizzato: " + self.__vehicle

    def get_name(self):
        return self.__name

    def get_members(self) -> list:
        return self.__members

    def get_vehicle(self):
        return self.__vehicle

    def get_csvFile(self):
        return self.__csvfile
