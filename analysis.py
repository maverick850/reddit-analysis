# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 19:03:37 2019

@author: BenE
"""
'''this loads the settings that are used for graphing'''

import posturldata
import os
import ast
from itertools import groupby
import formatdata

def loadsettings():
    print("Select file:")

    '''Path where datasets are stored'''
    path = r"C:\Users\BenE\Desktop\Python\Projects\reddit project\visualsetttings"

    '''Gets all the .txt files from path'''
    datafiles = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                datafiles.append(os.path.join(r, file))
    filenames = list()
    ''''Cuts filename'''
    for f in datafiles:
        filenames.append(f.replace(r"C:\Users\BenE\Desktop\Python\Projects\reddit project\visualsetttings", ''))
    #        print(filenames)

    '''Print a list of files to select from'''
    count = 0
    for fname in filenames:
        print('(', count, ')', fname)
        count += 1
    '''select file'''
    filenumber = int(input("Select file number:"))
    file = datafiles[filenumber]

    '''extract key from txt'''
    fh = open(file)
    keylist = fh.readlines()
    #    print(type(keylist))

    for i in keylist:
        print(i)
        # keylist = list(i)
        # print(type(i))
        keylist = ast.literal_eval(i)

    return keylist


def getkeys():
    choice = int(input(print("(1)Load settings\n(2)make new settings")))
    if choice == 1:
        keylist = loadsettings()
        print("loadedsettings")
    elif choice == 2:
        print("makesettings")
        '''configure settings'''
        posneg = "pos", "neg"
        sorts = "best", "top", "controversial", "new"
        postdata = "Date", "PostID", "Title", "username", "URL"

        '''following variables are user controls'''
        postdataindex = (0, 1, 2, 3, 4,)
        sortsindex = (6, 12, 18, 24)

        sortcomtotindex = (5, 11, 17, 24)
        posindex = (7, 9), (13, 15), (19, 21), (25, 27)
        negindex = (8, 10), (14, 16), (20, 22), (26, 28)
        # addablekeys = (10,11,14,15,16,17,20,21,22,23,26,27,28,29)

        keylist = list()
        filename = str()

        '''Get settings from user'''
        for i in range(len(postdata)):
            choice = str(input(print("would you like include", postdata[i], "?")))
            print(choice)
            if choice == 'y':
                keylist.append(postdataindex[i])
                filename += postdata[i]
                print(keylist)
        '''If you include sort -> ask if you want summary data -> '''
        for i in range(len(sorts)):

            choice = str(input(print("Include sort by:", sorts[i], "?")))
            if choice == 'y':
                keylist.append(sortsindex[i])
                filename += sorts[i]
                print(keylist)

                choice = str(input(print("Include summary data for this sort type?:", sorts[i], "?")))
                if choice == 'y':
                    keylist.append(sortcomtotindex[i])
                    print(keylist)

                choice = str(input(print("Include positive info for:", sorts[i], "?")))
                if choice == 'y':
                    for x in posindex[i]:
                        keylist.append(x)
                    filename += "pos"
                    print(keylist)

                choice = str(input(print("Include negative info for:", sorts[i], "?")))
                if choice == 'y':
                    for x in negindex[i]:
                        keylist.append(x)
                        filename += "neg"
        print(keylist)
        keylist.sort()

        '''set filename and save'''
        choice = str(input(print("Use:", "'", filename, "'", "as filename?")))
        if choice != 'y':
            filename = str(input("Name the settings file:"))

        filename = r"C:\Users\BenE\Desktop\Python\Projects\reddit project\visualsetttings\\" + filename + ".txt"
        fh = open(filename, 'w+')
        fh.write(str(keylist))

    return keylist


'''Takes the list of posts and formats by week for bar graphs'''


def splitpostsbyweek(postlist):
    weeks = list()
    postbyweek = list()
    templist = list()

    for x in range(len(postlist)):
        weeks.append(postlist[x][0][1])
    print('###', weeks)
    weekkey = list()
    weekkey = ([len(list(group)) for key, group in groupby(weeks)])

    postindex = 0

    '''iterates through number of seuential weeks, splits the weeklist into weeks'''
    for i in weekkey:
        for x in range(i):
            templist.append(postlist[postindex])
            postindex += 1
        postbyweek.append(templist)
        templist = list()

    return postbyweek


def savedata(splitforgraph):
    '''save file'''
    fileid = str(input("Enter a file name:"))
    '''write results to file'''
    filename = str(r"C:\Users\BenE\Desktop\Python\Projects\reddit project\cutdatasets\\" + fileid + ".txt")
    fh = open(filename, 'w+')
    fh.write(str(splitforgraph))
    print("File saved as:", fileid)
    fh.close()


'''main function'''


def prepinfovisual(postinfolist):
    keylist = getkeys()

    print(len(postinfolist))

    weeks = list()
    templist = list()

    postinfolist = splitpostsbyweek(postinfolist)
    postbyweek = postinfolist
    print('___RAW DATA___', postinfolist, '\n\n')

    addablekeys = (4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 25, 26, 27, 28)
    '''Cuts url of linked sites'''
    postbyweek, urldict = posturldata.main(postbyweek)

    '''make a list of keys that can be added'''
    keystoadd = list()
    for key in keylist:
        if key in addablekeys:
            keystoadd.append(key)

    for key in keystoadd:
        print("processing key:", key)

        '''iterate through weeks'''
        for week in postbyweek:
            if len(week) != 0:
                '''add the dictionaries of each week'''
                for post in range(len(week)):
                    if post != 0:
                        for k, v in week[post][key].items():
                            if k in week[0][key].keys():
                                week[0][key][k] += v
                            else:
                                print("item not in dictionary", k, v)
                                week[0][key][k] = week[0][key].get(k, v)

    '''Cuts down lists of words'''
    wordlistkeys = (9, 10, 15, 16, 21, 22, 27, 28)
    cut = 'Y'
    cutlength = 100
    for week in postbyweek:
        for index in wordlistkeys:

            week[0][index] = formatdata.wordsorter(week[0][index], cut, cutlength)

    ''' ADD HERE? keys for finding the average number of coments per sort type per week'''

    '''This takes the summed data and filters results'''
    selection = list()
    splitforgraph = list()

    for week in postbyweek:
        for index in keylist:
            x = week[0]
            selection.append(x[index])
        splitforgraph.append(selection)
        selection = list()

    for item in splitforgraph:
        print(item)

    choice = input("\nWould you like to save the data? 'Y/N'")
    if choice == "Y":
        savedata(splitforgraph)

    return splitforgraph,keylist
