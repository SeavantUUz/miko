from shoujo.utils import save_nodes,get_nodes,parse,getconfig
from shoujo.node import Node
from shoujo.pagination import Pagination
from shoujo.env import env
import codecs

def _node(filename):
    elements = parse(filename)
    node = Node(**elements)
    return node

def _render(object,template):
    template = env.get_template(template)
    html = template.render(object)
    configs = getconfig()
    app = configs['app']
    out = configs['out']
    try:object.archive
    except AttributeError:
        filename = os.path.join(app,out,object.title+'.html')
    else:filename = os.path.join(app,out,'posts',object.title+'.html')
    with codecs.open(filename) as f:
        f.write(html)
        f.close()
    return node

def render(func):
    def wrapper(*args,**kwargs):
        nodes = func(*args,**kwargs)
        pages = Pagination(nodes).pages
        paginations = map(lambda i:Pagination(nodes,i),range(pages))
        map(lambda node:_render(node,'post.html'),nodes)
        map(lambda page:_render(page,'page.html'),paginations)
        return nodes
    return wrapper

@render
@save_nodes
@get_nodes
@sort_nodes
def post(nodes,filename):
    '''post a article,elements is a dict'''
    node = _node(filename)
    nodes = filter(lambda o:o.title != node.title,nodes)
    nodes.append(node)
    #_generatorHtml(nodes)
    return nodes


@render
@save_nodes
@sort_nodes
def postDir(dirname):
    '''post dirs,which would try all files in dirs
       and post them'''
    # dirs = filter(lambda d:os.path.isdir(d),args)
    # for d in dirs:
    for root,dirs,files in os.walk(dirname):
        nodes = map(_node,[os.path.join(root,f) for f in files])
    return nodes


@get_nodes
def show(nodes):
    if not nodes:
        print u'这里空空如也，什么都没有\n'
    else:
        print '\n-----------------------------'
        for i,o in enumerate(nodes):
            print u'%5d:  %s' % (i,o)

@render
@save_nodes
@get_nodes
def remove(nodes,index):
    if not nodes:
        print u'这里空空如也，没什么需要删除的\n'
    else:
        try:
            node = nodes[index]
        except IndexError:
            print u'您所要求的索引溢界'
            return None
        else:
            print u'\n真的希望删除 {0}: {1} ? (yes/no)'.format(index,nodes[index])
            choose = raw_input()
            if choose == 'yes':
                _removePost(node)
                nodes.remove(node)
                return nodes
            else:
                return None


