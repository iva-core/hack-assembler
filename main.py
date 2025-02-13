def assemble_c_instruction(data):
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
        print(dest_bin)
        # print(line)
    else:
        print('no dest')

    # next look at jump
    line = line.split(';')
    if len(line) == 2:
        # we have jump
        jump = line[1]
        line = line[0]
        print(jump)
        # print(line)
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
        print(jump_bin)
        print(f'Line left: {line}')
    else:
        print('no jump')
        print(f'Line left: {line}')

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
    print(comp_bin)

    # combine
    # c_instr = dest_bin + comp_bin + jump_bin
    
def assemble_a_instruction(data):
    # don't think about the exceptions rn
    # just do @number = number
    if data.startswith('@'):
        line = data.split('@')
        loc = line[1]
        if loc.isdigit():
            # annoying formatting stuff 
            instr = bin(int(loc))
            instr = instr[2:].zfill(15)
            instr = f'0b{instr}'
        print(instr)
    pass

# symbol table which we will add to in one of the parses
symbol_table  = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 
                 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
                 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}


line_count = 0

example = 'M=D|M;JMP#@5#@20#0;JMP#//hello' # split by # for now

my_list = example.split('#')
# print(my_list)

for x in my_list:
    if x.startswith('//'):
        continue # comments aren't included in line count
    else:
        line_count += 1
print(line_count)

#assemble_c_instruction('M=D|M;JMP')
# assemble_c_instruction('M=comp')
# assemble_c_instruction('comp;jump')
# assemble_a_instruction('@5')