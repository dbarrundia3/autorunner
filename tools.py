import inspect
import ast

def test_call(source,target):
    call_names = []
    for c in ast.walk(ast.parse(inspect.getsource(source))):
        if isinstance(c, ast.Call):
            try:
                call_names.append(c.func.id)
            except Exception as e:
                pass
    return target.__name__ in call_names