import analysis
import ast
import os

def main(path,purpose):

    print("Select file:")


    '''Gets all the .txt files from path'''
    counter = 0
    datafiles = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                counter += 1
                datafiles.append(os.path.join(r, file))
    filenames = list()
    ''''Cuts filename'''
    for f in datafiles:
        filenames.append(f.replace(path, ''))
    #        print(filenames)

    count = 0
    for fname in filenames:
        print('(', count, ')', fname)
        count += 1

    filenumber = int(input("Select file number:"))
    file = datafiles[filenumber]

    fh = open(file)

    if purpose == "loaddataset":
        postinfolist = fh.readlines()
        postinfolist = list(postinfolist)
        for week in postinfolist:
            postinfolist = ast.literal_eval(week)
        return postinfolist

    if purpose == "loadgraphdata":
        splitforgraph = fh.readlines()
        splitforgraph = list(splitforgraph)
        for week in splitforgraph:
            splitforgraph = ast.literal_eval(week)

        keylist = analysis.getkeys()

        return splitforgraph, keylist

