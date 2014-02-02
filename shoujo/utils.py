#coding:utf-8
__all__ = ['sort_nodes','get_nodes','save_nodes','parse','getconfig','update_themes','_nodesdic','_tagsdic','_dontcare']

import pickle,codecs,re,os,shutil
import yaml
from shoujo.node import Node

def _nodesdic(nodes):
    dic = {}
    for node in nodes:
        dic.setdefault(node.archive,[]).append(node)
    return dic

def _tagsdic(nodes):
    dic = {}
    for node in nodes:
        for tag in node.tags:
            dic.setdefault(tag,[]).append(node)
    return dic

def _dontcare(nodes,filename,todict):
    from shoujo.env import env
    configs = getconfig()
    path = os.path.join(configs['app'],configs['out'],filename+'.html')
    template = env.get_template(filename+'.html')
    items = todict(nodes)
    return configs,template,items,path

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
            pickle.dump(nodes,pick)
            pick.close()
        else:
            try:
                os.remove('data.pick')
            except OSError:
                pass
        return nodes
    return wrapper

def getconfig(attr='all'):
    configs = yaml.load(open('config.yaml','r'))
    if attr == 'all':
        return configs
    else:
        return config.get(attr)

def update_themes(func):
    def wrapper(*args,**kwargs):
        ret = func(*args,**kwargs)
        configs = getconfig()
        themesdir = os.path.join(configs['app'],'themes')
        shutil.rmtree(themesdir)
        shutil.copytree('themes',themesdir)
        return ret
    return wrapper

def parse(filename):
    with codecs.open(filename,'r',encoding = 'utf-8') as f:
        lines = f.readlines()
        elements = {}
        patterns = [r'# (.+)\n',r'- archive:(.+)\n',r'- tags:(.+)\n',r'- date:(.+)\n']
        parsers = map(re.compile,patterns)
        atoms = [parser.match(line).group(1) for parser,line in zip(parsers,lines[:4])]

        elements['title'] = atoms[0]
        elements['archive'] = atoms[1]
        elements['tags'] = atoms[2]
        elements['date'] = atoms[3]
        configs = getconfig()
        elements['url'] = os.path.join(configs['out'],'posts',atoms[0]+'.html')
        elements['path'] = filename

        saps = filter(lambda i:lines[i]=='\n',range(len(lines)))
        # first sap saparate infos by abstrct
        # second sap saparate abstrct by content
        # we dont need blank line,so jump one line
        abstrct = lines[saps[0]+1:saps[1]]
        content = lines[saps[1]+1:]
        elements['abstrct'] = '\n'.join(abstrct)

        codeIndex = filter(lambda i:content[i][:3] == '```',range(len(content)))
        codeIndex.insert(0,0)
        codeIndex.append(len(content))
        contentParts = []
        for i in range(len(codeIndex)-1):
            currentIndex = codeIndex[i]
            nextIndex = codeIndex[i+1]
            if i % 2:
                contentPart = ''.join(content[currentIndex:nextIndex])
            else:
                contentPart = '\n'.join(content[currentIndex:nextIndex])
            contentParts.append(contentPart)
        elements['content'] = elements['abstrct']+'\n'+'\n'.join(contentParts)
        return elements

