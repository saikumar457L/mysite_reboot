from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
    title = "Mushrooms"
    link = "/blog/"
    description = "New posts of Mushrooms"

    def items (self):
        return Post.published.all()[:5]

    def item (self):
        return item.title

    def item_description(self,item):
        return truncatewords(item.body,30)
