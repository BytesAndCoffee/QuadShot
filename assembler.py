def tokenize(file):
    for line in file:
        line = line.split()
        op, args = line[0], line[1].split(',')
        yield op, args

def parse(lines):
    table = {'DIRECT':
                      {
                      'ADD': 'A0',
                      'SUB': 'A1',
                      'MUL': 'A2',
                      'DIV': 'A3',
                      'MOD': 'A6',
                      'INC': 'A4',
                      'DEC': 'A5',

                      },
             'IMMEDIATE':
                      {
                      'ADD': 'B0',
                      'SUB': 'B1',
                      'MUL': 'B2',
                      'DIV': 'B3',
                      'MOD': 'B6',
                      }
              'JMP': 'C0',
              'JZ':  'C1',
              'JNZ': 'C2',
              'JS':  'C3',
              'JNS': 'C4',
              'JO':  'C5',
              'JNO': 'C6',
              'MOV': 'D0',
              'CMP': 'DA',
              'PUSH':'E0',
              'POP': 'E1'
            }

    for line in lines:
