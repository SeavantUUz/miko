#coding:utf-8
__all__ = ['get_nodes','BleepRenderer']

import pickle

def get_nodes(func):
    '''A decorator for getting nodes'''
    try:
        pick = open('data.pick','rb')
    except IOError:
        nodes = []
    else:
        nodes = pickle.load(pick)
        pick.close()
    def wrapper(*args,**kwargs):
        return func(nodes,*args,**kwargs)
    return wrapper

def save_nodes(func):
    '''A decorator for saving nodes'''
    def wrapper(*args,**kwargs):
        nodes = func(*args,**kwargs)
        if nodes
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
