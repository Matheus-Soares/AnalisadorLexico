import csv
import sys

tokens = {}

# Palavras reservadas
espec = ["while", "void", "string", "return", "main", "integer", "inicio", "if", "for", "float", "fim", "else", "double", "do", "cout" , "cin", "char", "callfuncao"]

# Simbolos
simbols = ["!", ">>", ">=", ">", "==", "=", "<=", "<<", "<", "++", "+", "}", "{", ";", ":", "/", ",", "*", ")", "(", "$", "!=", "--", "-"]

# Leitura da tabela de tokens
def read_tokens():
	with open("tokens.csv") as table_:
		table = csv.reader(table_, delimiter='\t')
		for row in table:
			tokens[row[0]] = row[1]


# Imprime tokens
def print_token(lex, row):
	print("<{}, {}, {}>" .format(lex, tokens[lex], row))


# Le arquivo e classifica lexicamente, indicando erros
def analyzer():
	print("<Lexema, Token, Linha>\n")
	lex = ""
	row = 0
	count = 0

	with open(sys.argv[1], 'r') as code:

		# Sempre começa o while com um novo caracter não reconhecido
		char = code.read(1)
		while char:
			lex = ""

			# Ignora espaços em branco
			if char == " " or char == "\t":
				char = code.read(1)
				continue

			# Incrementa linha
			elif char == "\n":
				row += 1
				char = code.read(1)
				continue

			# Comantarios
			elif char == "%":
				char = code.read(1)

				# Comentario em linha
				if char != "*":
					char = code.read(1)
					while char != "\n" and char:
						char = code.read(1)
					row += 1
					char = code.read(1)
					continue

				# Comentario em bloco
				else:
					char1 = code.read(1)
					char2 = code.read(1)
					if char1 == "\n":
						row += 1
					while char1 != "*" and char2 != "%":
						if char2 == "\n":
							row += 1

						char1 = char2
						char2 = code.read(1)
						if not char1 and not char2:
							print("\tErro: Não foi fechado comentario em bloco. Linha {}." .format(row))
							exit()

					char = code.read(1)
					continue
			
			# Se não for comentario
			else:
				# Se for digito
				if char.isdigit():
					while char.isdigit() and char:
						char = code.read(1)
					
					# Numero float
					if char == ".":
						char = code.read(1)
						while char.isdigit() and char:
							char = code.read(1)
						if not char or char == " " or char == "\n" or char == "\t":
							print_token("numerofloat", row)

							if char == "\n":
								row += 1

							char = code.read(1)
							continue

						elif char in simbols:
							print_token("numerofloat", row)
							continue

						else:
							print("\tErro: Caracter invalido. Linha {}." .format(row))
							exit()

					# Numero inteiro
					else:
						if not char or char == " " or char == "\n" or char == "\t":
							print_token("numerointeiro", row)

							if char == "\n":
								row += 1

							char = code.read(1)
							continue

						elif char in simbols:
							print_token("numerointeiro", row)
							continue
						else:
							print("\tErro: Caracter invalido. Linha {}." .format(row))
							exit()
				
				else:
					# Simbolos
					if char in simbols:
						lex += char
						char2 = code.read(1)
						lex += char2
						if lex in simbols:
							print_token(lex, row)

							char = code.read(1)
							continue

						else:
							print_token(char, row)
							char = char2
							continue

					# Literal
					elif char == "@":
						count+=1
						char = code.read(1)
						while char != "@" and char:
							count += 1

							# Tamanho maximo de 32 caracteres
							if count > 32:
								print("\tErro: Excedido o tamanho maximo de literal. Linha {}." .format(row))
								exit()

							if char == "\n":
								row += 1

							char = code.read(1)

						if not char:
							print("\tErro: Não foi fechado literal. Linha {}." .format(row))
							exit()

						else:
							count = 0
							print_token("literal", row)
							char = code.read(1)
							continue

					# Outros casos: palavra reservada válida ou nome de variavel
					else:
						while char.isalnum() and char:
							count += 1

							# Tamanho maximo de 32 caracteres
							if count > 32:
								print("\tErro: Excedido o tamanho maximo de nome de variavel. Linha {}." .format(row))
								exit()
							lex += char
							char = code.read(1)

						if char in simbols or char == " " or char == "\t" or char == "\n":
							if lex in tokens:
								print_token(lex, row)	
							else:
								print_token("nomevariavel", row)
								
							if char == "\n":
								row += 1
								char = code.read(1)
							count = 0
							continue

						else:
							if char == '"':
								char = code.read(1)
								while char != '"' and char:
									lex += char
									char = code.read(1)
								if not char:
									print("\tErro: Não foi fechado string. Linha {}." .format(row))
									exit()
								else:
									if char == "\n":
										row += 1
									print_token("nomedastring", row)
									char = code.read(1)
									continue

							if char == "'":
								char = code.read(1)
								char1 = code.read(1)
								if char1 == "'" and char and char1:
									print_token("nomedochar", row)
									char = code.read(1)
									continue
								else:
									print("\tErro: Declaração incorreta de char. Linha {}." .format(row))
									exit()

							print("\tErro: Caracter invalido. Linha {}." .format(row))
							exit()
	
	return()

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("Usage: \n\tpython3 lexical.py 'your_file'.blocky")
	else:
		# Le a tabela de tokens
		read_tokens()

		# Le o arquivo passado como argumento e analisa lexicamente
		analyzer()