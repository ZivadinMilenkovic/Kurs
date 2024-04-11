from typing import Literal
from app.calculations import add, sub, mul, div, BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_acc():
    return BankAccount()


@pytest.fixture
def bank_acc():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected", [(5, 3, 8), (7, 1, 8), (12, 4, 16)])
def test_add(
    num1: Literal[5] | Literal[7] | Literal[12],
    num2: Literal[3] | Literal[1] | Literal[4],
    expected: Literal[8] | Literal[16],
):
    assert add(num1, num2) == expected


def test_div():
    assert div(8, 4) == 2


def test_mul():
    assert mul(9, 4) == 36


def test_sub():
    assert sub(9, 4) == 5


def test_bank_set_initial_amount(bank_acc: BankAccount):
    assert bank_acc.balance == 50


def test_bank_default_amount(zero_bank_acc: BankAccount):
    assert zero_bank_acc.balance == 0


def test_withdraw(bank_acc):
    bank_acc.withdraw(20)
    assert bank_acc.balance == 30


def test_deposit(bank_acc):
    bank_acc.deposite(20)
    assert bank_acc.balance == 70


def test_collect_interst(bank_acc):
    bank_acc.collect_interst()
    assert round(bank_acc.balance, 4) == 55


@pytest.mark.parametrize(
    "deposited,withdrew,expected", [(50, 30, 20), (70, 10, 60), (120, 40, 80)]
)
def test_bank_transaction(zero_bank_acc, deposited, withdrew, expected):
    zero_bank_acc.deposite(deposited)
    zero_bank_acc.withdraw(withdrew)
    assert zero_bank_acc.balance == expected


def test_insufficient_funds(bank_acc):
    with pytest.raises(InsufficientFunds):
        bank_acc.withdraw(55)
