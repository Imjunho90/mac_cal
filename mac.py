import time

eps=1e-6

def normalize_label(label): # 4
    
    if label=='+' or str(label).lower()=='cross':
        return 'Cross'
    
    if str(label).lower()=='x':
        return 'X'
    
    return None


def mac(pattern, filter): # 5
    
    score=0.0
    
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score+=pattern[i][j] * filter[i][j]
    
    return score


def decide(score_a,score_b,label_a="A",label_b="B"): # 6.1
    
    if abs(score_a-score_b) < eps or score_a==score_b:
        return "UNDECIDED"
    
    if score_a>score_b:
        return label_a
    
    return label_b


def measure_mac(pattern,filter,repeat=10): # 6.2
    
    total_time=0.0
    
    for _ in range(repeat):
        start_time=time.perf_counter()
        mac(pattern,filter)
        end_time=time.perf_counter()

        total_time+=end_time-start_time
    average_time=total_time/repeat
    
    return average_time*1000


def input_matrix(size,title):
    
    while True:
        print(f"\n {title} ({size}줄 입력, 공백 구분)")
        
        matrix=[]
        error=False
        
        for _ in range(size):
            try:
                row=list(map(float,input().split()))
                if len(row)!=size:
                    print(
                        f"입력 형식 오류: 각 줄에 {size}개의 숫자를 "
                        "공백으로 구분해 입력하세요."
                    )
                    error=True
                    break
                    
                matrix.append(row)
                    
            except ValueError:
                print("입력 형식 오류 : 숫자만 입력하세요.")
                error=True
                break
                
        if not error and len(matrix)==size:
            return matrix
            
        print("처음부터 다시 입력해주세요.")
    
    
def user_mode():
    print("\n#---------------------------------------")
    print("#[1] 필터 입력")
    print("#---------------------------------------")
    
    filter_a=input_matrix(3,"filter_A")
    filter_b=input_matrix(3,"filter_B")
    
    print("\n필터 저장 완료")
    
    print("\n#---------------------------------------")
    print("#[2] 패턴 입력")
    print("#---------------------------------------")
    pattern= input_matrix(3,'pattern')
    
    score_a=mac(pattern,filter_a)
    score_b=mac(pattern,filter_b)
    
    result=decide(score_a,score_b)
    
    average_time=(measure_mac(pattern,filter_a)+measure_mac(pattern,filter_b))/2
    
    print("\n#---------------------------------------")
    print("#[3] MAC 결과")
    print("#---------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {average_time:.3f}ms")
    
    if result=="UNDECIDED":
        print(f"판정: 판정불가(|A-B| < {eps})")
    else: 
        print(f"판정: {result} ")
    
    




        

def main():
    
    while True:
        print("\n=== Mini NPU Simulator ===")
        
        print("\n [모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        
        choice=input("선택:").strip()
        
        if choice=='1':
            user_mode()
            break
        elif choice=='2':
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
            
            
if __name__ == "__main__":

    main()