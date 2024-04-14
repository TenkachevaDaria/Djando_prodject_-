from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector


from goods.models import Product


def q_search(query):
    if query.isdigit() and len(query) <= 2:
        return Product.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    query = SearchQuery(query)
    return Product.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")