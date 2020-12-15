import time
import random
import random
import edit_doc
from sys import exit
from copy import deepcopy

# Manual enter board
board = [[5,3,0,0,7,0,0,0,0],
         [6,0,0,1,9,5,0,0,0],
         [0,9,8,0,0,0,0,6,0],
         [8,0,0,0,6,0,0,0,3],
         [4,0,0,8,0,3,0,0,1],
         [7,0,0,0,2,0,0,0,6],
         [0,6,0,0,0,0,2,8,0],
         [0,0,0,4,1,9,0,0,5],
         [0,0,0,0,8,0,0,7,9]]
boards = deepcopy(board)
stopp = False


def main():
    reboard()
    while True:
        print('1. gen : Generate problem\n',
              '2. emp : Empty board\n',
              '3. fill: Fill board with manual entered number\n',
              '4. sub : Substitute solve\n',
              '5. bac : Backtrack sovle\n',
              '6. test: Test Algolithms times\n',
                sep="")
        cmd = input('solve method: ')
        if cmd == "sub":
            susbstitute_solve()
            print_board()
        if cmd == "gen":
            n_rm = int(input("How many: "))
            Generate_board()
            random_remove(n_rm)
            to_pdf()
        if cmd == "exit":
            exit(0)
        if cmd == "test":
            algolithm_test()
        if cmd == "emp":
            empty_board()
        if cmd == "fill":
            reboard()
        if cmd == 'bac':
            backtrack_solve()
            print_board()
        else: continue

def reboard():
    global board
    global boards
    board = deepcopy(boards)

def Generate_board():
    ### Use for generate a random sudoko problem
    def backtrack(h,max):
        global stopp
        i = unsolve_pos[h][0]
        j = unsolve_pos[h][1]

        legal_num = generate_numberset()

        for n in range(9):
            #print(h)
            board[i][j] = legal_num[n]
            #print(i,j)
            if check(i,j,legal_num[n]):
                if h + 1 < max:
                    #print_board()
                    backtrack(h + 1,max)
                else:
                    #print ("found")
                    stopp = True
            if stopp:
                return
            #print("tracing back tree")
        board[i][j] = 0

    def generate_numberset():
        ### Random process ###
        legal_num = []
        while True:
            if len(legal_num) == 9:
                break
            rnd_num = random.randint(1, 9)
            legal_num.append(rnd_num)
            for item in legal_num[:-1]:
                if rnd_num == item:
                    del legal_num[-1]
                    break
        return legal_num

    global board
    global stopp
    #random.seed(a=1992)
    empty_board()
    stopp = False
    unsolve_n, unsolve_pos = find_num_unsolve()
    backtrack(0,unsolve_n)

def random_remove(n):
    global board
    max_round = 200
    k = 0; r = 0

    while k < n and r < max_round:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if board[i][j] != 0:
            old_value = board[i][j]
            board[i][j] = 0
            print_board()
            if check_unique_answer() != 1 :
                board[i][j] = old_value
                print ("not unique")
                r += 1
            else:
                k += 1
            print(f"r={r}")
        print (f"k={k}")
    """
    if k < n:
        backtrack_solve()
        random_remove(n)
    """
    global boards
    boards = deepcopy(board)
    print_board()

def empty_board():
    global board
    for i in range(9):
        for j in range(9):
            board[i][j] = 0
    print_board()

def to_pdf():
    edit_doc.main(board)

def check_unique_answer():
    #print("backtrack")
    global board
    unsolve_n, unsolve_pos = find_num_unsolve()
    n_answer = 0

    def backtrack(h,max, n_answer):
        global stopp
        i = unsolve_pos[h][0]
        j = unsolve_pos[h][1]
        for n in range(1,10):
            board[i][j] = n
            if check(i,j,n):
                if h + 1 < max:
                    n_answer += backtrack(h + 1,max,n_answer)
                else:
                    n_answer += 1
        board[i][j] = 0
        return n_answer

    #print(f"HHH {unsolve_n}")
    n_answer = backtrack(0,unsolve_n, n_answer)
    print (n_answer)
    #print_board()
    return n_answer

def algolithm_test():
    algo_name = ["backtrack","susbstitute1","susbstitute2"]
    times = []
    for j in range(3):
        total_time = 0
        for i in range(100):
            reboard()
            t0 = time.time()
            if j == 0:
                backtrack_solve()
            if j == 1:
                susbstitute_solve()
            if j == 2:
                susbstitute_solve2()
            round_time = round(1000*(time.time() - t0),3)
            total_time += round_time
            #checkall()
        times.append(total_time)

    for i in range(len(algo_name)):
        print(f"{algo_name[i]} total {times[i]}")
    return

### Helper fn ###
def print_board():
    global board
    print("-------------------------")
    for h in range(3):
        for i in range (3): #loop row
            print("|",end = " ")
            for j in range (3): #loop bucket
                for k in range (3): #loop element
                    position = board[i + h * 3][k + 3 * j]
                    if position == 0:
                        print("-", end = " ")
                    else: print(str(position),end = " ")
                print("|",end = " ")
            print("")
        print("-------------------------")
def print_board2():
    global board
    print("-------------------------")
    for h in range(3):
        for i in range (3): #loop row
            print("|",end = " ")
            for j in range (3): #loop bucket
                for k in range (3): #loop element
                    position = board[i + h * 3][k + 3 * j]
                    if position == 0:
                        print("-", end = " ")
                    else: print(str(position),end = " ")
                print("|",end = " ")
            print("")
        print("-------------------------")

def find_num_unsolve():
    global board
    unsolve_n = 0
    unsolve_pos = []
    for i in range(9): #loop row
        for j in range (9): #loop col
            if board[i][j] == 0:
                unsolve_n += 1
                unsolve_pos.append([i,j])
    #print (f"unsolve_n {unsolve_n}")
    #print (unsolve_pos)
    return unsolve_n, unsolve_pos

def check(i,j,ck):
    global board
    row_block =  i // 3
    col_block =  j // 3

    for m in range(3):
        for n in range(3):
            #print(m + 3 * row_block,n + 3 * col_block)
            if not(m + 3 * row_block == i and n + 3 * col_block == j):
                if board[m + 3 * row_block][n + 3 * col_block] == ck:
                     #print(f"incorrect {i} {j} with {m + 3 * row_block} {n + 3 * col_block}")
                     return False

    for m in range(9):
        if not(m == j):
            if board[i][m] == ck:
                #print(f"incorrect {i} {j} with {i} {m}")
                return False

    for m in range(9):
        if not(m == i):
            if board[m][j] == ck:
                #print(f"incorrect {i} {j} with {m} {i}")
                return False
    #print("True")
    return True

def checkall():
    correct = True
    global board
    for i in range(9):
        for j in range(9):
            if not(check(i,j,board[i][j])):
                print(f"incorrect {i} {j}")
                return False
            correct = correct and check(i,j,board[i][j])
    print(f"correct {correct}")
    return correct



##################### Solving Algolithm ##########################
# Substitute 1 and 2 runtime equally fast
def susbstitute_solve():
    #print("sub")
    global board
    max_try = 10
    ans = []
    unsolve_n, unsolve_pos = find_num_unsolve()


    for x in range(max_try): #x = turn
        if unsolve_n == 0:
            #print (f"solve in {x} turn")
            break

        for i in range(9): #loop row
            for j in range (9): #loop col
                if board[i][j] == 0:
                    for k in range(1,10):
                        if check(i,j,k) :
                            ans.append(k)
                    if len(ans) == 1:
                        board[i][j] = ans[0]
                        #print
                        #print_board()
                        unsolve_n -= 1
                    #print (i,j,ans)
                    ans = []

def susbstitute_solve2():
    #print("sub")
    global board
    max_try = 10
    ans = []
    unsolve_n, unsolve_pos = find_num_unsolve()


    for x in range(max_try): #x = turn
        if unsolve_n == 0:
            #print (f"solve in {x} turn")
            break

        dellist = []
        for h in range(unsolve_n):
            i = unsolve_pos[h][0]
            j = unsolve_pos[h][1]
            #print (f"i: {i}, j: {j}")
            for k in range(1,10):
                if check(i,j,k) :
                    ans.append(k)
            if len(ans) == 1:
                board[i][j] = ans[0]
                #print_board()
                unsolve_n -= 1
                dellist.append(h)
            #print (i,j,ans)
            ans = []
        for index in dellist[::-1]:
            del unsolve_pos[index]
        #print(f"Len UNSOLVE:{len(unsolve_pos)}")
    #print_board()

def tryall_solve():
    print("try all")
    global board
    global stopp
    stopp = False

    unsolve_n, unsolve_pos = find_num_unsolve()
    ans = []

    for h in range(unsolve_n):
        ans.append(1)

    def brute(n, max):
        global stopp
        #for h in range(unsolve_n):
        for m in range(9):
            if not n + 1 == max :
                brute(n+1, max)
            else:
                print (ans)
                fill_table(ans)
            if stopp:
                print("found")
                return
            ans[n] += 1
        ans[n] = 1

    def fill_table(ans):
        global stopp
        for h in range(unsolve_n):
            i = unsolve_pos[h][0]
            j = unsolve_pos[h][1]
            board[i][j] = ans[h]
        if (checkall()):
            print_board()
            stopp = True
        reboard()

    brute(0, unsolve_n)

def backtrack_solve():
    #print("backtrack")
    global board
    global stopp
    stopp = False
    unsolve_n, unsolve_pos = find_num_unsolve()
    def backtrack(h,max):
        global stopp
        i = unsolve_pos[h][0]
        j = unsolve_pos[h][1]
        for n in range(1,10):
            #print(h)
            board[i][j] = n
            #print(i,j)
            if not check(i,j,n):
                pass
            else:
                if h + 1 < max:
                    #print_board()
                    backtrack(h + 1,max)
                else:
                    #print ("found")
                    stopp = True
            if stopp:
                return
        board[i][j] = 0
    #print(f"HHH {unsolve_n}")
    backtrack(0,unsolve_n)

#################################################################

if __name__ == "__main__":
    main()
