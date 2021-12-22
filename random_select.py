import random


class Choice:
    def __init__(self, array: list):
        self.array = array

    # to exchange array elements
    def __swap(self, array: list, x: int, y: int) -> None:
        array[x], array[y] = array[y], array[x]

    # to knuth shuffle
    def shuffle(self) -> None:
        for s in range(len(self.array)):
            r = random.randint(0, s)
            self.__swap(self.array, s, r)

    # to calculate total teams per group
    def __teams_per_group(self, groupNr: int) -> int:
        return len(self.array) // groupNr

    # choose teams randomly for each group
    def choose_by_sample(self, groupNr: int) -> list:
        array = self.array.copy()
        groups = []

        for _ in range(groupNr):
            teams = random.sample(array, self.__teams_per_group(groupNr))
            groups.append(teams)
            # to delete the elements from array which is already taken
            for t in teams:
                for ar in range(len(array)):
                    if t == array[ar]:
                        del array[ar]
                        break
        return groups

    # choose from array single team and a assigned group from the array randomly
    def choose_by_team_group(self) -> int:
        tms = random.choice(self.array)

        return tms
