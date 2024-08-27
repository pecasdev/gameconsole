import astunparse
import ast

# source: https://stackoverflow.com/a/42734810
class TypeHintRemover(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # remove the return type defintion
        node.returns = None
        # remove all argument annotations
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        return node

    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node):
        return node if node.module != 'typing' else None

def remove_type_hints_from_source_code(source_code: str) -> str:
    parsed_source = ast.parse(source_code)
    no_types_source_code = TypeHintRemover().visit(parsed_source)
    return astunparse.unparse(no_types_source_code)