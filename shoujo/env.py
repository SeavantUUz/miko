#coding:utf-8
from jinja2 import Environment,PackageLoader
from utils import getconfig
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from misaka import HtmlRenderer,SmartyPants
import misaka as m
import datetime

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

def xmldatetime(value):
    date = datetime.datetime.fromtimestamp(value)  
    return date.strftime('%Y-%m-%d %H:%M')

def markdown(data):
    renderer = BleepRenderer()
        md = m.Markdown(renderer,
        extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
        return md.render(data) 

configs = getconfig()
application = config.get('app')
env = Environment(loader=PackageLoader(application,'templates'))
filters = {'datetime':xmldatetime,'markdown':markdown}
env.filters(filters)
env.globals(configs)
