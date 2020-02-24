"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        """Currently the register and memory are stored here."""
        self.reg = [0] * 8
        self.ram = [0] * 256

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

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001


        program = [
            # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001 # HLT

            LDI,
            0,
            8,
            PRN,
            0,
            HLT
        ]

        for instruction in program:
            self.raw_write(instruction, address)
            address += 1



    def alu(self, op, reg_a, reg_b):
        """Partially implemented mathematical functions."""
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def HLT(self):
        print("Program successfully halted.")
        exit(0)

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        pc = 0
        for i in self.ram:
            if i == self.ram_read(pc):
                if i == LDI:
                    operand_a = self.ram_read(pc + 1)
                    operand_b = self.ram_read(pc + 2)
                    self.reg[operand_a] = operand_b
                    pc += 3
                elif i == PRN:
                    operand_a = self.ram_read(pc + 1)
                    data = self.reg[operand_a]
                    print(data)
                    pc += 2
                elif i == HLT:
                    print("Program successfully ran.")
                    exit(0)
                else:
                    print(f"ERROR: Unknown command in program at line {pc}.  Code: {i}")
                    exit(1)
            else:
                pass

