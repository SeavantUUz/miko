#coding:utf-8
from shoujo.utils import save_nodes,get_nodes,sort_nodes,parse,getconfig,update_themes,_nodesdic,_tagsdic,_dontcare
from shoujo.node import Node
from shoujo.pagination import Pagination
import codecs,shutil,os,SimpleHTTPServer,SocketServer

def _node(filename):
    elements = parse(filename)
    node = Node(**elements)
    return node

def _render(item,template):
    from shoujo.env import env
    template = env.get_template(template)
    html = template.render(item=item)
    configs = getconfig()
    app = configs['app']
    out = configs['out']
    try:item.archive
    except AttributeError:
        filename = os.path.join(app,out,item.title+'.html')
    else:filename = os.path.join(app,out,'posts',item.title+'.html')
    with codecs.open(filename,'w','utf-8') as f:
        f.write(html)
        f.close()
    return item

def tags(func):
    def wrapper(*args,**kwargs):
        nodes = func(*args,**kwargs)
        configs,template,tags,path = _dontcare(nodes,'tags',_tagsdic)
        html = template.render(title = configs['tags_title'],tags = tags)
        with codecs.open(path,'w','utf-8') as f:
            f.write(html)
        return nodes
    return wrapper

def archive(func):
    def wrapper(*args,**kwargs):
        nodes = func(*args,**kwargs)
        configs,template,archives,path = _dontcare(nodes,'archive',_nodesdic)
        html = template.render(title = configs['archive_title'],archives=archives)
        with codecs.open(path,'w','utf-8') as f:
            f.write(html)
        return nodes
    return wrapper

def sitemap(func):
    def wrapper(*args,**kwargs):
        nodes = func(*args,**kwargs)
        configs = getconfig()
        app = configs.get('app')
        home = configs.get('home')
        out = configs.get('out')
        with codecs.open(os.path.join(app,'sitemap.txt'),'w','utf-8') as sitemap:
            for node in nodes:
                url = home+'/'+node.url
                sitemap.write(url+'\n')
        return nodes
    return wrapper

def feed(func):
    def wrapper(*args,**kwargs):
        from shoujo.env import env
        nodes = func(*args,**kwargs)
        configs = getconfig()
        template = env.get_template('feed.xml')
        html = template.render(nodes=nodes)
        f = codecs.open(os.path.join(configs['app'],'feed.xml'),'w','utf-8')
        f.write(html)
        f.close()
        return nodes
    return wrapper

def _content(filename):
    from shoujo.env import env
    configs = getconfig()
    htmlfile = filename + '.html'
    mdfile = filename + '.md'
    path = os.path.join(configs['app'],configs['out'],htmlfile)
    template = env.get_template(htmlfile)
    with codecs.open(mdfile,'r','utf-8') as fcontent:
        content = '\n'.join([line.replace('\n','  \n') for line in fcontent])
    html = template.render(content=content)
    f = codecs.open(path,'w','utf-8')
    f.write(html)
    print '\n{0} page 生成结束'.format(filename)

def render(func):
    def wrapper(*args,**kwargs):
        ## delete old rendered pages and html files
        configs = getconfig()
        dirname = os.path.join(configs['app'],configs['out'])
        for root,dirs,files in os.walk(dirname):
            for name in files:
                if  name == 'links.html' or \
                    name == 'about_me.html' or \
                    name == 'robots.txt':
                    continue 
                else: os.remove(os.path.join(root,name))
        # rerender
        nodes = func(*args,**kwargs)
        if not nodes:
            return None
        pages = Pagination(nodes).pages
        paginations = map(lambda i:Pagination(nodes,i+1),range(pages))
        map(lambda node:_render(node,'post.html'),nodes)
        map(lambda page:_render(page,'page.html'),paginations)
        return nodes
            
    return wrapper

@feed
@sitemap
@tags
@archive
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


@feed
@sitemap
@tags
@archive
@render
@save_nodes
@sort_nodes
@update_themes
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
    print '\n-----------------------------\n'
    if not nodes:
        print u'这里空空如也，什么都没有'
    else:
        for i,o in enumerate(nodes):
            print u'%5d:  %s' % (i,o)
    print '\n-----------------------------\n'

@feed
@sitemap
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
            return nodes
        else:
            print u'\n真的希望删除 {0}: {1} ? (yes/no)'.format(index,nodes[index])
            choose = raw_input()
            if choose == 'yes':
                nodes.remove(node)
            return nodes

@save_nodes
def init():
    configs = getconfig()
    app = configs['app']
    out = configs['out']
    theme = configs['theme']
    try: os.remove('data.pick')
    except OSError:pass
    try:os.mkdir(app)
    except OSError:
        print u'\n检测到已存在的目录树，删掉它么?(yes/no)'
        choose = raw_input()
        if choose == 'yes':
            shutil.rmtree(app)
            os.mkdir(app)
    else:
        shutil.copytree('themes',os.path.join(app,'themes'))
        os.mkdir(os.path.join(app,out))
        os.mkdir(os.path.join(app,out,'posts'))
        print u'目录结构已建立'

@update_themes
def themes():
    '''update themes.In fact,decorater handle all things'''
    return None

def links(func):
    '''generate links.html'''
    return _content('links')

def aboutme():
    '''generate about_me.html'''
    return _content('about_me')

def preview():
    configs = getconfig()
    app = configs['app']
    os.chdir(os.path.join(app))
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(('localhost',PORT),Handler)
    print u'运行服务器在http://localhost:8000'
    httpd.serve_forever()
