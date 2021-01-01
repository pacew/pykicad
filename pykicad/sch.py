from pykicad.sexpr import *
from pykicad.module import Module, Net, xy_schema
from pykicad.sexpr import number, text, integer, boolean, flag, Optional
from pykicad.sexpr import tuple_parser, AST, Literal, Group, OneOrMore
from pykicad.sexpr import allowed, extend_schema, extend_schema, yes_no
from pykicad.sexpr import Suppress, tree_to_string

def comment(number):
    str_num = str(number)
    return {
        '_tag': 'comment',
        '_attr': 'comment' + str_num,
        '_parser': Suppress(str_num) + text,
        '_printer': (lambda x: '(comment %s %s)' %
                     (str_num, tree_to_string(x)))
    }

class Size(AST):
    tag = 'size'
    schema = {
        '0': {
            '_attr': 'width',
            '_parser': number
        },
        '1': {
            '_attr': 'height',
            '_parser': number
        }
    }

    def __init__(self, width=None, height=None):
        super(self.__class__, self).__init__(width=width, height=height)

def qstring(name):
    # if the input side is changed to interpret c escapes
    # change _printer here to json.dumps
    return {
        '_parser': text,
        '_printer': lambda val: f'"{val}"',
        '_tag': False,
        '_attr': name
    }

class PinNumbers(AST):
    tag = 'pin_numbers'
    schema = {
        'hide': flag('hide')
    }

    def __init__(self, hide=None):
        super(self.__class__, self).__init__(hide=hide)

class PinNames(AST):
    tag = 'pin_names'
    schema = {
        'offset': number,
        'hide': flag('hide')
    }

    def __init__(self, offset=None, hide=None):
        super(self.__class__, self).__init__(offset=offset, hide=hide)


class Symbol(AST):
    tag = 'symbol'
    schema = {
        '0': qstring('symbol_name'),
        'pin_numbers': {
            '_parser': PinNumbers
        },
        'pin_names': {
            '_parser': PinNames
        }
    }

    def __init__(self, name='', symbol_name=None, pin_numbers=None, pin_names=None):
        super(self.__class__, self).__init__(symbol_name=symbol_name, pin_numbers=pin_numbers,
                                             pin_names=pin_names)


class Paper(AST):
    tag = 'paper'
    schema = {
        'psize': qstring('psize')
    }

    def __init__(self, name='', psize=None):
        super(self.__class__, self).__init__(psize=psize)



class Font(AST):
    tag = 'font'
    schema = {
        'size': {
            '_parser': Size
        }
    }

    def __init__(self, name='', size=None, bar=None):
        super(self.__class__, self).__init__(size=size, bar=bar)

class LibSymbols(AST):
    tag = 'lib_symbols'
    schema = {
        'symbol': {
            '_parser': Symbol
        }
    }

    def __init__(self, name='', symbol=None):
        super(self.__class__, self).__init__(symbol=symbol)


class Sch(AST):
    tag = 'kicad_sch'
    schema = {
        '0': {
            '_tag': 'version',
            '_parser': integer
        },
        'host': {
            '_parser': text + text
        },
        'generator': {
            '_parser': text
        },
        'paper': {
            '_parser': Paper
        },

        'font': {
            '_parser': Font
        },

        'lib_symbols': {
            '_parser': LibSymbols
        }

        # '3': {
        #     '_tag': 'lib_symbols',
        #     '_parser': Group(ZeroOrMore(text))
        # },
        # '4': {
        #     '_tag': 'symbol_instances',
        #     '_parser': Group(ZeroOrMore(text))
        # }
    }

    def __init__(self, 
                 version=1, 
                 host=['pykicad', 'x.x.x'],
                 generator=None,
                 paper=None,
                 lib_symbols=None,
                 symbol_instances=None,
                 font=None,
                 bar=None
    ):
        # lib_symbols = self.init_list(lib_symbols, [])
        symbol_instances = self.init_list(symbol_instances, [])

        super(self.__class__, self).__init__(version=version, 
                                             generator=generator,
                                             host=host,
                                             paper=paper,
                                             lib_symbols=lib_symbols,
                                             symbol_instances=symbol_instances,
                                             font=font,
                                             bar=bar
        )

    def to_file(self, path):
        if not path.endswith('.kicad_sch'):
            path += '.kicad_sch'
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(self.to_string())

    @classmethod
    def from_file(cls, path):
        return Sch.parse(open(path, encoding='utf-8').read())
