import json
import urllib
import urllib2


def query1(terms, size=20):
    root = 'http://webhose.io/search'

    query_string = urllib.quote(terms)

    url = '{root_url}?token={key}&format=json&q={query}&sort=relevancy&size={size}'.format(
        root_url=root,
        key='01fd6583-6c03-484e-9af5-399d8e85e495',
        query=query_string,
        size=size)
    try:

        search_results = []
        print(url)
        resp = urllib2.urlopen(url).read()
        print(resp)
        json_resp = json.loads(resp)

        for post in json_resp['posts']:
            print(post['title'])
            search_results.append({'title': post['title'],
                                   'link': post['url'],
                                   'summary': post['text'][:150]})

    except Exception as error:
        print(error)
    return search_results