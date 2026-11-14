mac_price = 1299
mouse_price = 79
paper_price = 24.99
subtotal = mac_price + mouse_price + paper_price
tax = 0.08875*subtotal
tax = round(tax, 3)
total = subtotal + tax
print("subtotal", subtotal)
print("tax", tax)
print("total", total)