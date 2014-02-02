#coding:utf-8
import codecs,os
import datetime

def convert(filename,dirname):
    f = codecs.open(filename,mode = 'r',encoding='utf-8')
    elements = []
    rest = None
    lines = f.readlines()
    f.close()
    for index,line in enumerate(lines):
        if not line == u'\n':
            elements.append(line)
        else:
            rest = lines[index:]
            break
    assert len(elements) == 3
    elements[0] = '# '+elements[0]
    elements[1] = '- archive:'+elements[1]
    elements[2] = '- tags:'+elements[2]
    timestamp = os.path.getctime(filename)
    time = datetime.datetime.fromtimestamp(timestamp)
    time = time.strftime('%Y-%m-%d:%H')
    date = '- date:'+time+'\n'
    elements.append(date)
    #elements.append('\n')
    elements = elements+rest
    content = ''.join(elements)
    basepath = os.path.basename(filename)
    fw = codecs.open(os.path.join(dirname,basepath),mode='w',encoding='utf-8')
    fw.write(content)
    fw.close()

def convertDir(source,target):
    for root,dirs,files in os.walk(source):
        for name in files:
            convert(os.path.join(root,name),target)
    print 'finished'

convertDir('/home/aprocysanae/Dropbox/oldPosts/blog','miko')
