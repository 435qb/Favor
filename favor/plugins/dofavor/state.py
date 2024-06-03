class item:
    index : int = 1
    group : str

    def __init__(self, group_ : str, index_ : int = 1) -> None:
        self.group = group_
        self.index = index_

    def curr(self) -> str:
        return self.group[self.index]

    def end(self):
        return self.index == len(self.group) - 1
    
    def incr(self):
        self.index += 1

    def __str__(self) -> str:
        return f"{self.curr()} {self.group}"

class state:
    data : list[item] = []
    filename : str

    def new_group(self, newgroup : str) -> bool:
        if self.contains(newgroup) != None:
            return False
        self.data.append(item(newgroup))
        return True

    def next_group(self, curr : str, newgroup : str) -> bool:
        item = self.contains(newgroup)
        if item == None or curr != item.curr():
            return False
        if not item.end():
            item.incr()
            return True
        # remove
        self.data.remove(item)
        return True
        
    def contains(self, newgroup : str) -> item | None:
        for d in self.data:
            if sorted(d.group) == sorted(newgroup):
                return d
            
    def __str__(self) -> str:
        s = ""
        for d in self.data:
            s += f"{d}\n"
        return s
    
    def save(self):
        with open(self.filename, "w") as f:
            for d in self.data:
                f.write(f"{d.index} {d.group}\n")

    def load(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    others = line.split()
                    if len(others) != 2:
                        print("严重错误")
                        exit(1)
                    state.data.append(item(others[1], int(others[0])))
        except OSError:
            pass