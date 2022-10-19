from chronobio.game.constants import LOAN_DURATION_IN_MONTHS, LOAN_INTEREST


class Loan:
    def __init__(self: "Loan", amount: int, start_day: int) -> None:
        self.amount = amount
        self.start_day = start_day

    def month_cost(self: "Loan", day: int) -> int:
        if not (self.start_day <= day < self.start_day + LOAN_DURATION_IN_MONTHS * 30):
            return 0
        return int(self.amount * LOAN_INTEREST / LOAN_DURATION_IN_MONTHS)

    def state(self: "Loan") -> dict:
        return {
            "amount": self.amount,
            "start_day": self.start_day,
        }

    def __repr__(self: "Loan") -> str:
        return f"Loan(amount={self.amount}, start_day={self.start_day})"
