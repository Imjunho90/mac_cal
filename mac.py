import time
import json

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
    
    
def user_mode(): # 2
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
    

def normalize_filters(filters):
    
    result={}
    
    for size,filter in filters.items():
        
        size=int(size.replace('size_',''))
        result[size]={}
        
        for key,value in filter.items():
            label=normalize_label(key)
            
            if label is not None:
                result[size][label]=value
                
    return result

def make_zero_matrix(size):
    
    return [[1.0 for _ in range(size)] for _ in range(size)]

def performance_analysis(sizes):
    
    for size in sizes:
        pattern=make_zero_matrix(size)
        filter=make_zero_matrix(size)
        
        average=measure_mac(pattern,filter)
        operation_count=size**2
        print(f"{size}x{size:<5} {average:<5.3f}ms {operation_count:>7}")
        


def json_mode():
    
    total_test=0
    passed=0
    failed=0
    fail_case=[]
    print('\n#-----------------')
    print('# [1] 필터 로드')
    print('#-----------------')
    
    try:
        with open('data.json','r') as f:
            data=json.load(f)
    except FileNotFoundError:
        print("data.json 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print("data.json 파일의 형식이 올바르지 않습니다.")
        return
    except OSError as e:
        print(f"파일 열기 오류: {e}")
        return
    
    
    filter=normalize_filters(data.get('filters'))
    pattern=data.get('patterns')
    
    if not isinstance(filter,dict):
        print("오류: filters 데이터가 존재하지 않거나 형식이 잘못됬습니다.")
        return
    if not isinstance(pattern,dict):
        print("오류: pattern 데이터가 존재하지 않거나 형식이 잘못됬습니다.")
        return
    
    for size in [5,13,25]:
        
        if size in filter and 'Cross' in filter[size] and 'X' in filter[size]:
            print(f"✓ size_{size} 필터 로드 완료 (Cross, X)")
            
        else: print(f"x size_{size} 필터 로드 실패")
    
    print("\n#-------------------------------")
    print(" [2] 패턴 분석")
    print("#-------------------------------")
    
    for key, value in pattern.items():
        size=int((key.split('_'))[1])
        cross_filter=filter[size].get("Cross")
        x_filter=filter[size].get("X")
        
        cross_score=mac(value['input'],cross_filter)
        x_score=mac(value['input'],x_filter)
        decided=decide(cross_score,x_score,'Cross','X')
        expected1=normalize_label(value['expected'])
        if decided == expected1:
            porf='PASS'
            passed+=1
        else:
            porf='FAIL'
            failed+=1
            fail_case.append(f'{key}: 동점(UNDICIDED) 처리 규칙에 따라 FAIL')
            
            
        total_test+=1
        
        f
        print(f'---{key}---')
        print(f'Cross 점수{cross_score}')
        print(f'X 점수 {x_score}')
        print(f'판정 {decided} | expected: {expected1} | {porf}')
        
        
    print("\n#-------------------------------")
    print(" [3] 성능 분석 (평균/10회)")
    print("#-------------------------------")
    print("크기   평균 시간(ms) 연산 횟수")
    performance_analysis([3,5,13,25])
        
    

    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total_test}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")
    
    print("\n실패 케이스:")
    
    for case in fail_case:
        print(f'-{case}')
        

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
            json_mode()
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
            
            
if __name__ == "__main__":

    main()