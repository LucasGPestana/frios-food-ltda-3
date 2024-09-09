from src.business_plan import BusinessPlan
from src.utils import changeColor

if __name__ == "__main__":

  b_plan = BusinessPlan(150, 550)

  for quantity in [0, 50, 100, 200, 148, 149, 165, 450, 550]:

    print(f"Lucro para {quantity} unidades vendidas: R${changeColor(b_plan.calculateProfit(quantity))}")
  
  print(f"Ponto de equilíbrio: {b_plan.break_even_point} unidades")
  print(f"Lucro máximo: R${b_plan.maximum_profit}")

  b_plan.generateGraphic("Profit")
  b_plan.generateGraphic("Cost")
  b_plan.generateGraphic("Revenue")