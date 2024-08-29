
class StringReader:
    def __init__(self,string:str) -> None:
        self.string = string
        self.pointer = 0
    
    def read(self,ammount:int) -> str | None:
        if self.pointer+ammount >= len(self.string):
            return
        else:
            ret = self.string[self.pointer:self.pointer+ammount]
            self.pointer += ammount
            return ret
    
    def peek(self,ammount:int) -> str | None:
        if self.pointer+ammount > len(self.string):
            return
        else:
            return self.string[self.pointer:self.pointer+ammount]
    
    def skip(self,ammount:int) -> None:
        self.pointer += ammount
    
    def backtrack(self,ammount:int) -> None:
        self.pointer -= ammount

