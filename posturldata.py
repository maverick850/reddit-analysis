# -*- coding: utf-8 -*-

import re


def main(postbyweek):
    urldict = dict()
    #    counter = 0
    for week in postbyweek:
        for post in week:
            url = post[4]

            '''cut site name out of url'''
            #            print(url)
            #            print('\n',url[0:20])
            if 'www' in url[0:20]:
                cuturl = str(re.findall('www.(.+?)/', url))
            else:
                cuturl = str(re.findall('https://(.+?)/', url))
            #            print(cuturl)
            post[4] = dict({str(cuturl): 1})

            '''Make dictionary of site linkage over time'''
            if cuturl not in urldict.keys():
                urldict[cuturl] = urldict.get(cuturl, 0) + 1
            else:
                urldict[cuturl] += 1
    print(urldict)




    #    for item in urldict.items():
    #        print(item)

    return postbyweek, urldict
