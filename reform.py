# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 14:27:48 2014

@author: YAZDMICH230
"""
from pprint import pprint
jumps = {'JMP': 'C0',
         'JZ': 'C1',
         'JNZ': 'C2',
         'JS': 'C3',
         'JNS': 'C4',
         'JO': 'C5',
         'JNO': 'C6'
         }
arithmetic = {
    'ADD': ['A0', 'B0'],
    'SUB': ['A1', 'B1'],
    'MUL': ['A2', 'B2'],
    'DIV': ['A3', 'B3'],
    'MOD': ['A6', 'B6']
}
table = {
    'INC': 'A4',
    'DEC': 'A5',
    'MOV': ['D0', 'D1', 'D2', 'D3', 'D4'],
    'CMP': ['DC', 'DA', 'DB'],
    'PUSH': 'E0',
    'POP': 'E1'
}
registers = {'AL': '00', 'BL': '01', 'CL': '02', 'DL': '03'}
a = {}
for key, values in arithmetic.items():
    for value in values:
        a[value] = {'op': key, 'len': 2}
for key, value in jumps.items():
    a[value] = {'op': key, 'len': 1}
for item in table['CMP']:
    a[item] = {'op': 'CMP', 'len': 2}
for item in table['MOV']:
    a[item] = {'op': 'MOV', 'len': 2}
a['A4'] = {'op': 'INC', 'len': 1}
a['A5'] = {'op': 'DEC', 'len': 1}
a['E0'] = {'op': 'PUSH', 'len': 1}
a['E1'] = {'op': 'POP', 'len': 1}
pprint(a)