from chronobio.game.loan import Loan


def test_remaining_amount_at_start():
    loan = Loan(amount=100, start_day=10)

    assert loan.amount == 100