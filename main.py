def assemble_c_instruction(data: str) -> int: # takes in string and returns int
    # dest = comp;jump
    # first check if there's a dest
    line = data.split('=')
    if len(line) == 2:
        # we have destination
        dest = line[0]
        line = line[1]
        match dest:
            case 'M':
                dest_bin = 0b001
            case 'D':
                dest_bin = 0b010
            case 'MD':
                dest_bin = 0b011
            case 'A':
                dest_bin = 0b100
            case 'AM':
                dest_bin = 0b101
            case 'AD':
                dest_bin = 0b110
            case 'AMD':
                dest_bin = 0b111
            case _:
                raise Exception(f'{dest} is not a valid destination. ')
        dest_bin <<= 3 # bit shift left 3
    else:
        line = line[0]
        dest_bin = 0

    # next look at jump
    # print(line)
    line = line.split(';')
    if len(line) == 2:
        # we have jump
        jump = line[1]
        line = line[0]
        match jump:
            case 'JGT':
                jump_bin = 0b001
            case 'JEQ':
                jump_bin = 0b010
            case 'JGE':
                jump_bin = 0b011
            case 'JLT':
                jump_bin = 0b100
            case 'JNE':
                jump_bin = 0b101
            case 'JLE':
                jump_bin = 0b110
            case 'JMP':
                jump_bin = 0b111
            case _:
                raise Exception(f'{jump} is not a valid jump. ')
    else:
        line = line[0]
        jump_bin = 0

    # now look at computation
    match line:
        case '0':
            comp_bin = 0b0101010
        case '1':
            comp_bin = 0b0111111
        case '-1':
            comp_bin = 0b0111010
        case 'D':
            comp_bin = 0b0001100
        case 'A':
            comp_bin = 0b0110000
        case '!D':
            comp_bin = 0b0001101
        case '!A':
            comp_bin = 0b0110001
        case 'D+1':
            comp_bin = 0b0011111
        case 'A+1':
            comp_bin = 0b0110111
        case 'D-1':
            comp_bin = 0b0001110
        case 'A-1':
            comp_bin = 0b0110010
        case 'D+A':
            comp_bin = 0b0000010
        case 'D-A':
            comp_bin = 0b0010011
        case 'A-D':
            comp_bin = 0b0000111
        case 'D&A':
            comp_bin = 0b0000000
        case 'D|A':
            comp_bin = 0b0010101
        case 'M':
            comp_bin = 0b1110000
        case '!M':
            comp_bin = 0b1110001
        case '-M':
            comp_bin = 0b1110011
        case 'M+1':
            comp_bin = 0b1110111
        case 'M-1':
            comp_bin = 0b1110010
        case 'D+M':
            comp_bin = 0b1000010
        case 'D-M':
            comp_bin = 0b1010011
        case 'M-D':
            comp_bin = 0b1000111
        case 'D&M':
            comp_bin = 0b1000000
        case 'D|M':
            comp_bin = 0b1010101 
        case _:
            raise Exception(f'{line} is not a valid computation. ')
    comp_bin <<= 6 # bit shift left 6

    # combine
    instr = 0b000000000000000
    instr |= jump_bin
    instr |= dest_bin
    instr |= comp_bin
    instr |= 0b111_0000000_000_000
    return instr
    

def assemble_a_instruction(data: str) -> int:
    line = data.split('@')
    loc = line[1]
    if loc.isdigit():
        if int(loc) > 2**15:
            raise Exception(f'{loc} is greater than 2^15')
        instr = int(loc)
    else:
        my_num = symbol_table[loc]
        instr = my_num
    return instr

# symbol table which we will add to in one of the parses
symbol_table  = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 
                 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
                 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}


line_count = 0

to_assemble = []
with open('test.asm', 'r') as my_file:
    to_assemble = [x.strip() for x in (my_file.readlines())]

print(to_assemble)

for x in to_assemble:
    if x.startswith('//'):
        continue # comments aren't included in line count
    else:
        if x.startswith('('):
            if x.endswith(')'):
                label = x[1:-1]
                if label in symbol_table:
                    raise Exception(f'{label} already exists in table')
                symbol_table[label] = line_count
                continue
    line_count += 1

for x in to_assemble:
    current_pos = 16
    if x.startswith('@'):
        if (x[1:] not in symbol_table) and (not x[1:].isdigit()):
            new_symbol = x[1:]
            symbol_table[new_symbol] = current_pos
            current_pos += 1

assembled: list[int] = [] # saying it's a list of ints

for x in to_assemble:
    if x.startswith('@'):
        assembled.append(assemble_a_instruction(x))
    elif x.startswith('(') or x.startswith('//'):
        continue
    else:
        assembled.append(assemble_c_instruction(x))

