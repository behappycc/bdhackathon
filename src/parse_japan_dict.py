def parseData():
    with open('japan_dict.txt', 'r+') as datafile:
        for line in datafile:
            #newstr = oldstr.replace("M", "")
            line = line.replace('\n', '')
            datafile.write(line + ' ' +str(len(line) + 8) + ' ' +'n' + '\n')

def main():
    parseData()

if __name__ == '__main__':
    main()