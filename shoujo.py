# coding:utf-8
import os,time
import yaml,jinja2,misaka
from Node import Node

##config = yaml.load(open('config.yaml','r'))

OUT_DIR = '/home/aprocysanae/outdir'

def paragraphs(text,is_separator=str.isspace,joiner=''.join):
    ''' To split the text to paragraphs.return a generator '''

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
    ''' varify your article.'''

    if blank != '\n':
        raise Exception("\nPlease obey the rules.First Four line have some special means\n")
    if title == None:
        raise Exception("\nYou should not let the first paragraph empty! Rechek your blog please!\n")
    if archive == None:
        archive = u'未命名'
    if tags == None:
        tags = ['default']
    return (title,archive,tags)

def built(filename,auto_abstrct=False,max_lenth=1000):
    ''' convert markdown file to html,to let the process more clearly,please remember the below rules:
        1. the first line is your article's title
        2. the second line your should written as this:
        archive: python
        or leave it as a empty line
        3. the third line is the tags,like second line,you should written as this:
        tags:python,sanae
        4. please always leave the forth line as a empty line which could help the program varify all you written above are right '''

    m_time = os.path.getmtime(filename)
    f = open(filename,'rU') 
    title = f.readline().replace('\n','').replace('\r','').strip()
    path = os.path.join(OUT_DIR,title+'.html')
    archive = f.readline().split(':')[-1].strip()
    tags = f.readline().split(':')[-1]
    tags = tags.decode('utf-8').replace(u'，',',').split(',')
    tags = [word.strip() for word in tags]
    blank_line = f.readline()
    title,archive,tags = properties_varify(title,archive,tags,blank_line)
    ## abstrct always use content's first 
    ## paragraph.I suppose this is split 
    ## from below by empty line
    ## set auto_abstrct to control the behavior
    ## of getting abstrct.by lenth or by blankline
    if auto_abstrct == True:
        abstrct = f.read(max_lenth)
        content = ''.join([abstrct,f.read()])
    else:
        text = f.read()
        paragraph = paragraphs(text.splitlines(True))
        abstrct = paragraph.next()
        try:
            remainText = paragraph.next()
        except StopIteration:
            remainText = ''
        content = ''.join([abstrct,remainText])
    node = Node(timestamp = m_time,title=title,path = path,archive=archive,tags=tags,content=content,abstrct=abstrct)
    return node


##def rebuiltAll(source,NODE=[]):
##    for root,dirs,files in os.walk(source):
##        for filename in files:
##            m_time = os.path.getmtime(filename)
##            path = os.path.join(root,filename)
##            NODE.append(node)
##    return NODE
##
##
##def generate_homepage(nodes,env):
##    template = env.get_template(TEMPLATES['home'])
##    write_file('index.html',template.render(posts = nodes[:HOME_POSTS]))
##
##def generate_post(node,env):
##    template = env.get_template(TEMPLATES['post'])
##    write_file(node['url'],template.render(post = node))

if __name__ == '__main__':
    print Node
    node = built('example')
    for i in [node.Title,node.TimeStamp,node.Path,node.Tags,node.Content,node.Archive,node.Abstrct]:
        print i,'\n'
