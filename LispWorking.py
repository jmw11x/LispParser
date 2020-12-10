from LispParser import parser
import copy

'for user input'
def read_input():
  result = ''
  while True:
    data = input('lisp: ').strip()
    if ';' in data:
      i = data.index(';')
      result += data[0:i+1]
      break
    else:
      result += data + ' '
  return result

'''
gets valid getIdentifiers and constants from the list
expression for output....for ex....
[[[num, 3], [num 33], ...]], ....[nthDigit]] --> (3, 33, ....nthDigit)
'''
def getIdentifiers(ast,temp):
    if ast ==[]:
        return ast
    elif type(ast[0]) == float or type(ast) == float or type(ast)==str:
        return ast
    elif ast == 'lists empty sorry!':
        return ast
    elif ast[0][0] in ['+','/','*','-']:
        s = evalNum(ast[0], 'good',{})
        temp+=[s]
        if ast[1]== []:
            return temp
        else:
            return getIdentifiers(ast[1:len(ast)],temp)
    elif [] in ast:
        return temp + [ast[0][1]]
    elif len(ast) == 1:
        return getIdentifiers(ast[0], temp)
    else:
        temp+=[ast[0][1]]
        return getIdentifiers(ast[1:len(ast)],temp)

'''
    Error check message between left and right recursion
    arethmitic calls in evalNum.

    Raises error for car of an empty list.
'''
def errorCheck(left, right):
    message='good'
    if left == 'CAR of empty list' or right =='CAR of empty list':
        raise Exception ('Cannot evaluate CAR of EMPTY List!')
    return message

''''Adds decalred variables in let block to a dictionary evaluates each
    variable defined in place by calling evalNum if necessary.
'''
def updateDict(ast, dict):
    if ast == []:
        return dict
    else:
        if ast[0][1][0] in ['*', '-', '+', '/', 'CAR']:
            dict.update({ast[0][0] : evalNum(ast[0][1], 'good',dict)})
        else:
            dict.update({ast[0][0] : ast[0][1][1]})
        return updateDict(ast[1:], dict)
'''
----->Helper for sub. Temp returns the transformed list as it would be
      at the end of the abstract syntax tree data made by the parser.
'''
def replaceVars(ast, dict, temp):
    if type(ast) == 'float':
        return ast
    if ast == []:
        return temp
    elif ast[0][0] in ['+', '-', '*', '/']:
        replaceVars(ast[0][1:], dict, temp)
        if type(temp)==str:
            return temp
        elif ast[0][0] == 'CAR':
            head = evalNum(ast[0], 'good',dict)
            eval = evalNum([head]+temp,'good',dict)
            return temp + ['num' ,dict.get(head)]
        elif len(temp) > 2:
            temp = [temp[0]] + [[ast[0][0]] + temp[1:]]
            eval = evalNum([ast[0][0]]+temp, 'good',dict)
            return eval
        else:
            eval = evalNum([ast[0][0]]+temp+[ast[0][2]], 'good',dict)
            temp = [['num', eval]] + temp[1:]
            return temp + ast[1:]
    elif ast[0][0] == 'CAR':
        head = evalNum(ast[0], 'good',dict)
        eval = evalNum([head]+temp,'good',dict)
        return temp + [['num',dict.get(head)]]
    else:
        #check dictionary for errors or add and store new values
        if ast[0][0]=='var' and ast[0][1] not in dict:
            raise Exception('EVALUATION ERROR: Uninstantiated Variable ' + str(ast[0][1]))
        elif ast[0][1] in dict:
            if type(dict.get(ast[0][1])) == list:
                #NEED TO REPLACE VARIABLES
                dictList=dict.get(ast[0][1])
                old
                for i in dictList:
                    if i[0] in dict:
                        dict.update({i[0] : i[1][1]})
            temp += [['num' ,dict.get(ast[0][1])]]
            return replaceVars(ast[1:], dict, temp)

'''
Substitute defined identifiers in let exp outside the let block
to be interpreted. If an identifier is not defined, there
will be an error raised.
'''
def sub(ast, dict, error):
    if ast == []:
        return dict
    elif type(ast) == float:
        return ast
    else:
        if ast[0][0] in ['*','/','-','+']:
            # replace vars and return them
            update = replaceVars(ast[0][1:], dict, [])
            if type(update) == float:
                return update
            elif update[1][0] in ['*','/','-','+', 'CAR']:
                tempUp=replaceVars(update[1:], dict,[])
                update = [ast[0][0]] + [update[0]] + tempUp
                s = evalNum(update, 'good',dict)
                return sub(s,dict,error)
            else:
                s = evalNum([ast[0][0]]+update, 'good',dict)
                return sub(s,dict,error)
        else:
            if 'LET' in ast[0]:
                set = sub(ast[0][1:],dict,'good')
                return set
            dict = updateDict(ast[0] , dict)
            return sub(ast[1:], dict, error)

'''
Processes ast of list expressions executing cdr,
cons, let, and arethmitic operations inside
the list expressions scope, as needed.
Raises exception for Uninstantiated variables
'''
def evalList(ast,message,dict):
    if ast == []:
        return ast
    elif ast[0][0] == 'num':
        if message == 'car':
            return ast
        elif ast[1]==[]:
            return ast
        if ast[1][0] == 'CDR':
            head =evalList(ast[1], message,dict)
            return [ast[0]]+head
        else:
            return ast
    elif ast[0][0] == 'var':
        if ast[0][1] not in dict:
            raise Exception('EVALUATION ERROR: Uninstantiated Variable ' +ast[0][1])
        return ast
    elif ast[0] == 'CDR':
        head = []
        if ast[1] == []:
            message = 'bad'
        else:
            head = evalList(ast[1], message,dict)
        '''
            Several checks need to be made for let expression
            execution.
        '''
        if head==[] or ast[1]==[]:
            message='bad'
        let = []
        if [] not in head and head !=[]:
            let = head[1][1]
        if let == []:
            let = [let]
        if 'LET' in let[0]:
            eval = evalList(let[0], message,dict)
            return [head[1][0] + [ eval]]
        if message == 'bad':
            raise Exception('CDR of an empty list error!')
        else:
            return head[1]
    elif ast[0] == 'CONS':
        next = evalNum(ast[1][0], message,dict)
        edit = [['num',next]] + [ast[1][1:]]
        return evalList(edit,message,dict)
    elif ast[0] == 'LET' or 'LET' in ast[1][0]:
        set = sub(ast[1:],{},message)
        return set

'''
processes ast of lisp expressions processing let, car,
and arethmitic operations as needed. Raises exception for
Uninstantiated variables.
'''
def evalNum(ast, message,dict):
    if type(ast) == float:
        return ast
    elif ast[0] == 'LET':
        set = sub(ast[1:],dict,message)
        return set
    elif ast[0] == 'num':
        return ast[1]
    elif ast[0] == 'var':
        if ast[1] not in dict:
            raise Exception('EVALUATION ERROR: Uninstantiated Variable ' +ast[1])
        return ast[1]
    elif ast[0] == '+':
        left = evalNum(ast[1], message,dict)
        right = evalNum(ast[2],message,dict)
        message = errorCheck(left,right)
        return left+ right
    elif ast[0] == '-':
        left = evalNum(ast[1],message,dict)
        right = evalNum(ast[2],message,dict)
        message = errorCheck(left, right)
        return left - right
    elif ast[0] == '*':
        left = evalNum(ast[1],message,dict)
        right = evalNum(ast[2],message,dict)
        message = errorCheck(left,right)
        return left * right
    elif ast[0] == '/':
        left = evalNum(ast[1],message,dict)
        right = evalNum(ast[2],message,dict)
        message = errorCheck(left,right)
        if right == 0:
            return 'EVALUATION ERROR: Divide by 0!'
        else:
            return left / right
    elif ast[0] == 'CAR':
        s=evalList(ast[1], 'car',dict)
        if s ==[] or s =='lists empty sorry!':
            message = 'bad'
        return 'Cannot evaluate CAR of empty list' if message == 'bad' else s[0][1]

def main():
  while True:
    data = read_input()
    if data == 'exit;':
      break
    try:
      ast = parser.parse(data)
      if ast[0] == 'list':
          expression = evalList(ast[1],'good',{})
          print(
              'CDR of empty list Error!' if expression == 'lists empty sorry!'
               else tuple( getIdentifiers(expression,[]) )
          )
      else:
          print(evalNum(ast[1],'good',{}))
    except Exception as inst:
      print(inst.args[0])
      continue

main()
