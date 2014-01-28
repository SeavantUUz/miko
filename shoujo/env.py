#coding:utf-8
from jinja2 import Environment,PackageLoader
from utils import getConfig 
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from misaka import HtmlRenderer,SmartyPants
import misaka as m

__all__ = ['env']

class BleepRenderer(HtmlRenderer,SmartyPants):
    ''' code highlight '''
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def datetime(value):
    pass

def markdown(data):
   renderer = BleepRenderer()
        md = m.Markdown(renderer,
        extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
        return md.render(data) 

application = getConfig('app')
env = Environment(loader=PackageLoader(application,'templates'))
env.filters['datetime'] = datetime
