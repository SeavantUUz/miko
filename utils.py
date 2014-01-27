import pickle

def get_nodes(func):
    '''only to use decorator'''
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

class BleepRenderer(HtmlRenderer,SmartyPants):
    ''' code highlight '''
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


