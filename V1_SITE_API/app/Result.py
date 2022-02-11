class Result:
    def __init__(self, i, result, j=None,):
        self.start = i
        if j:
            self.finish=j
        else:
            self.finish = i + 250
        self.result = result
