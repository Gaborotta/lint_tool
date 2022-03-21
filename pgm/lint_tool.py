from glom import glom
import ast


def get_before_var_assign_by_id(tree, idx, node_id):
    id_list = []
    for i, b in reversed([(i, b) for i, b in enumerate(tree.body[:idx])]):
        if type(b) == ast.Assign:
            id_list = [i for i, t in enumerate(b.targets) if t.id == node_id]
            if len(id_list) > 0:
                break
    if len(id_list) > 0:
        return i, b, id_list[0]
    return None, None, None


def is_target_attr(node, attr_name):
    # nodeが探索対象のattrかどうかを判定
    if type(node) == ast.Call:
        if glom(node, 'func.attr', default=None) == attr_name:
            return True
    return False


def get_arg_by_idx(node, args_idx):
    # 指定idxのargsを取得
    if glom(node.value, 'args', default=None) is not None:
        return node.value.args[args_idx]
    return None


def get_binop(node, tree, now_idx):
    # now_idx = 8
    # node = arg
    left = node.left
    right = node.right
    op = node.op
    left_constant_value = get_constant_value(left, tree, now_idx)
    right_constant_value = get_constant_value(right, tree, now_idx)
    if type(op) == ast.Add:
        return left_constant_value + right_constant_value
    return None


def get_joinedstr(node, tree, now_idx):
    str_list = [get_constant_value(n, tree, now_idx) for n in node.values]
    return ''.join(str_list)


def get_str_format_attr(node, tree, now_idx):
    func_node = node.func
    if type(func_node) == ast.Attribute:
        func_keywords = node.keywords
        func_value = glom(func_node, 'value', default=None)
        if func_value is not None:
            func_value = get_constant_value(func_value, tree, now_idx)

        func_attr = glom(func_node, 'attr', default=None)

        if type(func_value) != str or func_attr != 'format':
            return None

        key_dict = {k.arg: get_constant_value(
            k.value, tree, now_idx) for k in func_keywords}

        return func_value.format(**key_dict)


def get_constant_value(node, tree, now_idx):
    # 展開した定義を返す
    if type(node) == ast.Constant:
        # pprint(ast.dump(node))
        return node.value

    elif type(node) == ast.Name:
        assign_idx, assign, assign_id = get_before_var_assign_by_id(
            tree, now_idx, node.id)

        if assign_idx is not None:
            # assign_node = assign.targets[assign_id]
            return get_constant_value(assign.value, tree, assign_idx)
        return '{' + node.id + '}'

    elif type(node) == ast.BinOp:
        return get_binop(node, tree, now_idx)

    elif type(node) == ast.FormattedValue:
        return get_constant_value(node.value, tree, now_idx)

    elif type(node) == ast.JoinedStr:
        return get_joinedstr(node, tree, now_idx)

    elif is_target_attr(node, 'format'):
        return get_str_format_attr(node, tree, now_idx)


def get_pd_to_csv_path(tree):
    res_list = []
    for now_idx, b in enumerate(tree.body):
        if type(b) == ast.Expr:
            # pprint(ast.dump(b))
            if is_target_attr(b.value, 'to_csv'):
                target_node = b

                arg = get_arg_by_idx(target_node, 0)
                arg_constant = get_constant_value(arg, tree, now_idx)
                res_list.append((now_idx, arg_constant, b))
                print(now_idx, arg_constant, b)
    return res_list


def get_ast_tree(path):
    with open(path) as f:
        source = f.read()
    return ast.parse(source)


# tree = get_ast_tree('sample.py')
# get_pd_to_csv_path(tree)
