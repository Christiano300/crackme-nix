from collections import deque

class State:
    def __init__(self, flag: list[int]):
        self.instr_pointer = 0
        self.flag = flag
        self.stack = deque()
        self.mem: dict[str, int] = {}
        self.switch_dict = {
            "swapStack": self.swap_stack,
            "exit": self.exit,
            "pop": self.pop,
            "push": self.push,
            "inc": self.inc,
            "dec": self.dec,
            "clearStackToMem": self.clear_stack_to_mem,
            "clearMemToStack": self.clear_mem_to_stack,
            "pushFlagAtA0": self.push_flag,
            "jumpToA0": self.jump,
            "printBuf": self.print_buf,
            "nonNoop": self.noop,
            "_bitAnd": lambda: self.instr(lambda x, y: x & y, "&"),
            "_bitXor": lambda: self.instr(lambda x, y: x ^ y, "^"),
            "_sub": lambda: self.instr(lambda x, y: x - y, "-"),
            "_add": lambda: self.instr(lambda x, y: x + y, "+"),
            "_mul2Pow": lambda: self.instr(lambda x, y: x * 2**y, "<<"),
            "_div2Pow": lambda: self.instr(self.div2_pow, ">>"),
        }

    def div2_pow(self, x, y):
        if x > -1:
            return x // 2**y
        return ~((~x) // 2**y)

    def instr(self, func, repr):
        x = self.stack.popleft()
        y = self.stack.popleft()
        x_v = self.mem.get(str(x), 0)
        y_v = self.mem.get(str(y), 0)
        res = func(x_v, y_v)
        print(f"{self.instr_pointer:<6d}: mem[{x}] = {x_v:10d} {repr:2s} {y_v:10d} ({res})")
        self.mem[str(x)] = res
        self.instr_pointer += 1

    def swap_stack(self):
        self.instr_pointer += 1
        first = self.stack.popleft()
        second = self.stack.popleft()
        self.stack.appendleft(first)
        self.stack.appendleft(second)

    def exit(self):
        self.instr_pointer = -1

    def push(self):
        self.instr_pointer += 1
        self.stack.appendleft(self.mem.get("0", 0))

    def pop(self):
        self.instr_pointer += 1
        self.mem["0"] = self.stack.popleft()

    def inc(self):
        self.instr_pointer += 1
        self.mem["0"] = self.mem.get("0", 0) + 1

    def dec(self):
        self.instr_pointer += 1
        self.mem["0"] = self.mem.get("0", 0) - 1

    def clear_stack_to_mem(self):
        self.instr_pointer += 1
        self.mem = { str(idx): elem for idx, elem in enumerate(self.stack) }
        self.stack = deque()

    def clear_mem_to_stack(self):
        self.instr_pointer += 1
        self.stack = deque(self.mem[str(i)] for i in range(len(self.mem)))
        self.mem = {}

    def push_flag(self):
        self.instr_pointer += 1
        a0 = self.mem.get("0", 0)
        if a0 < len(self.flag):
            self.stack.appendleft(self.flag[a0])
        else:
            self.stack.appendleft(-1)
        print(f"Pushing flag at {a0} at line {self.instr_pointer - 1}, stack is now {list(self.stack)}")

    def jump(self):
        before = self.instr_pointer
        if self.instr_pointer == 52616:
            self.instr_pointer = 52617
        else:
            self.instr_pointer += self.mem.get("0", 0)
        print("Jumping to", self.instr_pointer, "from", before, list(self.stack), self.mem)

    def print_buf(self):
        self.instr_pointer += 1
        print("".join(chr(i) for i in self.stack))
        self.stack = deque()

    def noop(self):
        self.instr_pointer += 1

    def execute(self, instr):
        func = self.switch_dict.get(instr)
        if func is None:
            raise ValueError(f"Instruction {instr} not found")
        func()


def main():
    state = State([ord(c) for c in "halloooo"])
    with open("instrs.txt") as f:
        instrs = [line.strip() for line in f.readlines()]
        while state.instr_pointer >= 0:
            instr = instrs[state.instr_pointer]
            state.execute(instr)
        print("done")


if __name__ == "__main__":
    main()
