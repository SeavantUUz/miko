# coding:utf-8
## each article
## you can also add some other properties
class Node(object):
    def __init__(self,*args,**kwargs):
        try:
            self._title = kwargs['title']
            self._timestamp = kwargs['timestamp']
            self._path = kwargs['path']
            self._tags = kwargs['tags']
            self._content = kwargs['content']
            self._archive = kwargs['archive']
            self._abstrct = kwargs['abstrct']

        except KeyError:
            raise Exception('Ouch! Properties not enough!!\n')
    
    @property
    def Title(self):
        return self._title

    @property
    def TimeStamp(self):
        return self._timestamp

    @property
    def Path(self):
        return self._path

    @property
    def Tags(self):
        return self._tags

    @property
    def Content(self):
        return self._content

    @property
    def Archive(self):
        return self._archive

    @property
    def Abstrct(self):
        return self._abstrct

    def __unicode__(self):
        return self._title

    def __str__(self):
        return unicode(self).encode('utf-8')
