
class StringReader:
    def __init__(self,string:str) -> None:
        self.string = string
        self.pointer = 0
    
    def read(self,amount:int) -> str | None:
        if self.pointer+amount >= len(self.string):
            return
        else:
            ret = self.string[self.pointer:self.pointer+amount]
            self.pointer += amount
            return ret
    
    def peek(self,amount:int) -> str | None:
        if self.pointer+amount > len(self.string):
            return
        else:
            return self.string[self.pointer:self.pointer+amount]
    
    def skip(self,amount:int) -> None:
        self.pointer += amount
    
    def backtrack(self,amount:int) -> None:
        self.pointer -= amount

