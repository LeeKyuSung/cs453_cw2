from ast import dump, parse


tmp = "not (1<2)"
print(eval(tmp))
print(dump(parse(tmp)))


x=5
exec("print(x)")

