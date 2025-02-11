def assemble_c_instruction(data):
    # dest = comp;jump
    # first check if there's a dest
    line = data.split('=')
    if len(line) == 2:
        # we have destination
        dest = line[0]
        line = line[1]
        # print(dest)
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
        print(line)
    else:
        print('no dest')

    # next look at jump
    temp = line.split(';')
    # print(temp)
    if len(temp) == 2:
        print('we have jump')
        jump = temp[1]
        line = temp[0]
        print(jump)
        print(line)
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
    else:
        print('no jump')
        print(line)

assemble_c_instruction('M=comp;jump')
# assemble_c_instruction('M=comp')
# assemble_c_instruction('comp;jump')