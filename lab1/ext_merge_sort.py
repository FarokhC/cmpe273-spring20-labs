unsortedFiles = [
    "input/unsorted_1.txt",
    "input/unsorted_2.txt",
    "input/unsorted_3.txt",
    "input/unsorted_4.txt",
    "input/unsorted_5.txt",
    "input/unsorted_6.txt",
    "input/unsorted_7.txt",
    "input/unsorted_8.txt",
    "input/unsorted_9.txt",
    "input/unsorted_10.txt",
]

sortedFiles = [
    "output/sync/sorted_1.txt",
    "output/sync/sorted_2.txt",
    "output/sync/sorted_3.txt",
    "output/sync/sorted_4.txt",
    "output/sync/sorted_5.txt",
    "output/sync/sorted_6.txt",
    "output/sync/sorted_7.txt",
    "output/sync/sorted_8.txt",
    "output/sync/sorted_9.txt",
    "output/sync/sorted_10.txt",
]

def sort():
    sortFile(unsortedFiles[0], sortedFiles[0])
    sortFile(unsortedFiles[1], sortedFiles[1])
    sortFile(unsortedFiles[2], sortedFiles[2])
    sortFile(unsortedFiles[3], sortedFiles[3])
    sortFile(unsortedFiles[4], sortedFiles[4])
    sortFile(unsortedFiles[5], sortedFiles[5])
    sortFile(unsortedFiles[6], sortedFiles[6])
    sortFile(unsortedFiles[7], sortedFiles[7])
    sortFile(unsortedFiles[8], sortedFiles[8])
    sortFile(unsortedFiles[9], sortedFiles[9])
    mergeSortedFiles(sortedFiles)

def mergeSortedFiles(sortedFiles):
    unmergedData = []
    for fileName in sortedFiles:
        data = getFileLines(fileName)
        unmergedData.extend(data)
    unmergedData.sort()
    writeSortedFileLines("output/sync/sorted.txt", unmergedData)

def sortFile(inputFileName, outputFileName):
    unsortedValues = getFileLines(inputFileName)
    unsortedValues.sort()
    sortedValues = unsortedValues
    writeSortedFileLines(outputFileName, sortedValues)

def getFileLines(fileName):
    file = open(fileName, 'r')
    lines = []
    for line in file:
        lines.append(int(line))
    file.close()
    return lines

def writeSortedFileLines(fileName, lines):
    file = open(fileName, 'w')
    for line in lines:
        file.write(str(line) + "\n")
    file.close()

if __name__ == "__main__":
    sort()