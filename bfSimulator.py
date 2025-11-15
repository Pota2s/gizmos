from collections import deque as stack
from time import sleep

class Simulator:
    """
    A simulator class to interpret the brainfuck esolang using python.
    Allows memory exposure via the show_memory() method. 
    """

    _memory : list[int] = [0]
    _current_address : int = 0
    _current_instruction : int = 0
    _code : str = ""
    _stack : stack[int] = stack()
    _step_by_step : bool = False
    _delay : float = 0
    _output : str = ""

    @property
    def operation(self) -> str:
        return self._code[self._current_instruction] 

    def run(self) -> str:
        self.parse()
        return self._output

    def __init__(self, code : str, step_by_step : bool = False, delay : float = 0.) -> None:
        self._memory = [0]
        self._current_address = 0
        self._code = code
        self._step_by_step = step_by_step
        self._delay = delay

    def open_loop(self) -> None:
        if self._memory[self._current_address] == 0:
            depth = 1
            while (depth > 0):
                self._current_instruction += 1
                match(self.operation):
                    case "[":
                        depth += 1
                    case "]":
                        depth -= 1
        else : self._stack.append(self._current_instruction)
        

    def close_loop(self):
        if self._memory[self._current_address] != 0:
            self._current_instruction = self._stack.pop() - 1
        else:
            self._stack.pop()

    def move_right(self):
        self._current_address += 1
        if len(self._memory) <= self._current_address:
            self._memory.append(0)

    def move_left(self):
        self._current_address -= 1
        if self._current_address < 0:
            raise IndexError("Index out of memory")

    def increment(self):
        self._memory[self._current_address] += 1
        self._memory[self._current_address] %= 256

    def decrement(self):
        self._memory[self._current_address] -= 1
        self._memory[self._current_address] %= 256

    def output(self):
        char = chr(self._memory[self._current_address])
        self._output += char

    def ask_input(self):
        self._memory[self._current_address] = ord(input("Input one character:")[:1] or '\0')

    def create_breakpoint(self):
        self.show_memory()
        print(self._output)
        input("Press Enter to Continue!")

    def parse(self):

        INSTRUCTIONS = {
            "[" : self.open_loop,
            "]" : self.close_loop,
            ">" : self.move_right,
            "<" : self.move_left,
            "+" : self.increment,
            "-" : self.decrement,
            "." : self.output,
            "," : self.ask_input,
            "^" : self.create_breakpoint
        }

        while self._current_instruction < len(self._code):
            if self.operation in INSTRUCTIONS:
                INSTRUCTIONS[self.operation]()
                if self._step_by_step or self._delay > 0 :
                    self.show_memory()
            
            self._current_instruction += 1

    def show_memory(self, columns = 16):
        print("=" * columns * 5)
        print(f"Instruction : {self._code[self._current_instruction]}")
        print(f"Stack : {list(self._stack)}")
        print(f"Memory:")
        for i in range(0,len(self._memory),columns):
            for j in range(columns):
                idx = i * columns + j
                try:
                    value = self._memory[idx]
                except IndexError:
                    break
                if idx == self._current_address:
                    print(f"\033[32m0x{value:0>2x}\033[0;0m",end=' ')
                    continue
                print(f"0x{value:02x}",end=' ')
            print()
        if (self._step_by_step):
            input()
        sleep(self._delay)

if __name__ == "__main__":
    ... 

    print(Simulator(input("Brainfuck Code:")).run())