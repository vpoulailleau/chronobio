from chronobio.game.constants import LOAN_DURATION_IN_MONTHS, LOAN_INTEREST
from chronobio.game.loan import Loan


def float_equal(a: float, b: float) -> bool:
    return int(a + 0.5) == int(b + 0.5)


def test_month_cost_before_loan():
    loan = Loan(amount=100, start_day=10)
    assert loan.month_cost(day=5) == 0


def test_month_cost_after_loan():
    loan = Loan(amount=100, start_day=10)
    assert loan.month_cost(day=10 + LOAN_DURATION_IN_MONTHS * 30) == 0


def test_month_cost_during_loan():
    loan = Loan(amount=100, start_day=10)
    assert (
        loan.month_cost(day=20) == loan.amount * LOAN_INTEREST / LOAN_DURATION_IN_MONTHS
    )


def test_remaining_amount_at_start():
    loan = Loan(amount=100, start_day=10)
    assert loan.amount == 100


def test_remaining_cost_at_start():
    loan = Loan(amount=100, start_day=10)
    assert float_equal(loan.remaining_cost(day=10), loan.amount * LOAN_INTEREST)


def test_expense_greater_than_income():
    loan = Loan(amount=1, start_day=10)
    assert LOAN_DURATION_IN_MONTHS * loan.month_cost(day=20) > loan.amount
