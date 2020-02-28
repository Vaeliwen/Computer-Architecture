"""CPU functionality."""

import sys

LDI = 1
PRN = 2
HLT = 3
MUL = 4
PUSH = 5
POP = 6
CMP = 7
JMP = 8
JEQ = 9
JNE = 10

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        """Contains Registry, RAM, Program Counter, and branchtable."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0b00000000] * 256
        self.fl = [0] * 3
        self.e = self.fl[0]
        self.l = self.fl[1]
        self.g = self.fl[2]
        self.program = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE
        """Stack Pointer."""
        self.reg[-1] = 242


    def ram_read(self, mar):
        "Reads the selected address within the RAM."
        value = self.ram[mar]
        return value

    def raw_write(self, mdr, mar):
        """Takes in data and an address to write the data to."""
        self.ram[mar] = mdr
        return

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) == 1:
            print("ERROR: No program loaded.  Please specify program directory.")
            exit(1)
        else:
            program = open(sys.argv[1])

        for instruction in program:
            splitstring = instruction.split()
            if splitstring == []:
                pass
            elif splitstring[0] == "#":
                pass
            elif splitstring[0] == "LDI": 
                self.raw_write(LDI, self.program)
                self.program += 1
            elif splitstring[0] == "PRN":
                self.raw_write(PRN, self.program)
                self.program += 1
            elif splitstring[0] == "HLT":
                self.raw_write(HLT, self.program)
                self.program += 1
            elif splitstring[0] == "MUL":
                self.raw_write(MUL, self.program)
                self.program += 1
            elif splitstring[0] == "PUSH":
                self.raw_write(PUSH, self.program)
                self.program += 1
            elif splitstring[0] == "POP":
                self.raw_write(POP, self.program)
                self.program += 1
            elif splitstring[0] == "CMP":
                self.raw_write(CMP, self.program)
                self.program += 1
            elif splitstring[0] == "JMP":
                self.raw_write(JMP, self.program)
                self.program += 1
            elif splitstring[0] == "JEQ":
                self.raw_write(JEQ, self.program)
                self.program += 1
            elif splitstring[0] == "JNE":
                self.raw_write(JNE, self.program)
                self.program += 1

            else:
                binary_mode = int(instruction, 2)
                self.raw_write(binary_mode, self.program)
                self.program += 1

        self.raw_write(HLT, self.program)



    def alu(self, op, reg_a, reg_b):
        """Partially implemented mathematical functions."""
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_HLT(self):
        print("Program successfully halted.")
        exit(0)

    def handle_LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3
    
    def handle_PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        data = self.reg[operand_a]
        print(data)
        self.pc += 2
    
    def handle_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def handle_PUSH(self):
        operand_a = self.ram_read(self.pc + 1)
        data = self.reg[operand_a]
        self.raw_write(data, self.reg[-1])
        if self.reg[-1] <= self.program:
            print(f"ERROR: Stack Overflow at line {self.pc}.")
        self.reg[-1] -= 1
        self.pc += 2

    def handle_POP(self):
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.ram_read(self.reg[-1])
        if self.reg[-1] >= 242:
            print(f"ERROR: Stack Underflow at line {self.pc}.")
            exit(1)
        self.reg[-1] += 1
        self.pc += 2
    def handle_CMP(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        if self.reg[operand_a] == self.reg[operand_b]:
            self.e = 1
            self.l = 0
            self.g = 0
        elif self.reg[operand_a] > self.reg[operand_b]:
            self.e = 0
            self.l = 0
            self.g = 1
        elif self.reg[operand_a] < self.reg[operand_b]:
            self.e = 0
            self.l = 1
            self.g = 0
        self.pc += 3
    def handle_JMP(self):
        operand_a = self.ram_read(self.pc + 1)
        self.pc = self.reg[operand_a]
    def handle_JEQ(self):
        if self.e == 1:
            operand_a = self.ram_read(self.pc + 1)
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2
    def handle_JNE(self):
        if self.e == 0:
            operand_a = self.ram_read(self.pc + 1)
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2


    def run(self):
        """Run the CPU."""


        for i in self.ram:
            if i == self.ram_read(self.pc):
                if self.branchtable[i]:
                    self.branchtable[i]()
                else:
                    print(f"ERROR: Unknown command in program at line {self.pc}.  RAM dump: {i}")
                    exit(1)
            else:
                pass

