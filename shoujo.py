# coding:utf-8
import os,time
import yaml,jinja2,misaka
from Node import Node

config = yaml.load(open('config.yaml','r'))

## from <<python cookbook>>
def paragraphs(text,is_separator=str.isspace,joiner=''.join):
    paragraph = []
    for line in text:
        if is_separator(line):
            if paragraph:
                yield joiner(paragraph)
                paragraph=[]
        else:
            paragraph.append(line)
    if paragraph:
        yield joiner(paragraph)

## varify_properties
## Maybe you can add some new ways 
## to make sure all your properties
## are well
def properties_varify(title,archive,tags,blank):
    if blank != '\n':
        raise Exception("\nPlease obey the rules.First Four line have some special means\n")
    if title == None:
        raise Exception("\nYou should not let the first paragraph empty! Rechek your blog please!\n")
    if archive == None:
        archive = u'未命名'
    if tags == None:
        tags = ['default']
    return (title,archive,tags)


def get_tree(source,NODE=[]):
    for root,dirs,files in os.walk(source):
        for filename in files:
            ## modified time and path
            ## made first line as title
            ## second line as archive
            ## written as:
            ## archive: python
            ## and third line as tags
            ## tags written as this way:
            ## tags:python,sanae
            m_time = os.path.getmtime(filename)
            path = os.path.join(root,filename)
            f = open(filename,'rU') 
            title = f.readline().replace('\n','').replace('\r','')
            archive = f.readline().split(':')[-1].strip()
            tags = f.readline().split(':')[-1].split(',')
            tags = [word.strip() for word in tags]
            ## release the forth line as empty line
            ## which could help varifying
            blank_line = f.readline()
            ## varify above properti are all right
            title,archive,tags = properties_varify(title,archive,tags,blank_line)
            content = f.read()
            ## abstrct always use content's first 
            ## paragraph.I suppose this is split 
            ## from below by empty line
            abstrct = paragraphs(text.splitlines(True)).next()
            if len(abstrct)>=800:
                raise Exception("\nYou did't split abstrct from below by blank line!!\n\n")
            node = Node(timestamp = m_time,title=title,path = path,archive=archive,tags=tags,content=content,abstrct=abstrct)
            NODE.append(node)
    return NODE


def generate_homepage(nodes,env):
    template = env.get_template(TEMPLATES['home'])
    write_file('index.html',template.render(posts = nodes[:HOME_POSTS]))

def generate_post(node,env):
    template = env.get_template(TEMPLATES['post'])
    write_file(node['url'],template.render(post = node))

