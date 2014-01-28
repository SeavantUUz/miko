#coding:utf-8
__all__ = ['Pagination']

class Pagination(object):
    def __init__(self,items,per_page):
        self.total_items = items
        self.page = 0
        self.per_page = per_page

    @property
    def pages(self):
        return int((self.total - 1) / self.per_page)+1
    
    @property
    def total(self):
        return len(self.total_items)
    
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
        self.page += 1
        start = (self.page-1) * self.per_page
        end = self.page * self.per_page
        return self.total_items[start:end]
