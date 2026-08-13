import time

eps=1e-6

def normalize_label(label):
    
    if label=='+' or str(label).lower()=='cross':
        return 'Cross'
    
    if str(label).lower()=='x':
        return 'X'
    
    return None


def mac(pattern, filter):
    
    score=0.0
    
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score+=pattern[i][j] * filter[i][j]
    
    return score


def decide(score_a,score_b,label_a="A",label_b="B"):
    
    if abs(score_a-score_b) < eps:
        return "UNDECIDED"
    
    if score_a>score_b:
        return label_a
    
    return label_b

def input_matrix(size,title):
    
    while True:
        print(f"\n {title} ({size}줄 입력, 공백 구분)")
        
        matrix=[]
        error=False
        
        try:
            for _ in range(size):
                row=list(map(float,input().split()))
                
                if len(row)!=size:
                    error=True
                    break
                
                matrix.append(row)
        except ValueError:
            print("입력 형식 오류 : 숫자만 입력하세요.")
            error=True
            break
    if not error and len(matrix)==size:
        return matrix
    
