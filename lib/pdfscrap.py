import sys
import pdfplumber

LEFT_FLEXIBILITY = 10  #Tab length is about 15, so 10 is okay for pdf formatting
RIGHT_FLEXIBILITY = 5  #Flexibility to commodate difference in physical character length eg. M vs - or .
TOP_FLEXIBILITY = 30   #End of references is usually followed by a large whitespace.
MIN_WORD_LENGTH = 10

def isPartOfSentence(leftBound, leftLimit, previousRightBound, rightLimit):
    if (int(previousRightBound) < int(rightLimit - RIGHT_FLEXIBILITY)):    #account space difference for - and other characters.
        if (int(leftBound) <= int(leftLimit + LEFT_FLEXIBILITY)):          #This word is part of a new sentence, this works because of the indents at the start
            return False

    return True

def pageListMaker(file, splitPdf, noOfPage, referencePageNo):
    pageList = []
    for x in range(0, int(noOfPage)):
        y = (int(referencePageNo) - 1) + x
        page = file.pages[y]
        if (splitPdf == "y"):
            croppedPage1 = page.crop((0, 0, 0.5 * float(page.width), page.height))
            croppedPage2 = page.crop((0.5 * float(page.width), 0, float(page.width), page.height))
            pageList.append(croppedPage1)
            pageList.append(croppedPage2)
        else:
            pageList.append(page)

    return pageList

#Extracting References
def citationExtractor():
    referenceRegion = False
    referenceList = []
    pageList = []
    filepath = input("Please provide the relative filepath to your PDF file: ")
    with pdfplumber.open(filepath) as pdf:
        referencePageNumber = input("Please indicate the References page number: ")
        numberOfPages = input("Please indicate number of References page(s): ")
        splitPdf = input("Does the article has 2 pages in 1 page? Y/N: ").lower()

        # for page in pdf.pages:
        pageList = pageListMaker(pdf, splitPdf, numberOfPages, referencePageNumber)
        for page in pageList:
            content = page.extract_words(x_tolerance = 1, y_tolerance = 3)   #list of dictionary of word with its attributes
            firstReference = True
            leftLimit = content[0]["x0"]
            rightLimit = content[0]["x1"]
            previousRightBound = 0
            previousTopBound = 0
            reference = ""
            for word in content:
                if ((word["text"].lower() == 'references') and referenceRegion == False):
                    referenceRegion = True
                    continue
                if (referenceRegion == False):
                    continue
                
                if (firstReference == True):  #To use the first reference as the limit as Headers may be designed differently in different documents
                    leftLimit = word["x0"]
                    rightLimit = word["x1"]
                    previousTopBound = word["top"]
                    firstReference = False

                topBound = word["top"]
                if (topBound - previousTopBound > TOP_FLEXIBILITY):
                    break

                leftBound = word["x0"]
                rightBound = word["x1"]
                rightLimit = rightBound if rightLimit <= rightBound else rightLimit    #updating the max limit
                if (isPartOfSentence(leftBound, leftLimit, previousRightBound, rightLimit)):
                    reference = reference + " " + word["text"]
                    previousRightBound = word["x1"]
                    previousTopBound = word["top"]
                else:
                    reference = reference.replace("- ", "")                  #to remove nextline in PDF that splits words eg. TensorF- low due to 2 pages in 1 page
                    referenceList.append(reference) if len(reference) > MIN_WORD_LENGTH else None    #if not part of sentence, append the previous few sentence and 
                    reference = word["text"]
            referenceList.append(reference) if len(reference) > MIN_WORD_LENGTH else None         #for the last line that doesnt have the previous bound to push it  
    pdf.close()

    for x in referenceList:
        print(x)
        print("***")

    return referenceList
