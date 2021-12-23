import os
import win32file
from cryptography.fernet import Fernet

keys={}

class F():
    def __init__(self, key=None) -> None:
        if os.name=="nt":
            key_name="p.key"
        else:
            key_name=".pkey"
        if not os.path.isfile(key_name):
            key=Fernet.generate_key()
            with open(key_name,"wb") as f:
                f.write(key)
            if os.name=="nt":
                win32file.SetFileAttributes(key_name,2)
        else:
            key=open(key_name,"rb").read()
        self.key=key
        self.f=Fernet(self.key)
    
    def encrypt(self, data, is_string=True):
        if isinstance(data,bytes):
            res=self.f.encrypt(data)
        else:
            res=self.f.encrypt(data.encode("utf-8"))
        if is_string:
            return res.decode("utf-8")
        else:
            return res
    
    def decrypt(self, data, is_string=True):
        if isinstance(data,bytes):
            res=self.f.decrypt(data)
        else:
            res=self.f.decrypt(data.encode("utf-8"))
        if is_string:
            return res.decode("utf-8")
        else:
            return res

password=F()

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def Add():
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

def Remove():
    field=input("Key name to remove: ").strip()
    if keys.get(field) != None:
        del keys[field]
        print("Key removed")
    else:
        print("Not valid key name")

def Search():
    while True:
        src=input("Key name or username (* to show all): ").strip()
        if src=="" or src.isspace(): continue
        else: break
    found=False
    if src=="*":
        for field in keys:
            i=keys[field]
            print(f"Key: {field}")
            print(f"Username: {i[0]}")
            print(f"Password: {i[1]}")
            print()
        return
    for field in keys:
        if (src in field) or (src in keys[field][0]):
            i=keys[field]
            print(f"Key: {field}")
            print(f"Username: {i[0]}")
            print(f"Password: {i[1]}")
            print()
            found=True
    if not found:
        print("No key found")

def Save(f):
    for field in keys:
        fld=field
        usr,pwd=keys[field]
        pwd=password.encrypt(pwd)
        f.write(f"{fld},{usr},{pwd}\n")
    f.close()

def Load(f):
    f.seek(0)
    for line in f:
        fld,usr,pwd=line.strip().split(",")
        try:
            pwd=password.decrypt(pwd)
        except:
            continue
        content=(usr,pwd)
        keys[fld]=content

def main():
    f=open("passwd","a+t")
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
            f=open("passwd","wt")
            Save(f)
            exit()
        else:
            clear()
            continue

if __name__=="__main__":
    main()
