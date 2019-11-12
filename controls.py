"""TO START PROGRAM ENTER SETTINGS AND RUN THIS FILE"""

'''following variables are user controls'''
import analysis
import fetchdata
import scraping
import graphdata

subredditname = "politics"
posttimeframe = "month"
'''number of post that are search for the searchterm. Final number of post will be fewer'''
numberofposts = 6
replacelimit = 5
searchterm = " "
cut = 'N'
cutlength = 1
cutafter = "Y"

comsort = "best"

sortbytime = "Y"
aggregate = 'N'

posneg = ("pos", "neg")
sorts = ("best", "top", "controversial", "new")


def main():
    gatherdata = input("Hello user. Would you like to scrape data?\n'Y'/'N'\n->")
    if gatherdata == "Y":

        '''Make a batch of samples'''
        samples = list()
        ssize = 0
        makesampleset = input("would you like to make a sample set? 'Y/N'")
        if makesampleset == 'Y':
            while ssize != None:
                ssize = input(("Next sample size: 'enter to stop adding'"))
                if ssize == '':
                    break
                samples.append(int(ssize))

            count = 0
            for ssize in samples:
                print("Now processing sample size:", ssize)
                postinfolist = scraping.main(sorts, sortbytime, cut, searchterm, aggregate, replacelimit, subredditname,
                                             posttimeframe, ssize, cutlength)
                count += 1
                if count == len(samples):
                    quit()

        print("-> Scraping enitiated")
        ''''pass settings to scraper'''
        postinfolist = scraping.main(sorts, sortbytime, cut, searchterm, aggregate, replacelimit, subredditname,
                                     posttimeframe, numberofposts, cutlength)
        analyscurrent = input("Would you like to analyse this data?\n'Y'/'N'\n->")
        if analyscurrent == 'Y':
            print("->Analysing current data...")
            splitforgraph, keylist = analysis.prepinfovisual(postinfolist)
            print("->Done analysing current data...")
            # print("\n\n\n\n\nend", splitforgraph)
            graph = input("Would you like to graph this data: 'Y/N'")
            if graph == 'Y':
                graphdata.main(splitforgraph, keylist)


    else:
        analyse = input("Would you like to analyse a dataset?\n'Y'/'N'\n->")
        if analyse == 'Y':
            print("-> Fetching data...")
            postinfolist = fetchdata.main(r"C:\Users\BenE\Desktop\Python\Projects\reddit project\datasets",
                                          "loaddataset")
            print("->Done fetching...")

            print("->Analysing data...")
            splitforgraph, keylist = analysis.prepinfovisual(postinfolist)
            print("->Done analysing data...")

            graph = input("Would you like to graph this data: 'Y/N'")
            if graph == 'Y':
                graphdata.main(splitforgraph, keylist)

        else:
            graph = input("Would you like to graph some data: 'Y/N'")
            if graph == 'Y':
                splitforgraph, keylist = fetchdata.main(
                    r"C:\Users\BenE\Desktop\Python\Projects\reddit project\cutdatasets", "loadgraphdata")
                graphdata.main(splitforgraph, keylist)

    exit()


main()
