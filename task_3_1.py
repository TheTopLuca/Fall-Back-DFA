import argparse

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)



class State :
    def __init__(self,name):
        self.name = name
        self.transitions = dict()
        self.states = None
        self.isFinalState = False
        self.regexLabel = ""


def findState(name , array):
    for state in array:
        if state.name == name:
            return state
    return None


class DFA :
    def __init__(self):
        self.states = []
        self.startState = None
        self.acceptState = None
        self.alphabet = None
        self.regexActions = dict()







if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")

    args = parser.parse_args()


    output_file = open("task_3_1_result.txt","w+")

    with open(args.dfa_file,"r")as file :
        currentDFA = DFA()
        currentDFA.states = []
        currentDFA.alphabet = []
        currentDFA.acceptState = []
        regexActions = []
        stateRegex = []
        lineNumber = 1
        transitions = []

        for line1 in file:
            lines = line1.splitlines()
            #lines is an array containing each line
            for line in lines :
                elements = line.split(",")
                #elements is an array containing the elements of each line after splitting on the comma
                if(lineNumber==1):
                    for element in elements:
                        state = State(element)
                        currentDFA.states.append(state)
                if(lineNumber==2):
                    for element in elements:
                        currentDFA.alphabet.append(element)
                if(lineNumber==3):
                    for element in elements:
                        stateName = element
                        for state in currentDFA.states:
                            if state.name == stateName:
                                currentDFA.startState=state
                if(lineNumber==4):
                    for element in elements:
                        stateName = element
                        currentState = findState(stateName,currentDFA.states)
                        currentState.isFinalState = True
                        for state in currentDFA.states:
                            if state.name == stateName:
                                currentDFA.acceptState.append(state)
                if(lineNumber==5):
                    length = len(line)
                    i = 0
                    while(i<length-1):
                        field = ""
                        if(line[i]=="("):
                          j = i+1
                          while not(line[j]==")"):
                               field = field + line[j]
                               j=j+1
                          i=j
                          transitions.append(field)
                        field = ""
                        i+=1


                if(lineNumber==6):
                    length = len(line)
                    i = 0
                    while(i<length-1):
                        field = ""
                        if(line[i]=="("):
                          j = i+1
                          while not(line[j]==")"):
                               field = field + line[j]
                               j=j+1
                          i=j
                          stateRegex.append(field)
                        field = ""
                        i+=1

                if(lineNumber==7):
                    length = len(line)
                    i = 0
                    while(i<length-1):
                        field = ""
                        if(line[i]=="("):
                          j = i+1
                          while not(line[j]==")"):
                               field = field + line[j]
                               j=j+1
                          i=j
                          regexActions.append(field)
                        field = ""
                        i+=1

                lineNumber+=1
            #print(currentDFA.states)
        for transition in transitions:
            arr = transition.split(",")
            fromState = findState(arr[0],currentDFA.states)
            toState = findState(arr[2],currentDFA.states)
            fromState.transitions.update({arr[1]:toState})
        for action in stateRegex:
            arr = action.split(",")
            fromState = findState(arr[0],currentDFA.states)
            fromState.regexLabel = arr[1]
        for regex in regexActions:
            arr = regex.split(",")
            currentDFA.regexActions.update({arr[0]:arr[1]})

       # for state in currentDFA.states:
            #print(state.regexLabel)
        #print(currentDFA.regexActions)


        inputText = ""
        with open(args.input_file,"r")as file1 :
            for line in file1:
                input = line.splitlines()
                for textField in input:
                    inputText = textField
            #print(inputText)

        stack = Stack()
        stack.push(currentDFA.startState)
        maxLeft = -1
        left = -1
        right = 0
        length = len(inputText)
        #Loop to Popuplate the stack
        while(left<=right):
          while(left<length-1):
           # print("adding states")
            currentState = stack.peek()
            left+=1
            maxLeft = left
            if(left<length):
               character = inputText[left]
               nextState = currentState.transitions[character]
               maxState = nextState
               stack.push(nextState)
        #Loop to backtrack the Stack
          while not (stack.isEmpty()):
            #print("Stack is stil not  Empty")
            currentState = stack.pop()
            print(currentState.name)
            if(currentState.isFinalState):
                regexLabel = currentState.regexLabel
                for label in currentDFA.regexActions:
                    if(regexLabel==label):
                        #print(currentDFA.regexActions[label])
                        print(inputText[right:left+1])
                        output_file.write(inputText[right:left+1]+"," + currentDFA.regexActions[label] +"\n")
                        break

                break
            else:
                left = left-1
          if(stack.isEmpty()):
            #print(currentDFA.regexActions[currentDFA.startState.regexLabel])
            string = inputText[right:maxLeft+1]
            print(string)
            output_file.write(inputText[right:maxLeft+1]+"," + currentDFA.regexActions[maxState.regexLabel])
            break
          else:
           stack = Stack()
           print("Right has Moved")
           right = left+1
           if(right<length):
              stack.push(currentDFA.startState)
           else:
               break






        #print(regexActions)
       # print(stateAction)






