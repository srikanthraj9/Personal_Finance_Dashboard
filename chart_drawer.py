import turtle

def draw_category_chart(category_totals):
    if not category_totals:
        print("No data to show.")
        return

    categories = list(category_totals.keys())
    totals = list(category_totals.values())

    screen = turtle.Screen()
    screen.title("Expense Category Chart")
    screen.bgcolor("white")
    screen.setup(width=800, height=600)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.goto(-300, 200)
    t.pendown()
    t.pensize(2)
    t.color("black")

    t.write("Expense Category Chart", align="left", font=("Arial", 18, "bold"))
    t.penup()
    t.goto(-300, 150)

    max_amount = max(totals)
    bar_unit = 300 / max_amount

    y_pos = 120
    colors = ["#4CAF50", "#2196F3", "#FFC107", "#FF5722", "#9C27B0", "#00BCD4"]

    for i, category in enumerate(categories):
        amount = totals[i]
        bar_length = amount * bar_unit
        color = colors[i % len(colors)]

        t.goto(-300, y_pos)
        t.pendown()
        t.color(color)
        t.begin_fill()
        t.forward(bar_length)
        t.right(90)
        t.forward(30)
        t.right(90)
        t.forward(bar_length)
        t.right(90)
        t.forward(30)
        t.right(90)
        t.end_fill()

        t.penup()
        t.goto(-300 + bar_length + 10, y_pos - 20)
        t.color("black")
        t.write(f"{category}: {amount:.2f}", font=("Arial", 10, "normal"))

        y_pos -= 50

    t.hideturtle()
    screen.mainloop()
