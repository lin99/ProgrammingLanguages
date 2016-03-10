# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 20:31:11 2016

@author: Lin
"""
import re
import sys

RESERVED_WORDS = ['funcion_principal', 'booleano','caracter','entero','real','cadena','fin_principal','leer','imprimir','si','si_no','entonces',
                  'fin_si','mientras','hacer','fin_mientras','para','fin_para','seleccionar','entre','caso','romper','defecto','fin_seleccionar',
                  'estructura','fin_estructura','funcion','fin_funcion','falso','verdadero','retornar']

RESERVED_WORDS = dict(zip(RESERVED_WORDS, RESERVED_WORDS))

DOUBLE_TOKENS = {'==': 'tk_igual', '!=': 'tk_dif', '&&': 'tk_y', '||': 'tk_o',
                 '<=': 'tk_menor_igual', '>=': 'tk_mayor_igual'}


SINGLE_TOKENS = {'+': 'tk_mas', '-': 'tk_menos', '*': 'tk_mult', '/': 'tk_div',
                 '%': 'tk_mod', '=': 'tk_asig', '!': 'tk_neg', ':': 'tk_dosp',
                 '<': 'tk_menor', '>': 'tk_mayor', '\'': 'tk_comilla_sen',
                 '"': 'tk_comilla_dob',';': 'tk_pyc', ',': 'tk_coma',
                 '(': 'tk_par_izq', ')': 'tk_par_der'}
                     
re_reserved = re.compile('|'.join(RESERVED_WORDS))
re_double = re.compile('>=|==|<=|\\|\\||&&|!=')
re_single = re.compile('!|%|\'|=|-|,|/|<|\\)|;|:|\\*|\\+|\\(|>')
re_id = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")
re_real = re.compile("[0-9]+\\.[0-9]+")
re_entero = re.compile("[0-9]+")
re_char = re.compile('\'.\'')
#re_strings = re.compile("\".*?\"")
#re_strings = re.compile("\"[a-zA-Z_][a-zA-Z0-9_]\\s*?\"")
re_strings = re.compile("\"([a-zA-Z_][a-zA-Z0-9_]*\\s*)*?\"")
re_space = re.compile("\\s")
re_singlecomment = re.compile("//.*")
re_multcomment_open = re.compile("/\\*.*")
re_multcomment_close = re.compile(".*?\\*/")
re_multcomment_line = re.compile("/\\*.*?\\*/")

ejemplo = """funcion_principal
    cadena cad = "hola mundo";
    imprimir/* ahola */ (3+5);
    //lemur 
fin_principal"""

ejemplo = sys.stdin.read()
pos = 0
col = 1
to_match_4 = [ (re_strings,"cadena"), (re_real,"real"), (re_entero,"entero"), (re_id,"id"), (re_char,"char") ]
to_match_space = [ re_space ]
to_match_3 = [ (re_reserved, RESERVED_WORDS), (re_double, DOUBLE_TOKENS), (re_single, SINGLE_TOKENS) ]

lineas = ejemplo.split("\n")
row = 1
is_comment = False
fatal_error = False

for ejemplo in lineas:
    col = 1
    pos = 0
    
    aux = re_multcomment_close.match(ejemplo[pos:])
    if(is_comment and aux):
        pos += aux.end()
        col += aux.end()
        is_comment = False

            
    if(is_comment):
        row += 1
        continue;
    
    while (pos < len(ejemplo) and not fatal_error):
        made_match = False
        
        aux = re_multcomment_line.match(ejemplo[pos:])
        if(aux):
            pos += aux.end()
            col += aux.end()
            made_match = True
            continue
            
        aux = re_multcomment_open.match(ejemplo[pos:])
        if(aux):
            is_comment = True
            break;
            
        aux = re_singlecomment.match(ejemplo[pos:])
        if(aux):
            pos += aux.end()
            col += 1
            made_match = True
            continue
        
        for m in to_match_3:
            
            aux = m[0].match(ejemplo[pos:])
            if(aux):
                pos += aux.end()
                made_match = True
                print ("<%s,%s,%s>"%(m[1][aux.group()],row,col))
                col += aux.end()
                break
        
        if(made_match):
            continue
            
        for m in to_match_4:
            aux = m[0].match(ejemplo[pos:])
            if(aux):
                made_match = True
                pos += aux.end()
                print ("<%s,%s,%s,%s>"%(m[1],aux.group(),row,col))
                col += aux.end()
                break
        
        if(made_match):
            continue
        
        aux = re_space.match(ejemplo[pos:])
        if(aux):
            pos += aux.end()
            col += 1
            made_match = True
            ##row += 1
            continue
        
        if(not made_match ):
            print ((">>>Error lexico (linea: %s, posicion: %s)")%(row,col))
            fatal_error = True
            break
    row += 1