"""
"""
import os
import sys
import inspect
import collections
import textwrap

from pprint import pprint

Member = collections.namedtuple('Member', ('type', 'name', 'doc', 'children'))

def analyse_member(name, member, ignore_private=True):
    if ignore_private and (name.startswith('__')):
        return 

    member_type = None
    if inspect.ismodule(member):
        member_type = 'module'
    elif inspect.isclass(member):
        member_type = 'class'
    elif inspect.ismethod(member):
        member_type = 'method'
    elif inspect.isfunction(member):
        member_type = 'function'
    else:
        raise Exception('Invalid member type %s' % (name, ))

    member_children = []
    for child_name, child_member in inspect.getmembers(member):
        child = analyse_member(child_name, child_member)
        if child:
            member_children.append(child)

    return Member(member_type, name, inspect.getdoc(member), member_children)


def pprint_member_result(t):
    d = []
    for field in t._fields:
        attr = getattr(t, field)
        if isinstance(attr, (str, bool, int, float, )):
            d.append('%s=%r' % (field, attr))
        elif isinstance(attr, list):
            if not attr:
                continue
            d.append('%s=[' % (field, ))
            for s in map(pprint_member_result, attr):
                d += [' ' * (len(field) + 2) + l for l in s.split('\n')]
            d.append(']')



    name = t.__class__.__name__
    indent = ' ' * (len(name) + 1)
    wrapper = textwrap.TextWrapper(width=80, initial_indent=indent, subsequent_indent=indent)
    
    s = '%s(%s)' % (name, (',\n' + indent).join(d))

    return s


if __name__ == '__main__':
    for path, folders, files in os.walk('test'):
        sys.path.append(path)
        for file_name in files:
            if not file_name.endswith('.py'):
                continue
            module_name = file_name.rsplit('.', 1)[0]
            try:
                module = __import__(module_name, globals(), locals(), [], 0)
            except Exception as exc:
                print("Exception importing module `%s`: %s" % (module_name, exc))
                continue

            result = analyse_member(module_name, module)

            # pprint(dir(result))
            print(pprint_member_result(result))
            del module
