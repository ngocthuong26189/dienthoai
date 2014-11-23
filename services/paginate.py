import urllib
from flask import request, url_for


# HTML pattern

PREV = '<li class="arrow {0}" aria-disabled="true"><a href="{1}">&laquo; Previous</a></li>'
NEXT = '<li class="arrow {0}"><a href="{1}">Next &raquo;</a></li>'
PAGE = '<li class="{0}"><a href="{1}">{2}</a></li>'
HELL = '<li class="unavailable"><a href="">&hellip;</a></li>'

class Paginate(object):

    def __init__(self, route_name, count=0, per_page=10):
        self.count = count
        self.per_page = per_page

        self.route_name = route_name
        self.page_count = (count - 1) / per_page + 1 # (10-1)/10+1 = 1 and (11-1)/10+1=2
        self.args = request.args.to_dict()

    @property
    def links(self):
        current_page = self.get_page()
        html = '<ul class="pagination">'
        print current_page
        html += PREV.format('' if current_page > 1 else 'unavailable', self.get_url(current_page-1))
        for page in range(1, self.page_count + 1):
            html += PAGE.format('current' if current_page == page else '', self.get_url(page), page)
        html += NEXT.format('' if current_page < self.page_count else 'unavailable', self.get_url(current_page+1))
        html += '</ul>'
        return html


    def get_page(self):
        page = 1
        try:
            page = int(self.args.get('page', 1))
        except:
            page = 1
        return page

    def get_url(self, page=1):
        url =  url_for(self.route_name) + '?'
        return url + self.to_query(self.args, page)


    def to_query(self, args, page=1):
        args['page'] = page
        return urllib.urlencode(args)



