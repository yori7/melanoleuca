class MyIterator:
    def __init__(self, ls):
        self.ls = ls
        self.now = 0

    def next(self, i=1):
        self.now += i
        if self.now >= len(self.ls):
            self.now -= len(self.ls)
        return self.ls[self.now]

    def prev(self, i=1):
        self. now -= i
        if self.now < 0:
            self.now += len(self.ls)
        return self.ls[self.now]

    def get(self, num):
        return self.ls[num]

    def get_now(self):
        print(self.ls[self.now])
        return self.ls[self.now]

    def add(self, element):
        self.ls.append(element)
