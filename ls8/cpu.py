"""CPU functionality."""

import sys


# Machine code:

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # holds 256 bytes of memory
        self.reg = [0] * 8 # 8 general-purpose registers
        self.pc = 0 # the program counter



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
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


    # should accept the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]


    # should accept a value to write, and the address to write it to.
    def ram_write(self, address, value):
        self.ram[address] = value


    def run(self):
        """Run the CPU."""

        running = True

        # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them.
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        while running:
            # read the memory address that's stored in register `PC`, and store that result in `IR`
            ir = self.ram_read(self.pc)

            # exit the loop if a `HLT` instruction is encountered
            # Halt the CPU (and exit the emulator)
            if ir == HLT:
                print("HLT")
                running = False
                self.pc += 1
                sys.exit(1)

            
            # Set the value of a register to an integer
            elif ir == LDI:
                print("LDI")
                self.reg[operand_a] = operand_b
                self.pc += 3


            # Print numeric value stored in the given register
            # Print to the console the decimal integer value that is stored in the given register
            elif ir == PRN:
                print("PRN")
                print(self.reg[operand_a])
                self.pc += 2

            else:
                print(f"Unknown instruction: {ir}")
                sys.exit(1)
        
