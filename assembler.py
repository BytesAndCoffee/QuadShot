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
                      'MUL': 'B2'
                      }
            }

    for line in lines:
