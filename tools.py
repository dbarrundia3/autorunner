import inspect
import ast

def test_call(source,target):
    call_names = [c.func.id for c in ast.walk(ast.parse(inspect.getsource(source)))
              if isinstance(c, ast.Call)]
    return target.__name__ in call_names