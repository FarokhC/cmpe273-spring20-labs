import asyncio

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
    "output/async/sorted_1.txt",
    "output/async/sorted_2.txt",
    "output/async/sorted_3.txt",
    "output/async/sorted_4.txt",
    "output/async/sorted_5.txt",
    "output/async/sorted_6.txt",
    "output/async/sorted_7.txt",
    "output/async/sorted_8.txt",
    "output/async/sorted_9.txt",
    "output/async/sorted_10.txt",
]

async def sort():
    await asyncio.gather(
        sortFile(unsortedFiles[0], sortedFiles[0]),
        sortFile(unsortedFiles[1], sortedFiles[1]),
        sortFile(unsortedFiles[2], sortedFiles[2]),
        sortFile(unsortedFiles[3], sortedFiles[3]),
        sortFile(unsortedFiles[4], sortedFiles[4]),
        sortFile(unsortedFiles[5], sortedFiles[5]),
        sortFile(unsortedFiles[6], sortedFiles[6]),
        sortFile(unsortedFiles[7], sortedFiles[7]),
        sortFile(unsortedFiles[8], sortedFiles[8]),
        sortFile(unsortedFiles[9], sortedFiles[9])
    )
    mergeSortedFiles(sortedFiles)

def mergeSortedFiles(sortedFiles):
    unmergedData = []
    for fileName in sortedFiles:
        data = getFileLines(fileName)
        unmergedData.extend(data)
    unmergedData.sort()
    writeSortedFileLines("output/async/sorted.txt", unmergedData)

async def sortFile(inputFileName, outputFileName):
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
    asyncio.run(sort())