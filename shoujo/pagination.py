#coding:utf-8
__all__ = ['Pagination']

class Pagination(object):
    def __init__(self,items,page,per_page):
        self.items = items
        self.page = page
        self.per_page = per_page

    def iter_pages(self,edge=4):
        if self.page <= edge:
            return range(1,min(self.pages,2 * edge + 1) + 1)
        if self.page + edge > self.pages:
            return range(max(self.pages - 2 * edge , 1),self.pages + 1)
        return range(self.page - edge,min(self.pages,self.page + edge) + 1)

    @property
    def pages(self):
        return int((self.total - 1) / self.per_page)+1
    
    @property
    def total(self):
        return len(self.items)
    
    @property
    def has_prev(self):
        return self.page > 1

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.page + 1

    @property
    def items(self):
        start = (self.page - 1) * self.per_page
        end = self.page * self.per_page
        return self.items[start:end]
