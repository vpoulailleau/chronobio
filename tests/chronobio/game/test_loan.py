from chronobio.game.constants import LOAN_DURATION_IN_MONTHS, LOAN_INTEREST
from chronobio.game.loan import Loan


def test_month_cost_before_loan():
    loan = Loan(amount=100, start_day=10)
    assert loan.month_cost(day=5) == 0


def test_month_cost_after_loan():
    loan = Loan(amount=100, start_day=10)
    assert loan.month_cost(day=10 + LOAN_DURATION_IN_MONTHS * 30) == 0


def test_month_cost_during_loan():
    loan = Loan(amount=100, start_day=10)
    assert loan.month_cost(day=20) == int(
        loan.amount * LOAN_INTEREST / LOAN_DURATION_IN_MONTHS
    )


def test_remaining_amount_at_start():
    loan = Loan(amount=100, start_day=10)
    assert loan.amount == 100