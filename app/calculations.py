def add(num1: int, num2: int):
    return num1 + num2


def mul(num1: int, num2: int):
    return num1 * num2


def div(num1: int, num2: int):
    return num1 / num2


def sub(num1: int, num2: int):
    return num1 - num2


class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, start_balance=0):
        self.balance = start_balance

    def deposite(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("insufficient funds in acc")
        self.balance -= amount

    def collect_interst(self):
        self.balance *= 1.1
