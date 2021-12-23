import os
import win32file
from cryptography.fernet import Fernet

keys={} # dictionary 사용하여 field,usr,pwd 저장

class F(): # 암호 관련 클래스 생성
    def __init__(self, key=None) -> None:
        if os.name=="nt":
            key_name="p.key" # Windows인 경우 key filename
        else:
            key_name=".pkey" # Linux 인 경우 key filename, hidden
        if not os.path.isfile(key_name): # key가 존재하지 않으면 생성
            key=Fernet.generate_key()
            with open(key_name,"wb") as f:
                f.write(key)
            if os.name=="nt": # hidden file(Windows)
                win32file.SetFileAttributes(key_name,2)
        else:
            key=open(key_name,"rb").read() # key가 존재하면 읽음
        self.key=key
        self.f=Fernet(self.key)
    
    def encrypt(self, data, is_string=True): # 암호화 method
        if isinstance(data,bytes): # bytes 인 경우 그대로 암호화
            res=self.f.encrypt(data)
        else:
            res=self.f.encrypt(data.encode("utf-8")) # 문자열이면 인코딩 후 암호화
        if is_string:
            return res.decode("utf-8") # 문자열 출력 시 디코딩
        else:
            return res
    
    def decrypt(self, data, is_string=True): # 복호화 method
        if isinstance(data,bytes): # bytes 인 경우 그대로 복호화
            res=self.f.decrypt(data)
        else:
            res=self.f.decrypt(data.encode("utf-8")) # 문자열이면 인코딩 후 복호화
        if is_string:
            return res.decode("utf-8") # 문자열 출력 시 디코딩
        else:
            return res

password=F() # password 객체 생성

def clear(): # clear prompt
    os.system("cls" if os.name=="nt" else "clear")

def Add(): # 필드 추가 함수
    while True:
        field_name=input("Field Name: ").strip()
        if field_name=="" or field_name.isspace(): continue
        else: break
    while True:
        user_name=input("User Name: ").strip()
        if user_name=="" or user_name.isspace(): continue
        else: break
    while True:
        pwd=input("Password: ").strip()
        if pwd=="" or pwd.isspace(): continue
        else: break
    content=(user_name,pwd)
    keys[field_name]=content

def Remove(): # 필드 제거 함수
    field=input("Key name to remove: ").strip()
    if keys.get(field) != None:
        del keys[field]
        print("Key removed")
    else:
        print("Not valid key name")

def Search(): # 필드 검색 함수
    while True:
        src=input("Key name or username (* to show all): ").strip()
        if src=="" or src.isspace(): continue
        else: break
    found=False
    if src=="*": # wildcard 입력일 때 전체 출력
        for field in keys:
            i=keys[field]
            print(f"Key: {field}")
            print(f"Username: {i[0]}")
            print(f"Password: {i[1]}")
            print()
        return
    for field in keys: # 부분 문자열로 검색하여 출력
        if (src in field) or (src in keys[field][0]):
            i=keys[field]
            print(f"Key: {field}")
            print(f"Username: {i[0]}")
            print(f"Password: {i[1]}")
            print()
            found=True
    if not found:
        print("No key found")

def Save(f): # 종료 시 passwd 파일에 딕셔너리 저장
    for field in keys:
        fld=field
        usr,pwd=keys[field]
        pwd=password.encrypt(pwd)
        f.write(f"{fld},{usr},{pwd}\n")
    f.close()

def Load(f): # 실행 시 passwd 파일로 딕셔너리 초기화
    f.seek(0) # append 이므로 파일 포인터 처음으로
    for line in f:
        fld,usr,pwd=line.strip().split(",")
        try:
            pwd=password.decrypt(pwd)
        except:
            continue
        content=(usr,pwd)
        keys[fld]=content

def main():
    f=open("passwd","a+t") # 파일이 있다면 그대로 읽기, 없다면 생성
    Load(f)
    f.close()
    while True:
        print("""\
1. Add password
2. Remove password
3. Search
4. Exit\
                """)
        print("> ",end="")
        i=input().strip()
        if i=="1":
            clear()
            Add()
        elif i=="2":
            clear()
            Remove()
        elif i=="3":
            clear()
            Search()
        elif i=="4":
            f=open("passwd","wt") # 저장 시 passwd 파일 덮어쓰기
            Save(f)
            exit()
        else:
            clear()
            continue

if __name__=="__main__":
    main()
