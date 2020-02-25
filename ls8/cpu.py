"""CPU functionality."""

import sys

LDI = 1
PRN = 2
HLT = 3
MUL = 4

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        """Contains Registry, RAM, Program Counter and branchtable."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[HLT] = self.handle_HLT

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

        address = 0

        # For now, we've just hardcoded a program:

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
                    self.raw_write(1, address)
                elif splitstring[0] == "PRN":
                    self.raw_write(2, address)
                elif splitstring[0] == "HLT":
                    self.raw_write(3, address)
                elif splitstring[0] == "MUL":
                    self.raw_write(4, address)
                else:
                    binary_mode = int(instruction, 2)
                    self.raw_write(binary_mode, address)
                address += 1
        self.raw_write(3, address)



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

    def run(self):
        """Run the CPU."""


        for i in self.ram:
            if i == self.ram_read(self.pc):
                if self.branchtable[i]:
                    self.branchtable[i]()
                else:
                    print(f"ERROR: Unknown command in program at line {pc}.  Code: {i}")
                    exit(1)
            else:
                pass

