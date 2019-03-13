import pycosat

def main(args):
    if len(args) == 0:
        print("Not enough arguments")
        return
    solveSudoku(args[0])

def solveSudoku(path):
    cnf = parseToFormula(path)
    sudoku(cnf)
    print("Amount of CNF:" + str(len(cnf)))

    # SAT 
    satResult = pycosat.solve(cnf)

    if (satResult == "UNSAT"):
        print("Unsatisfiable")
        return
    else:
        print("Satisfiable")

    solution = set(satResult) # множество

    file = open(path + "_result.txt","w+") # создание файла

    for i in range(0, 9):
        for j in range(0, 9):
            file.write("%d", fromVar(i,j,solution))
        file.write("\n")

    print(file.read())
    file.close();

# закодировать
def toVar(row, column, value):
    return 81 * row + 9 * column + value

# раскодировать
def fromVar(row, column, set):
    for value in range(1, 10):
        if toVar(row, column, value) in set:
            return value

def parseToFormula(path):
    cnf = []
    row = column = 0
    text = open(path, "r").read()
    for c in text:
        if c >= '1' and c <= '9':
            var = toVar(row, column, int(c))
            cnf.append([var])
        if c == '\n':
            row += 1
            column = 0
        else:
            column += 1

    print(text)
    return cnf

def sudoku(cnf):
    # только одно число в каждой клетке
    for i in range(0,9):
        for j in range(0,9):
            for k in range(1,10):
                for t in range(1,10):
                    if t != k:
                        cnf.append([-toVar(i,j,k), -toVar(i,j,t)])
    # хотя бы одно число в каждой клетке
    for i in range(0,9):
        for j in range(0,9):
            toAdd = []
            for k in range(1,10):
                toAdd.append(toVar(i,j,k))
            cnf.append(toAdd)
    # в строке все числа
    for i in range(0,9):
        for k in range(1,10):
            for j in range(0,9):    
                for t in range(0,9):
                    if t != j:
                        cnf.append([-toVar(i,j,k), -toVar(i,t,k)])
    # в столбце все числа
    for j in range(0,9):
        for k in range(1,10):
            for i in range(0,9):    
                for t in range(0,9):
                    if t != i:
                        cnf.append([-toVar(i,j,k), -toVar(t,j,k)])
    # в блоке все числа
    for bRow in range(0,3):
        for bCol in range(0,3):
            # в блоке
            for i in range(0,3):
                for j in range(0,3):
                    for k in range(1,10):
                        for t in range(1,10):
                            if t != k:
                                gI = bRow * 3 + i
                                gJ = bCol * 3 + j
                                cnf.append([-toVar(gI,j,k), -toVar(gJ,j,t)])


if __name__ == '__main__':
    path = raw_input("Enter path: ")
    solveSudoku(path)