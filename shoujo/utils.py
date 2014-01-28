#coding:utf-8
__all__ = ['sort_nodes','get_nodes','save_nodes','BleepRenderer']

import pickle

def sort_nodes(func):
    def wrapper(*args,**kwargs):
        return sorted(func(*args,**kwargs))
    return wrapper

def get_nodes(func):
    '''A decorator for getting nodes,
    import a key word mask to stop decorator.'''
    def wrapper(*args,**kwargs):
        try:
            pick = open('data.pick','rb')
        except IOError:
            nodes = []
        else:
            nodes = pickle.load(pick)
            pick.close()
        return func(nodes,*args,**kwargs)
    return wrapper

def save_nodes(func):
    '''A decorator for saving nodes'''
    def wrapper(*args,**kwargs):
        nodes = func(*args,**kwargs)
        if nodes:
            pick = open('data.pick','wb')
            pick.dump(nodes)
            pick.close()
        return nodes
    return wrapper

class BleepRenderer(HtmlRenderer,SmartyPants):
    ''' code highlight '''
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)
