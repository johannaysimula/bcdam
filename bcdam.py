import clingo
class Context:
    def id(self, x):
        return x
    def seq(self, x, y):
        return [x, y]

def on_model(m):
    print (m)

ctl = clingo.Control()
ctl.add("base", [], """\
p(@id(10)).
q(@seq(1,2)).
""")
ctl.ground([("base", [])], context=Context())
ctl.solve(on_model=on_model)
