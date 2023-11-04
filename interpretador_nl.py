import re

variables = {}

def lexer(input_string):
    tokens = re.findall(r'\b\w+\b|\S', input_string)
    return tokens

def evaluate_expression(tokens):
    operator_translations = {
        'mais': '+',
        'menos': '-',
        'vezes': '*',
        'dividido por': '/',
        'resto da divisao de': '%',
        'é maior que': '>',
        'é menor que': '<',
        'é igual a': '=='
    }

    stack = []
    operator = None

    for token in tokens:
        if token.isnumeric():
            stack.append(int(token))
        elif token in operator_translations:
            operator = operator_translations[token]
        elif token == '?':
            if operator is None or len(stack) < 2:
                raise ValueError("Expressão mal formada.")
            b = stack.pop()
            a = stack.pop()
            result = eval(f'{a} {operator} {b}')
            stack.append(result)
        elif token.isalpha():
            if token in variables:
                stack.append(variables[token])
            else:
                raise ValueError(f"Variável '{token}' não definida.")
        else:
            raise ValueError(f"Token desconhecido: {token}")

    if operator is None or len(stack) < 2:
        raise ValueError("Expressão mal formada.")

    a, b = stack.pop(), stack.pop()
    result = eval(f'{a} {operator} {b}')
    return result

def assign_variable(variable_name, value):
    variables[variable_name] = value

def main():
    while True:
        input_string = input("Digite uma expressão ou 'sair' para encerrar: ")
        if input_string == 'sair':
            break
        if '=' in input_string:
            parts = input_string.split('=')
            if len(parts) == 2:
                variable_name, expression = parts[0].strip(), parts[1].strip()
                try:
                    tokens = lexer(expression)
                    result = evaluate_expression(tokens)
                    assign_variable(variable_name, result)
                    print(f"Variável '{variable_name}' atribuída como {result}")
                except (ValueError, ZeroDivisionError) as e:
                    print("Erro:", e)
            else:
                print("Expressão inválida.")
        else:
            try:
                tokens = lexer(input_string)
                result = evaluate_expression(tokens)
                print("Resultado:", result)
            except (ValueError, ZeroDivisionError) as e:
                print("Erro:", e)

if __name__ == "__main__":
    main()
