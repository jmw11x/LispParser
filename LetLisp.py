from LispParser import parser
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

def getIdentifiers(ast, temp):
    if type(ast[0]) == float or type(ast) == float:
        return ast
    elif ast == 'lists empty guy':
        return ast
    elif ast==[]:
        return ast
    elif ast[0][0] in ['+','/','*','-']:
        s = evalNum(ast[0], 'good')
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
'''
def errorCheck(left, right):
    message='good'
    if left == 'CAR of empty list' or right =='CAR of empty list':
        message = 'bad'
    return message

def updateDict(ast, dict):
    if ast == []:
        return dict
    else:
        dict.update({ast[0][0] : ast[0][1][1]})
        return updateDict(ast[1:], dict)

def replaceVars(ast, dict, temp):
    '''
        perhaps Evaluates car, cdr cons expressions here???
    '''
    if ast == []:
        return temp
    elif ast[0][0] in ['+', '-', '*', '/']:
        replaceVars(ast[0][1:], dict, temp)
        eval = evalNum([ast[0][0]]+temp+[ast[0][2]], 'good')
        temp = [['num', eval]] + temp[1:]
        return temp + ast[1:]
    else:
        if ast[0][1] in dict:
            temp += [['num' ,dict.get(ast[0][1])]]
        return replaceVars(ast[1:], dict, temp)


def sub(ast, dict, error):
    if ast == []:
        return dict
    elif type(ast) == float:
        return ast
    else:
        if ast[0][0] in ['*','/','-','+']:
            # replace vars and return them
            update = replaceVars(ast[0][1:], dict, [])
            if update[1][0] in ['*','/','-','+']:
                tempUp=replaceVars(update[1:], dict,[])
                update = [ast[0][0]] + [update[0]] + tempUp
                s = evalNum(update, 'good')
                return sub(s,dict,error)
            elif ast[0][0] in ['CDR','CAR','CONS']:
                pass
            else:
                s = evalNum([ast[0][0]]+update, 'good')
                return sub(s,dict,error)
        elif ast[0][0] in ['CAR', 'CONS', 'CDR']:
            pass
        else:
            dict = updateDict(ast[0] , dict)
            return sub(ast[1:], dict, error)


def evalList(ast,message):
    if ast[0][0] == 'num':
        if ast[1][0] == 'CDR':
            pop =evalList(ast[1], message)
            return [ast[0]]+pop
        else:
            return ast
    elif ast[0][0] == 'var':
        return ast
    elif ast[0] == 'CDR':
        pop = evalList(ast[1], message)
        if pop==[]:
            message='bad'
        let = pop[1][1]
        if let == []:
            let = [let]
        if 'LET' in let[0]:
            eval = evalList(let[0], message)
            return [pop[1][0] + [ eval]]
        else:
            return 'lists empty guy' if message == 'bad' else pop[1]
    elif ast[0] == 'CONS':
        next = evalNum(ast[1][0], message)
        edit = [['num',next]] + [ast[1][1:]]
        return evalList(edit,message)
    elif ast[0] == 'LET' or 'LET' in ast[1][0]:
        set = sub(ast[1:],{},message)
        return set

def evalNum(ast, message):
    if ast[0] == 'LET':
        set = sub(ast[1:],{},message)
        return set
    elif ast[0] == 'num':
        return ast[1]
    elif ast[0] == 'var':
        return ast[1]
    elif ast[0] == '+':
        left = evalNum(ast[1], message)
        right = evalNum(ast[2],message)
        message = errorCheck(left,right)
        return 'CAR of empty list' if message == 'bad' else left+ right
    elif ast[0] == '-':
        left = evalNum(ast[1],message)
        right = evalNum(ast[2],message)
        message = errorCheck(left, right)
        return 'CAR of empty list' if message == 'bad' else left - right
    elif ast[0] == '*':
        left = evalNum(ast[1],message)
        right = evalNum(ast[2],message)
        message = errorCheck(left,right)
        return 'CAR of empty list' if message == 'bad' else left * right
    elif ast[0] == '/':
        left = evalNum(ast[1],message)
        right = evalNum(ast[2],message)
        message = errorCheck(left,right)
        if right == 0:
            return 'Cannot divide by 0!'
        else:
            return 'CAR of empty list' if message == 'bad' else left / right
    elif ast[0] == 'CAR':
        s=evalList(ast[1], 'good')
        if s ==[] or s =='lists empty guy':
            message = 'bad'
        return 'CAR of empty list' if message == 'bad' else s[0][1]

def main():
  while True:
    data = read_input()
    if data == 'exit;':
      break
    try:
      ast = parser.parse(data)
      if ast[0] == 'list':
          expression = evalList(ast[1],'good')
          print(
              'CDR of empty list Error!' if expression == 'lists empty guy'
               else tuple( getIdentifiers(expression,[]) )
          )
      else:
          print(evalNum(ast[1],'good'))

    except Exception as inst:
      print(inst.args[0])
      continue

main()
