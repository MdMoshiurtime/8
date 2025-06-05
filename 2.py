print("Enter the number of queens")
N = int(input())

# সমস্ত সমাধান সংরক্ষণ করার জন্য লিস্ট
all_solutions = []

def is_attack(i, j, board):
    # কলাম চেক
    for k in range(i):
        if board[k][j] == 1:
            return True
    
    # উপরের ডান দিকের ডায়াগোনাল চেক
    k, l = i-1, j+1
    while k >= 0 and l < N:
        if board[k][l] == 1:
            return True
        k -= 1
        l += 1
    
    # উপরের বাম দিকের ডায়াগোনাল চেক
    k, l = i-1, j-1
    while k >= 0 and l >= 0:
        if board[k][l] == 1:
            return True
        k -= 1
        l -= 1
    
    return False

def n_queen(row, n, board):
    if n == 0:
        # বোর্ডের একটি কপি সংরক্ষণ করুন
        all_solutions.append([row[:] for row in board])
        return
    
    for j in range(N):
        if not is_attack(row, j, board):
            board[row][j] = 1
            
            n_queen(row+1, n-1, board)
            
            board[row][j] = 0  # ব্যাকট্র্যাকিং

initial_board = [[0]*N for _ in range(N)]
n_queen(0, N, initial_board)

print(f"\nTotal solutions found: {len(all_solutions)}\n")
for idx, solution in enumerate(all_solutions, 1):
    print(f"Solution {idx}:")
    for row in solution:
        print(row)
    print()