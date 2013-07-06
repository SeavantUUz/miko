# coding:utf-8
import os,time,codecs,sys,pickle,shutil
import yaml
from jinja2 import Environment,FileSystemLoader,TemplateNotFound
import houdini as h
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import misaka as m
from misaka import HtmlRenderer,SmartyPants
from Node import Node,Site


class BleepRenderer(HtmlRenderer,SmartyPants):
    ''' code highlight '''
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def _paragraphs(text,is_separator=unicode.isspace,joiner=''.join):
    ''' To split the text to abstrct and content '''

    isAbstrct = False
    paragraph = []
    abstrct = ''
    content = ''
    for line in text:
        if isAbstrct == False:
            if is_separator(line): 
                if paragraph:
                    abstrct = joiner(paragraph)
                    paragraph=[]
                    isAbstrct = True
            else:
                paragraph.append(line)
        else:
            paragraph.append(line)
    if paragraph:
        content = joiner(paragraph)
    return abstrct,content

def _splitList(List,n):
    ''' split list each element of list is on same page'''
    i = 0
    nlist = []
    while i+n <= len(List):
        nlist.append(List[i:i+n])
        i += n
    nlist.append(List[i:])
    return nlist

## varify_properties
## Maybe you can add some new ways 
## to make sure all your properties
## are well
def _properties_varify(title,archive,tags,blank):
    ''' varify your article.'''

    if blank != '\n':
        raise Exception("\nPlease obey the rules.First Four line have some special means\n")
    if title == None:
        raise Exception("\nYou should not let the first paragraph empty! Recheck your blog please!\n")
    if archive == '':
        archive = u'未命名'
    if tags[0] == u'':
        tags = ['default']
    return (title,archive,tags)

def _getNodes():
    ''' unpick data.pick,getNodes'''
    try:
        pick = open('data.pick','rb')
    except IOError:
        Nodes = []
    else:
        Nodes = pickle.load(pick)
        pick.close()
    return Nodes

def _writeNodes(Nodes):
    ''' writeNodes'''
    pick = open('data.pick','wb')
    pickle.dump(Nodes,pick) 
    pick.close()

def _readConfig():
    ''' read config file '''
    config = yaml.load(open('config.yaml','r'))
    return config


def _renderToHtml(node):
    ''' convert file to html '''
    config = _readConfig()
    site = Site(config)
    ## get themes path and import it
    path = os.path.join(config['MAIN_PATH'],'themes',config['THEME_DIR'])
    ## jinja will handle the error
    env = Environment(loader=FileSystemLoader(os.path.join(path,'templates')))
    template = env.get_template('post.html')
    html = template.render(post=node,site=site,post_flag = True)
    f = codecs.open(os.path.join(config['MAIN_PATH'],config['OUTDIR'],'posts',node.Title+'.html'),'w','utf-8')
    f.write(html)
    f.close()

def _renderToPage(Nodes):
    config = _readConfig()
    site = Site(config)
    L_nodes = _splitList(Nodes,config['POSTS_NUM'])
    path = os.path.join(site.mainDir,'themes',site.themeDir)
    env = Environment(loader=FileSystemLoader(os.path.join(path,'templates')))
    template = env.get_template('page.html')
    for i,nodes in enumerate(L_nodes):
        before_page = True
        next_page = True
        ## only one page
        if len(L_nodes) == 1:
            before_page = False
            next_page = False
        ## not only one page
        elif i == 0:
            before_page = False
        elif i == len(L_nodes)-1:
            next_page = False
        html = template.render(posts=nodes,pagen=i,site=site,before_page=before_page,next_page=next_page)
        #if i == 0:
            #   f = codecs.open(os.path.join(site.mainDir,site.outDir,'home.html'),'w','utf-8')
        #else:
        pagename = u'page_%d.html' % i
        f = codecs.open(os.path.join(config['MAIN_PATH'],config['OUTDIR'],pagename),'w','utf-8')
        f.write(html)
        f.close()

def _ListToDir(Nodes):
    dic = {}
    for node in Nodes:
        dic.setdefault(node.Archive,[]).append(node)
    return dic

def _ListTagsToDir(Nodes):
    dic = {}
    for node in Nodes:
        for tag in node.Tags:
            dic.setdefault(tag,[]).append(node)
    return dic

def _compare(node1,node2):
    return cmp(node2.TimeStamp,node1.TimeStamp)


def page(Nodes=None):
    ''' rebuild page '''
    if Nodes == None:
        Nodes = _getNodes()
    archive()
    tags()
    _renderToPage(Nodes)


def archive():
    '''build archive page'''
    ## collect basic elements
    ## like Nodes,config and template
    Nodes = _getNodes() 
    config = _readConfig()
    site = Site(config)
    path = os.path.join(config["MAIN_PATH"],'themes',config["THEME_DIR"])
    env = Environment(loader=FileSystemLoader(os.path.join(path,'templates')))
    template = env.get_template('archive.html')
    archive_dir = _ListToDir(Nodes)
    ArchiveTitle = config["ARCHIVE_TITLE"]
    html = template.render(ArchiveTitle = ArchiveTitle,Archive = archive_dir,site = site)
    f = codecs.open(os.path.join(config['MAIN_PATH'],config['OUTDIR'],'archive.html'),'w','utf-8')
    f.write(html)
    f.close()

def tags():
    '''build tags page'''
    Nodes = _getNodes() 
    config = _readConfig()
    site = Site(config)
    path = os.path.join(config["MAIN_PATH"],'themes',config["THEME_DIR"])
    env = Environment(loader=FileSystemLoader(os.path.join(path,'templates')))
    template = env.get_template('tags.html')
    tags_dir = _ListTagsToDir(Nodes)
    TagsTitle = config["TAGS_TITLE"]
    html = template.render(TagsTitle = TagsTitle,Tags= tags_dir,site = site)
    f = codecs.open(os.path.join(config['MAIN_PATH'],config['OUTDIR'],'tags.html'),'w','utf-8')
    f.write(html)
    f.close()


def init():
    ''' init your environment.In face,it's only build some necessary dirs '''
    Nodes = []
    config = _readConfig()
    main_path = config['MAIN_PATH']
    outdir = config['OUTDIR']
    backup_dir = config['BACKUP_DIR']
    theme_dir = config['THEME_DIR']
    try:
        os.mkdir(main_path)
    except OSError:
        print u'\n检测已存在目录树，删掉它么?(yes/no)'
        a = raw_input()
        if a == 'yes':
            shutil.rmtree(main_path)
            os.mkdir(main_path)
    try:
        shutil.copytree('themes',os.path.join(main_path,'themes'))
    except OSError:
        shutil.rmtree(os.path.join(main_path,'themes'))
        shutil.copytree('themes',os.path.join(main_path,'themes'))
    try:
        os.mkdir(os.path.join(main_path,outdir))
    except OSError:
        pass
    try:
        os.mkdir(os.path.join(main_path,outdir,'posts'))
    except OSError:
        pass
    try:
        os.mkdir(os.path.join(main_path,backup_dir))
    except OSError:
        pass
    print u'目录结构建立完毕'
    _writeNodes(Nodes)

def _setNode(filename,auto_abstrct=False,max_lenth=1000):
    con = _readConfig()
    m_time = os.path.getmtime(filename)
    ## make sure every line is decode utf-8
    f = codecs.open(filename,'r','utf-8','strict') 
    f_lines = f.readlines()
    ## title = f.readline().replace('\n','').replace('\r','').strip()
    title = f_lines[0].replace('\n','').replace('\r','').strip()
    path = os.path.join(con['OUTDIR'],'posts',title+'.html')
    ## archive = f.readline().split(':')[-1].strip()
    archive = f_lines[1].split(':')[-1].strip()
    ## tags = f.readline().split(':')[-1]
    tags = f_lines[2].split(':')[-1]
    tags = tags.replace(u'，',',').split(',')
    tags = [word.strip() for word in tags]
    ## blank_line = f.readline()
    blank_line = f_lines[3]
    title,archive,tags = _properties_varify(title,archive,tags,blank_line)
    ## abstrct always use content's first 
    ## paragraph.I suppose this is split 
    ## from below by empty line
    ## set auto_abstrct to control the behavior
    ## of getting abstrct.by lenth or by blankline
    if auto_abstrct == True:
        abstrct = f.read(max_lenth)
        f_lines = [line.strip('\n' + '  ' +'\n' for line in abstrct.split('\n'))]
        abstrct = ''.join(f_lines)

        remain_text = f.read()
        f_lines = [line.strip('\n' + '  ' +'\n' for line in remain_text.split('\n'))]
        remain_text = ''.join(f_lines)

        content = '\n'.join([abstrct,remain_text])
    else:
        ##text = f.read()
        ## force break line
        lines = [line.strip('\n') +'  ' + '\n' for line in f_lines[4:]]
        text = ''.join(lines)
        abstrct,content = _paragraphs(text.splitlines(True))
        abstrct_lines = [line.strip('\n') +'  ' + '\n' for line in abstrct]
        content = '\n'.join([abstrct,content])
        if not abstrct:
            abstrct = content

    ## use misaka process markdown
    renderer = BleepRenderer()
    md = m.Markdown(renderer,
            extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
    abstrct = md.render(abstrct)
    content = md.render(content)

    node = Node(timestamp = m_time,title=title,path = path,archive=archive,tags=tags,content=content,abstrct=abstrct)
    f.close()
    return node


def _writeBackup(node,filename,config,mtime=None):
    '''write a backup file'''
    abspath = os.path.abspath(filename)
    dirname = os.path.dirname(abspath)
    backupdir = os.path.join(config['MAIN_PATH'],config['BACKUP_DIR'])

    if dirname != backupdir:
        f = codecs.open(filename,'r','utf-8','strict') 
        sf = codecs.open(os.path.join(backupdir,node.Title),'w','utf-8')
        f.seek(0)
        sf.write(f.read())
        sf.close()
        f.close()

    ## modified the backup file's modified time
    ## mtime is a tuple first arg is acess time
    ## second arg is modified time
    ## a lazy way is set atime and mtime to same
    if mtime != None:
        backupdir = os.path.join(config['MAIN_PATH'],config['BACKUP_DIR'])
        os.utime(os.path.join(backupdir,node.Title),mtime)
    return True

def _nodeToPost(node,filename,config,Nodes,Backup=True,Insert=False):
    if Backup:
        _writeBackup(node,filename,config)

    if Nodes == None:
        Nodes = _getNodes()

        if node.Title not in [o.Title for o in Nodes]: 
            Nodes.append(node)
            Nodes.sort(_compare)
            _renderToHtml(node)
            ## rebulid pages
            page(Nodes)

    
        else:
            print u'\n确定更新 %s ? yes/no: ' % node.Title
            choose = raw_input()
            if choose == 'yes':
                for i,o in enumerate(Nodes):
                    if o.Title == node.Title:
                        del Nodes[i]
                        break
                Nodes.append(node)
                Nodes.sort(_compare)
                _renderToHtml(node)
                page(Nodes)

        _writeNodes(Nodes)            

    else:
        if node.Title not in [o.Title for o in Nodes]: 
            Nodes.append(node)
            _renderToHtml(node)
        else:
            for i,o in enumerate(Nodes):
                if o.Title == node.Title:
                    if node.TimeStamp>o.TimeStamp:
                        del Nodes[i]
                        Nodes.append(node)
                        break
    return Nodes

            
def post(filename,Nodes = None,Backup = True):
    ''' convert markdown file to html,to let the process more clearly,please remember the below rules:
        1. the first line is your article's title
        2. the second line your should written as this:
        archive: python
        or leave it as a empty line
        3. the third line is the tags,like second line,you should written as this:
        tags:python,sanae
        4. please always leave the forth line as a empty line which could help the program varify all you written above are right '''


    con = _readConfig()
    ## a backup
    ## is file in the backup dir?
    ## if it is right,no need backup
    ## else backup
    node = _setNode(filename)
    _nodeToPost(node,filename,con,Nodes = Nodes,Backup = Backup)
    if Nodes == None:
        print u'\n提交完成'
    else:
        print u'\n已提交 %s' % node.Title
    archive()
    tags()
    return Nodes

def show(reverse = False):
    Nodes = _getNodes() 
    if Nodes == []:
        print u'这里空空如也，什么都没有...\n'
        return False
    else:
        print '\n------------------------------'
        if reverse:
            Nodes.reverse()
        for i,o in enumerate(Nodes):
            print u'%5d:  %s' % (i,o.Title)
        return True



def remove(index,Nodes = None ):
    if not Nodes:
        Nodes = _getNodes()
        config = _readConfig()
    try:
        print u'\n真的希望删除 %d: %s ? (yes/no)' % (index,Nodes[index].Title)
        choose = raw_input()
        if choose == 'yes':
            ## delete all relate files
            os.remove(os.path.join(config['MAIN_PATH'],config['BACKUP_DIR'],Nodes[index].Title))
            os.remove(os.path.join(config['MAIN_PATH'],config['OUTDIR'],'posts',Nodes[index].Title+'.html'))
            Nodes.remove(Nodes[index])
            print u'\n已删除'

        _writeNodes(Nodes)
        page(Nodes)
        archive()
        tags()
        return True
    except IndexError:
        print u'\n移除失败，不存在的索引: %d' % index
        print '\n------------------------------'
        print u'\n所有已经提交的文件:'
        show()
        return False


def postAll(dir_name=None):
    ''' clear up Nodes and files.Rebuild all from backupdir '''
    Nodes = _getNodes()
    config = _readConfig()
    outdir = os.path.join(config['MAIN_PATH'],config['OUTDIR'])
    backupdir = os.path.join(config['MAIN_PATH'],config['BACKUP_DIR'])
    ## clear up outdir 
    for root,dirs,files in os.walk(outdir):
        for name in files:
            os.remove(os.path.join(root,name))
    if dir_name == None:
        dir_name = backupdir
        Nodes = []
    for root,dirs,files in os.walk(dir_name):
        for name in files:
            filename = os.path.join(root,name)
            time.sleep(1)
            Nodes = post(filename,Nodes=Nodes)
    Nodes.sort(_compare)
    page(Nodes)
    _writeNodes(Nodes)
    archive()
    tags()
    print u'\n已重提交所有posts，更新成功'


def updateThemes():
    config = _readConfig()
    main_path = config['MAIN_PATH']
    shutil.rmtree(os.path.join(main_path,'themes'))
    shutil.copytree('themes',os.path.join(main_path,'themes'))
    print u'\n更新主题成功'

def _deleteANode(node,Nodes,l_index,r_index):
    remove_index = None
    for i,o in enumerate(Nodes[l_index:r_index]):
        if o.Title == node.Title:
            index = i
            del Nodes[i]
            break
    return index,Nodes

def insert(filename,index):
    config = _readConfig()
    Nodes = _getNodes()
    ## test index is right
    assert isinstance(index,int)
    assert index >= 0 and index <= len(Nodes)

    ## remove_index = 65535
    # get node
    node = _setNode(filename)
    lenth = len(Nodes)

    ## remove old node
    if node.Title in [o.Title for o in Nodes]: 
        r_index,Nodes = _deleteANode(node,Nodes,None,None)

    if index == lenth:
        index -= 1

    Nodes.insert(index,node)
    ## reset index
    ## you could draw a picture to study the regular
    ## if index > remove_index:
    ##    index -= 1
    lenth = len(Nodes)
    if index == 0:
        try:
            time = Nodes[1].TimeStamp+0.01
        except IndexError:pass
    elif index == lenth-1:
        try:
            time = Nodes[lenth-2].TimeStamp-0.01
        except IndexError:pass
    else:
        time = (Nodes[index-1].TimeStamp+Nodes[index+1].TimeStamp)/2
        
    node.setTimestamp(time)
    Nodes[index].setTimestamp(time)

    _renderToHtml(node)
    _writeBackup(node,filename,config,mtime=(time,time))
    Nodes.sort(_compare)
    _writeNodes(Nodes)
    archive()
    tags()
    show()

