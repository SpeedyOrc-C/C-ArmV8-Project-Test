from os import listdir, system, mkdir

# Get all the assembly files

try:
    mkdir('./solution')
except FileExistsError:
    pass

try:
    mkdir('./test/output')
except FileExistsError:
    pass

assemblies = {}
for category in listdir('./test/assembly'):
    assemblies[category] = listdir(f'./test/assembly/{category}')
    try:
        mkdir(f'./test/output/{category}')
    except FileExistsError:
        pass

ASSEMBLER_PATH = './solution/assemble'
EMULATOR_PATH = './solution/emulate'


# Run the assembler and emulator on all the assembly files

def fill_trailing_spaces(string, length):
    return string + ' ' * (length - len(string))


wrong_emulator = []
wrong_assembler = []
test_case_num = 0

for category in assemblies:
    test_case_num += len(assemblies[category])
    for assembly in assemblies[category]:

        assembly = assembly.split('.')[0]
        print(fill_trailing_spaces(f'{category}/{assembly}', 20), end='')

        error_found = False

        if system(
                f'{ASSEMBLER_PATH} ./test/assembly/{category}/{assembly}.s ./test/output/{category}/{assembly}.bin'):
            print('!', end='')
            error_found = True
        else:
            with open(f'./test/answer/{category}/{assembly}_exp.bin', 'rb') as f:
                expected_assembled = f.read()
            with open(f'./test/output/{category}/{assembly}.bin', 'rb') as f:
                actual_assembled = f.read()
            if expected_assembled != actual_assembled:
                print('X', end='')
                error_found = True
                wrong_assembler.append(f'{category}/{assembly}')
            else:
                print('O', end='')

        if system(
                f'{EMULATOR_PATH} ./test/answer/{category}/{assembly}_exp.bin ./test/output/{category}/{assembly}.out'):
            print('! ', end='')
            error_found = True
        else:
            with open(f'./test/answer/{category}/{assembly}_exp.out', 'r') as f:
                expected_cpu_state = f.read()
            with open(f'./test/output/{category}/{assembly}.out', 'r') as f:
                actual_cpu_state = f.read()
            if actual_cpu_state != expected_cpu_state:
                print('X', end='')
                error_found = True
                wrong_emulator.append(f'{category}/{assembly}')
            else:
                print('O', end='')
        if error_found:
            print('<<<<<<<<<<')
        else:
            print()

print()
if wrong_emulator:
    print(f'Wrong emulator test cases ({len(wrong_emulator)})')
    for x in wrong_emulator:
        print('\t' + x)
else:
    print('Emulator clear!')

print()
if wrong_assembler:
    print(f'Wrong assembler test cases ({len(wrong_assembler)})')
    for x in wrong_assembler:
        print('\t' + x)
else:
    print('Assembler clear!')
