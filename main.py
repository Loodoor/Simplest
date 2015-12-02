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
    vars_declaration = ["dyn", "cst"]

    while True:
        indentation, spaces = 0, 0
        chars_before, type_is_next, name_is_next, value_is_next, expression_is_next, \
            second_expr_is_next, ret_value_is_next, in_argument, type_arg_is_next, \
            name_arg_is_next = [False] * 10
        word, last_arg_name = "", ""

        user_input = input("SPL> ")

        user_input = user_input.replace(':', ' : ').replace('<', ' <')

        # traitement caractère par caractère
        for i in range(len(user_input)):
            char = user_input[i]

            if char == comment:
                break

            if not char.isspace():
                chars_before = True
                if char == ',' and in_argument:
                    char = ' '
                else:
                    word += char

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
                    elif word == "as" and not in_argument:
                        # gestion des types dans les constantes
                        type_is_next = True
                    elif word == "as" and in_argument:
                        # gestion des types des arguments, dans un dico séparé
                        type_arg_is_next = True
                    elif word in tokens_cond:
                        stack['indent'] = indentation
                        stack['structure'] = word
                        expression_is_next = True
                    elif word in ops_cond and expression_is_next:
                        # on est dans un opérateur d'une condition
                        print('in')
                        expression_is_next = False
                        stack['op_cond'] = word
                        second_expr_is_next = True
                    elif word == ":" and second_expr_is_next:
                        # on est à la fin d'une condition
                        second_expr_is_next = False
                    elif word == ":" and stack['structure'] in ('struct', 'func'):
                        # on va entrer dans la liste d'arguments
                        in_argument = True
                        name_arg_is_next = True
                        stack['args'] = {}
                    elif word == "ret":
                        # on a rencontré un token de retour
                        stack['structure'] = "ret"
                        ret_value_is_next = True
                    # assignation autre qu'un mot clé
                    else:
                        if name_arg_is_next:
                            last_arg_name = word
                            name_arg_is_next = False

                        if type_arg_is_next:
                            stack['args'].update({last_arg_name: word})
                            last_arg_name = ""
                            type_arg_is_next = False
                            name_arg_is_next = True

                        if ret_value_is_next:
                            if 'ret_expr' not in stack.keys():
                                stack['ret_expr'] = [word]
                            else:
                                stack['ret_expr'].append(word)

                        if expression_is_next:
                            if word != ':':
                                if 'expr' not in stack.keys():
                                    stack['expr'] = [word]
                                else:
                                    stack['expr'].append(word)

                        if second_expr_is_next:
                            if word != ':':
                                if 'expr2' not in stack.keys():
                                    stack['expr2'] = [word]
                                else:
                                    stack['expr2'].append(word)

                        if value_is_next:
                            if word != ':':
                                if 'value' not in stack.keys():
                                    stack['value'] = [word]
                                else:
                                    stack['value'].append(word)
                            #value_is_next = False

                        if type_is_next:
                            stack['type'] = word
                            type_is_next = False
                            if stack['structure'] in vars_declaration:
                                value_is_next = True

                        if name_is_next:
                            stack['name'] = word
                            name_is_next = False
                            if stack["structure"] == "func":
                                type_is_next = True
                    word = ""

        ast.append(stack)
        print(stack)
        stack = {}

if __name__ == '__main__':
    main()