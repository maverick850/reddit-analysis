import praw
import datetime
import formatdata

'''Filters posts using searchterms'''


def searchfilter(postinfolist, searchterm):
    count = 0
    filteredlist = list()
    print("Searchterm:", searchterm)

    for x in range(len(postinfolist)):
        if searchterm in postinfolist[x][2]:
            filteredlist.append(postinfolist[x])
            count += 1

    return filteredlist


'''Formats the timestamp to be more easily sorted by timeframe'''


def formattime(postinfolist):
    for x in range(len(postinfolist)):
        ts = str(postinfolist[x][0])
        ts = ts[0:10]
        ts = ts.replace('-', '')
        year = ts[0:4]
        month = ts[4:6]
        day = ts[6:8]
        week = (int(month) * 4) + (int(int(day) / 7))
        date = (int(year), week)
        postinfolist[x][0] = date
        '''sort by week'''
    postinfolist.sort(key=lambda x: x[0][1], reverse=True)
    return postinfolist


'''Sorts the post info by list key'''


def sortposts(postinfolist):
    postinfolist.sort(key=lambda x: x[0])
    return postinfolist


def getnegpos(top_level_comments, poswordlist, negwordlist):
    counter = 0
    postotal = 0
    negtotal = 0
    for comment in top_level_comments:
        '''skip automod comment'''
        if counter == 0:
            counter += 1
            continue
        if counter in range(len(top_level_comments)):
            #                print (counter,comment.body)
            counter += 1
            words = comment.body.split()

            '''counts negative words'''
            for word in words:
                if word in negwords:
                    negwordlist[word] = negwordlist.get(word, 0) + 1
                    negtotal += 1
                if word in poswords:
                    postotal += 1
                    poswordlist[word] = poswordlist.get(word, 0) + 1
            #                print (poswordlist)
            continue
    return poswordlist, negwordlist, postotal, negtotal


'''filters [removed], [deleted], and duplicate comments'''


def filterdupecomments(top_level_comments):
    uniquelist = list()
    duplicates = 0
    for x in top_level_comments:
        commentbody = x.body
        if commentbody not in uniquelist:
            #            print(commentbody)
            uniquelist.append(commentbody)
            continue
        elif commentbody == "[deleted]":
            continue
        elif commentbody == "[removed]":
            #            removed +=1
            continue
        else:
            duplicates += 1

    print("DUPLICATES:", duplicates)


'''
open and parse word lists
'''
negwords = list()
poswords = list()
nfh = open(r"C:\Users\BenE\Desktop\Python\text samples\negative words.txt")
pfh = open(r"C:\Users\BenE\Desktop\Python\text samples\positive words.txt")
for line in nfh:
    negwords += line.split()
for line in pfh:
    poswords += line.split()

'''
Authenticate
'''
reddit = praw.Reddit(client_id='uZLXar1yp-vTfA',
                     client_secret='NjXgI9lWBjgF69PLdSpSOellPEk',
                     password='111111',
                     user_agent='rambt script',
                     username='rambt')
'''
NEED REFRESH TOKEN HERE
'''

'''following variables are user controls'''
# print(reddit.user.me())


infofilepath = r"C:\Users\BenE\Desktop\Python\Projects\reddit comment analysis\postinfolist.txt"


# infoindex = 0
def main(sorts, sortbytime, cut, searchterm, aggregate, replacelimit, subredditname, posttimeframe, numberofposts,cutlength):
    merge = dict()
    negwordlist = dict()
    poswordlist = dict()
    totalcomments = dict()
    postinfolist = list()
    '''makes list of post IDs and info'''
    for submission in reddit.subreddit(subredditname).top(posttimeframe, limit=numberofposts):
        time = submission.created
        posttime = (datetime.datetime.fromtimestamp(time))
        currentpost = str(posttime), str(submission.id), str(submission.title), str(submission.author), str(
            submission.url)
        currentpost = list(currentpost)
        postinfolist.append(currentpost)

    '''filter search results by term'''
    postinfolist = searchfilter(postinfolist, searchterm)
    print("Number of search results for",searchterm,":",len(postinfolist))
    print("this is", 100*(numberofposts/len(postinfolist)), "% of the total results(" ,numberofposts, ")")

    '''Formats timestamps'''
    if sortbytime == "Y":
        postinfolist = formattime(postinfolist)
        infoindex = 0
        postinfolist = sortposts(postinfolist)

    x = 0
    numofcomments = 0

    if len(postinfolist) == 0:
        print("NO RESULTS")
        exit()

    '''iterate sort'''
    for sort in range(len(sorts)):
        postotal = 0
        negtotal = 0
        numofcomments = 0
        cursort = sorts[sort]

        '''iterate posts'''
        for postinfo in postinfolist:

            '''get submission'''
            submission = reddit.submission(id=postinfo[1])

            '''set comment sort'''
            submission.comment_sort = cursort
            submission.comments.replace_more(limit=replacelimit)
            top_level_comments = list(submission.comments)
            if x == 0:
                print("Sort type:", submission.comment_sort.upper(), '|', len(top_level_comments), "comments processed")
                '''get total comments processed per post'''
                numofcomments += len(top_level_comments)
            """Iterate comment sort and extract pos neg"""
            poswordlist, negwordlist, postotal, negtotal = getnegpos(top_level_comments, negwordlist, poswordlist)

            '''sort words by commonality'''
            negwordlist1 = formatdata.wordsorter(negwordlist, cut, cutlength)
            poswordlist1 = formatdata.wordsorter(poswordlist, cut, cutlength)

            '''Number of pos neg'''
            print("postotal", postotal, "negtotal", negtotal)

            postinfo.append({"num of comments": numofcomments})
            postinfo.append({"sort": cursort})
            postinfo.append({"pos": postotal})
            postinfo.append({"neg": negtotal})
            postinfo.append(poswordlist1)
            postinfo.append(negwordlist1)

            merge = formatdata.dictmerger(poswordlist, "neg", cursort, merge)
            merge = formatdata.dictmerger(negwordlist, "pos", cursort, merge)
            if aggregate == 'Y':
                totalcomments = formatdata.countcomments("neg", cursort, totalcomments, numofcomments)
                totalcomments = formatdata.countcomments("pos", cursort, totalcomments, numofcomments)
            '''reset the wordlists'''
            negwordlist = dict()
            poswordlist = dict()

    '''shows index of each info'''
    count = 0
    for post in postinfolist:
        for item in post:
            print('\n',count, item)
            count += 1
        count = 0

    '''if selected: takes all sampled posts and aggregates them'''
    if aggregate == 'Y':
        totalwords = 0
        for x, y in merge.items():
            for v in y.values():
                totalwords += v
            print("\nSUMMARY:\nSort:", x, "\nNumber of unique words:", len(y), "\nTotal Words used:", totalwords)
            print("Total comments processed", totalcomments[x])
            print("Word variance =", totalwords / len(y))
            print("words per post =", totalwords / totalcomments[x])
            complexity = formatdata.wordcomplexity(totalwords, y)
            print("Average complexity:", complexity)
            totalwords = 0

    numberofposts = str(numberofposts)
    replacelimit = str(replacelimit)

    fileid = str(subredditname + posttimeframe + "searchterm=" + searchterm + "-numpost=" + str(numberofposts) + replacelimit)
    print("File saved as:",fileid)
    '''write results to file'''
    filename = str(r"C:\Users\BenE\Desktop\Python\Projects\reddit project\datasets\\" + fileid + ".txt")
    fh = open(filename, 'w+')
    fh.write(str(postinfolist))
    fh.close()

    return postinfolist
