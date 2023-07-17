from cryptography.fernet import Fernet


def read_key(filename):
    with open(filename, 'rb') as reader:
        line = reader.readline()
        if (line == b''):
            key = Fernet.generate_key()
            with open(filename, 'wb') as writer:
                writer.write(key)
        else:
            key = line
        return key


def view(fernet):
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:",
                  fernet.decrypt(passw.encode()).decode())


def add(fernet):
    name = input('Account Name: ')
    pwd = input("Password: ")

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fernet.encrypt(pwd.encode()).decode() + "\n")


def run_login(masterfile, fernet):
    with open(masterfile, 'a') as w:
        pass
    with open(masterfile, 'r') as f:
        line = f.readline()
        if line == '':
            print("You are now creating a new master password\n")
            masterpass = input('enter password:')
            with open(masterfile, 'w') as w:
                w.write(fernet.encrypt(masterpass.encode()).decode() + "\n")
            return True
    masterpass = fernet.decrypt(line.encode('utf-8'))
    guess = ''
    masterpassstr = masterpass.decode('utf-8')
    while guess != masterpassstr:
        guess = input('Enter master password (enter q to quit):')
        if guess == masterpassstr:
            print('Logged in!')
            return True
        elif guess != 'q':
            print('Entered password is wrong, please try again')
        if guess == 'q':
            return False


if __name__ == "__main__":
    key = read_key("venv/a.txt")
    f = Fernet(key)
    success = run_login('master.txt', f)

    while success:
        mode = input(
            "Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
        if mode == "q":
            break
        if mode == "view":
            view(f)
        elif mode == "add":
            add(f)
        else:
            print("Invalid mode.")
