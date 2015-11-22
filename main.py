import re


INT = "(?P<ival>[0-9]+)"
FLOAT = "(?P<fval>[0-9]*\.[0-9]+)"
STR = "(?P<sval>\".*\")"
COMMENT = ";.+"
FUNC_DECLARE = "func +(?P<func_name>[a-zA-Z0-9\?!]+) *<(?P<func_type>(int|float|str|void|empty))> *: *(?P<func_args>.+)*(\r|\n|\r\n)+(?P<func_body>(.|\r|\n|\r\n)+)*(\r|\n|\r\n)*(end +(?P=func_name)|ret +(?P<func_return>.+)) *"
VAR_DECLARE = "(?P<var_declare_type>(dyn|cst)) +(?P<var_name>[a-zA-Z0-9\?!]+) +as +(int|float|str) *: *(?P<value>.+)"
FUNC_BEGIN = "func +(?P<func_name>[a-zA-Z0-9\?!]+) *<(?P<func_type>(int|float|str|void|empty))> *: *(?P<func_args>.+)*"
ARGS_CATCHER = "(?P<arg_name>.+) +as +(?P<arg_type>(int)|(float)|(str))"

NEW_LINE = "\r\n"

types = [STR, FLOAT, INT]
tokens = [VAR_DECLARE, FUNC_DECLARE, COMMENT] + types
semi = [FUNC_BEGIN]


def main():
    stack = []
    tmp = ""

    while True:
        founded = False
        user_input = input("SPL:> ") if not tmp else tmp + NEW_LINE + input("SPL:: ")

        for reg in tokens:
            parsed = re.match(reg, user_input)
            print("tokenzing ... (with : {})".format(reg))

            if parsed:
                print("parsed !")
                founded = True
                ast = parsed.groupdict({})
                if "value" in ast.keys() and ast["value"]:
                    for type_ in types:
                        val = re.match(type_, ast["value"])
                        if val:
                            ast["value"] = val.groupdict()
                            break
                if "func_args" in ast.keys() and ast["func_args"]:
                    for tok in tokens:
                        parsed2 = re.match(tok, ast['func_args'])
                        if parsed2:
                            ast['func_args'] = parsed2.groupdict()
                            break
                print(ast)
                tmp = ""
                stack.append(ast)
        if not founded:
            for reg in semi:
                print("using semi expressions ...")
                parsed = re.match(reg, user_input)

                if parsed:
                    print("parsed (with : {}) !".format(reg))
                    tmp = user_input if not tmp else tmp + NEW_LINE + user_input
                    break


if __name__ == '__main__':
    main()