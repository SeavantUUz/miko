#coding:utf-8
import os,calendar,datetime

class Node(object):
    def __init__(self,**kwargs):
        try:
            self.title     = kwargs['title']
            self.abstrct   = kwargs['abstrct']
            self.content   = kwargs['content']
            self.tags      = kwargs['tags']
            self.archive   = kwargs['archive']
            self.path      = kwargs['path']
        except KeyError:
            raise Exception('Ouch! Properties not enough!!\n')
        if kwargs.get('date'):
            date = kwargs.get('date').strip()
            d = datetime.datetime(date,'%Y-%m-%d:%H')
            self.timestamp = long(calendar.timegm(d.utctimetuple()))
        else:
            self.timestamp = long(os.path.getctime(self.path))
            
    @property
    def date(self):
        date = datetime.datetime.fromtimestamp(self.timestamp)
        return date.strftime('%Y-%m-%d:%H')

    @property
    def feed_data(self):
        date = datetime.datetime.fromtimestamp(self.timestamp)
        d = date.strftime('%Y-%m-%dT%H:%M:%S')
        return d+'+00:00'

    def __lt__(self,other):
        return self.timestamp > other.timestamp

    def __unicode__(self):
        return self.title

    def __str__(self):
        return unicode(self).encode('utf-8')
