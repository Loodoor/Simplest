class Struct:
    def __init__(self, name: str):
        self.name = name


class Func:
    def __init__(self, name: str, type_: Struct, args: list, corps: str):
        self.name = name
        self.type = type_
        self.args = args
        self.corps = corps


def main():
    stack = {}
    ast = []
    keywords = ['func', 'struct', 'dyn', 'cst', 'end']
    comment = ';'
    tokens_cond = ["if", "elif", "else"]
    ops_cond = ["==", "!=", "<", ">", "<=", ">="]

    while True:
        indentation, spaces = 0, 0
        chars_before, type_is_next, name_is_next, value_is_next, \
            expression_is_next, second_expr_is_next = [False] * 6
        word = ""

        user_input = input("SPL> ")

        replaced = {'<': 0, '>': 0, ':': 0}
        ui = list(user_input)

        for i in range(len(ui)):
            c = ui[i]
            if c in '<>:' and not replaced[c]:
                replaced[c] = 1
                ui[i] = ' '
        user_input = ''.join(ui) + ' '

        # traitement caractère par caractère
        for i in range(len(user_input)):
            char = user_input[i]

            if char == comment:
                break

            if char.isspace():
                # gestion de l'indentation
                if not chars_before:
                    spaces += 1
                    if not spaces % 4:
                        indentation += 1
                        spaces = 0
                # gestion des mots
                if word:
                    # gestion des mots clés
                    if word in keywords:
                        stack['indent'] = indentation
                        stack['structure'] = word
                        name_is_next = True
                    elif word == "as":
                        type_is_next = True
                    elif word in tokens_cond:
                        stack['indent'] = indentation
                        stack['structure'] = word
                        expression_is_next = True
                    elif word in ops_cond and expression_is_next:
                        # on est dans un opérateur d'une condition
                        expression_is_next = False
                        stack['op_cond'] = word
                        second_expr_is_next = True
                    elif word == ":" and second_expr_is_next:
                        # on est à la fin d'une condition
                        second_expr_is_next = False
                    # assignation autre qu'un mot clé
                    else:
                        if expression_is_next:
                            if 'expr' not in stack.keys():
                                stack['expr'] = [word]
                            else:
                                stack['expr'].append(word)

                        if second_expr_is_next:
                            if 'expr2' not in stack.keys():
                                stack['expr2'] = [word]
                            else:
                                stack['expr2'].append(word)

                        if value_is_next:
                            stack['value'] = word
                            value_is_next = False

                        if type_is_next:
                            stack['type'] = word
                            type_is_next = False
                            if stack['structure'] in ('dyn', 'cst'):
                                value_is_next = True

                        if name_is_next:
                            stack['name'] = word
                            name_is_next = False
                            if stack["structure"] == "func":
                                type_is_next = True
                    word = ""
            else:
                chars_before = True
                word += char

        ast.append(stack)
        print(stack)
        stack = {}

if __name__ == '__main__':
    main()