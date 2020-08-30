import xlrd #xlrd library to read an excel worksheet where the cards are stored -- can be changed to use odbc to take flash card from db
import random #random to pull a random number for questions

filePath = "Flashcard_Data.xlsx" #this is just a default file can take in user input for file name

workBook = xlrd.open_workbook(filePath)
spreadSheet = workBook.sheet_by_index(0) #get first spreadsheet in excel workbook

#declare all the lists required
flashCards = []
finishedCards = []
definitions = []
correct = []

#display lists for questions
displayQuest = ["0","1","2","3"]

#get the flashcards and definitions from excel sheet declared earlier
for (x) in range(spreadSheet.nrows - 1):
    flashCards.append(spreadSheet.cell_value(x + 1,0))
    definitions.append(spreadSheet.cell_value(x + 1,1))
    correct.append(0)

#this is to confirm the words are being extracted properly
# print(flashCards)
# print(definitions)
# print(correct)

index = 0 #index for the lists

while len(flashCards) > len(finishedCards): #while the flashcards total is greater than flashcards at all

    questionSize = 0 #initialize question size pool for testing soon

    properIndex = index #set the index to this

    #check to see if the definition has been successfully entered 2 times or more
    if correct[properIndex] >= 2:
        index = (index + 1) % len(flashCards)
        continue

    questionList = [] # this will generate the question list

    #generate proper questionsize if > 4 options default to 4. less than 4 do less
    if(len(flashCards) - len(finishedCards) >= 4):
        questionSize = 4
    else:
        questionSize = len(flashCards) - len(finishedCards)

    #last word so just display the proper definition
    if questionSize == 1:
        print("Final Word: Definition is: " + definitions[properIndex])
        print("You have completed the whole flashcard set!")
        break

    print("What is the definition of " + flashCards[properIndex] + "?")
    randomRight = random.randrange(0, questionSize) # this is the correct choice

    #print(randomRight) #this prints the correct choice

    for x in range(0, questionSize): # this will choose random definitions to fill in for every other choice that isn't correct
        correctIndex = properIndex # make sure we know which index we shouldn't be choosing from
        if x != randomRight:
            while (correctIndex == properIndex) or (correctIndex in questionList):
                correctIndex = random.randrange(0, len(definitions))

        questionList.append(correctIndex)
        #print(questionList)
        print(displayQuest[x] + ". " + definitions[correctIndex])

    #get user input to see if its the correct index
    val = input("Enter the number for the correct definition: ")
    #print(val + " vs " + str(randomRight)) #checking the choice vs the user choice
    if val == str(randomRight):
        print("\nCorrect!\n")
        correct[properIndex] = 1 + correct[properIndex] #increment correct count

        if correct[properIndex] >= 2: #check if count is at predetermined amount
            finishedCards.append(flashCards[properIndex])
            print("\nYou completed this definition\n")
            if len(flashCards) == len(finishedCards):
                print("You have completed the whole flashcard set!")
                break
    else: #reset count as choice was wrong
        print("\nIncorrect, restarting your learning for this flashcard\n")
        correct[properIndex] = 0

    #index watch
    if flashCards[-1] == flashCards[properIndex]:
        index = 0
    else:
        index = (index + 1) % len(flashCards)
