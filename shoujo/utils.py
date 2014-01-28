#coding:utf-8
__all__ = ['sort_nodes','get_nodes','save_nodes']

import pickle,codecs,re

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
            pick.dump(nodes)
            pick.close()
        return nodes
    return wrapper

def parse(filename):
    with codecs.open(filename,'r',encoding = 'utf-8') as f:
        lines = f.readlines()
        elements = {}
        patterns = [r'# (.+)\n',r'- archive:(.+)\n',r'- tags:(.+)\n',r'- date:(.+)\n']
        parsers = map(re.compile,patterns)
        atoms = [parser.match(line).group(1) for parser,line in zip(parsers,line[:4])]

        elements['title'] = atoms[0]
        elements['archive'] = atoms[1]
        elements['tags'] = atoms[2].strip().replace(u'，',',').split(',')
        elements['date'] = atoms[3]

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
        elements['content'] = '\n'.join(contentParts)
        return elements

