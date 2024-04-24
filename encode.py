import hashlib

if __name__ == '__main__':
    password = input("Enter your password: ")
    data_sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(data_sha)
