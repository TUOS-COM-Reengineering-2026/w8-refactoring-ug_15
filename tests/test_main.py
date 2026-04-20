import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items, calculate_shipping_fee_for_heavy_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchases(self):
        cm = CustomerManager()
        name = "Charles"
        purchase1 = {'price': 100, 'item': 'apple'}
        purchase2 = {'price': 300, 'item': 'grape'}
        cm.add_purchases(name, [purchase1, purchase2])

        self.assertEqual(
            {name: [purchase1, purchase2]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility_various_prices(self):
        test_cases = [
            ("Bob", [{'price': 600}], "Eligible for discount"),
            ("Bill", [{'price': 301}], "Potential future discount customer"),
            ("Alice", [{'price': 100}], "No discount"),
            ("Charlie", [{'price': 1300}], "VIP Customer!"),
            ("Charlie-taxed", [{'price': 1001}], "Eligible for discount"),
            ("Cameron", [{'price': 810}], "Priority Customer"),
        ]

        for name, purchases, expected_text in test_cases:
            cm = CustomerManager()
            cm.add_customer(name, purchases)

            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                cm.generate_report()

            output = captured.getvalue()

            self.assertIn(name, output)
            self.assertIn(expected_text, output)

    def test_calculate_shipping_fee(self):
        test_cases = [
            (5, False, 20, 25),
            (40, False, 50, 25),
            (5, True, 20, 60),
        ]
        for weight, fragile, cost, cost_frag in test_cases:
            cm = CustomerManager()
            purchases = [{'price': 40, 'weight': weight, 'fragile': fragile}]

            fee = cm.calculate_shipping_fee(purchases)
            self.assertEqual(fee, second=cost)

            fee = calculate_shipping_fee_for_heavy_items(purchases)
            self.assertEqual(fee, second=cost)

            fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
            self.assertEqual(fee_fragile, cost_frag)

if __name__ == "__main__":
    unittest.main()
