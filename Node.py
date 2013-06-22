# coding:utf-8
import datetime
import os

## Your website's config
class Site(object):
    def __init__(self,conf_dict):
        try:
            self._outDir      = conf_dict['OUTDIR']
            self._path        = conf_dict['MAIN_PATH']
            self._themeDir    = conf_dict['THEME_DIR']
            self._name        = conf_dict['NAME']
            self._author      = conf_dict['AUTHOR']
            self._homepage    = conf_dict['HOMEPAGE']
            self._version     = conf_dict['VERSION']
            self._description = conf_dict['DESCRIPTION']

        except KeyError:
            raise Exception('Ouch! Properties not enough!!\n')

    @property
    def name(self):
        return self._name

    @property
    def author(self):
        return self._author

    @property
    def homepage(self):
        return self._homepage

    @property
    def version(self):
        return self._version

    @property
    def description(self):
        return self._description

    @property
    def themeDir(self):
        return self._themeDir

    @property
    def themePath(self):
        return os.path.join(self._path,self._themeDir)

    @property
    def outDir(self):
        return self._outDir

## each article
## you can also add some other properties
class Node(object):
    def __init__(self,*args,**kwargs):
        try:
            self._title     = kwargs['title']
            self._timestamp = kwargs['timestamp']
            self._path      = kwargs['path']
            self._tags      = kwargs['tags']
            self._content   = kwargs['content']
            self._archive   = kwargs['archive']
            self._abstrct   = kwargs['abstrct']

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

    @property
    ## Formated time
    def Date(self):
        date = datetime.datetime.fromtimestamp(self._timestamp)
        return date.strftime('%Y-%m-%d:%H')


    def __unicode__(self):
        return self._title

    def __str__(self):
        return unicode(self).encode('utf-8')
