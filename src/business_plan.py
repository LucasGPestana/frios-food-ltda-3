import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os

class BusinessPlan:

  """
  Representa o plano de negócio da Frios Foods Ltda
  """
  
  def __init__(self, fixed_quantity: int, demand_quantity: int) -> None:

    """
    Parâmetros:

      fixed_quantity: Corresponde a quantidade limite a qual a função custo total é válida. Após esse valor, será aplicada uma nova regra a função custo total, correspondente a equação da reta tangente a função custo total com a regra anterior.

      demand_quantity: Corresponde a quantidade demandada pela empresa.

    """

    self.initial_point = [fixed_quantity]
    self.initial_point = self.initial_point + [self.calculateTotalCost(fixed_quantity)]

    self.demand_quantity = demand_quantity
  
  @property
  def linear_rate_change(self):

    """
    Taxa de variação linear, ou coeficiente angular.
    """

    x = sp.Symbol('x')

    # Mesma função que calcula o custo total, mas usando o objeto Symbol do sympy
    total_cost_function = 800 + 0.16 * x - 6e-4 * x ** 2 + 3e-6 * x ** 3

    # Taxa de variação linear da reta tangente
    return sp.limit((total_cost_function - self.initial_point[1]) / (x - self.initial_point[0]), x, self.initial_point[0])
  
  def calculateTotalCost(self, quantity: int) -> float:

    """
    Custo total por quantidade

    Caso a quantidade seja superior a quantidade fixa definida, a regra da função custo total será remodelada para a equação da reta tangente a função custo total inicial 
    """

    if quantity <= self.initial_point[0]:

      return 800 + 0.16 * quantity - 6e-4 * quantity ** 2 + 3e-6 * quantity ** 3

    """
    função que define o valor de y na reta tangente
    y - y0 = m * (x - x0) => y = m * x + y0 - m * x0
    """
    return self.linear_rate_change * quantity + self.initial_point[1] - self.linear_rate_change * self.initial_point[0]
    
  def calculateTotalRevenue(self, quantity: int) -> float:

    """
    Receita por quantidade
    """

    if quantity <= self.initial_point[0]:

      return 5.5 * quantity
    
    return 5 * quantity
  
  def calculateProfit(self, quantity: int) -> float:

    """
    Lucro por quantidade
    """

    return self.calculateTotalRevenue(quantity) - self.calculateTotalCost(quantity)
  
  def calculateMeanTotalCost(self, quantity: int) -> float:

    """
    Custo total médio por quantidade
    """

    if quantity == 0:

      return self.calculateTotalCost(quantity)

    return self.calculateTotalCost(quantity) / quantity
  
  @property
  def break_even_point(self) -> int:

    """
    Ponto de equilíbrio, que corresponde a quantidade cuja receita seja igual ou superior ao custo total
    """

    quantity: int = 0

    while self.calculateTotalRevenue(quantity) < self.calculateTotalCost(quantity):

      quantity += 1
    
    return quantity

  @property
  def maximum_profit(self) -> float:

    """
    Lucro máximo, ou seja, o lucro para a quantidade demandada pela empresa
    """

    return self.calculateProfit(self.demand_quantity)
  
  @property
  def maximum_total_cost(self) -> float:

    """
    Custo total máximo, ou seja, o lucro para a quantidade demandada pela empresa
    """

    return self.calculateTotalCost(self.demand_quantity)
  
  @property
  def maximum_total_revenue(self) -> float:

    """
    Receita total máxima, ou seja, o lucro para a quantidade demandada pela empresa
    """

    return self.calculateTotalRevenue(self.demand_quantity)
  
  def generateGraphic(self, ordinate_axis_variable:str) -> None:

    PROJECT_DIRPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if not os.path.exists(os.path.join(PROJECT_DIRPATH, "graphics")):

      os.mkdir(os.path.join(PROJECT_DIRPATH, "graphics"))

    ordinate_axis_variable = ordinate_axis_variable.lower()
    
    fig, ax = plt.subplots()

    x = np.arange(0, self.demand_quantity + 1)

    match ordinate_axis_variable:

      case "profit":

        y = list(map(self.calculateProfit, x))

        y_label = "Lucro (R$)"
        label = "Lucro por unidade vendida"
        title = "Lucro Associado a Cada Unidade Vendida"

        # Gráfico de dispersão
        ax.scatter(x=self.demand_quantity, y=self.maximum_profit, color='g', zorder=5, label=f"Lucro Máximo")

        ax.annotate(text=f"{self.maximum_profit:.2f}", xy=(self.demand_quantity, self.maximum_profit), xytext=(-15, -20), textcoords="offset points")
      
      case "cost":

        y = list(map(self.calculateTotalCost, x))

        y_label = 'Custo Total (R$)'
        label = "Custo Total por Unidade Vendida"
        title = "Custo Total Associado a Cada Unidade Vendida"

        # Gráfico de dispersão
        ax.scatter(x=self.demand_quantity, y=self.maximum_total_cost, color='g', zorder=5, label=f"Custo Total Máximo")

        ax.annotate(text=f"{self.maximum_total_cost:.2f}", xy=(self.demand_quantity, self.maximum_total_cost), xytext=(-15, -20), textcoords="offset points")

      case "revenue":

        y = list(map(self.calculateTotalRevenue, x))

        y_label = "Receita Total (R$)"
        label = "Receita Total por Unidade Vendida"
        title = "Receita Total Associada a Cada Unidade Vendida"

        # Gráfico de dispersão
        ax.scatter(x=self.demand_quantity, y=self.maximum_total_revenue, color='g', zorder=5, label=f"Receita Total Máxima")

        ax.annotate(text=f"{self.maximum_total_revenue:.2f}", xy=(self.demand_quantity, self.maximum_total_revenue), xytext=(-15, -20), textcoords="offset points")
      
      case "mean_cost":

        y = list(map(self.calculateMeanTotalCost, x))

        y_label = "Custo Total Médio (R$)"
        label = "Custo Total Médio por Unidade Vendida"
        title = "Custo Total Médio Associado a Cada Unidade Vendida"
      
      case _:

        raise Exception("A variável do eixo das ordenadas deve ser profit (lucro), cost (custo), revenue (receita)!")

    # Labels dos eixos e do gráfico
    ax.set_ylabel(y_label)
    ax.set_xlabel("Quantidade de Unidades Vendidas")
    ax.set_title(title)

    # Gráfico de Linha
    ax.plot(x, y, label=label)

    # Reta vertical
    ax.axvline(x=self.break_even_point, color="red", linestyle="--", label=f"Ponto de Equilíbrio")
    
    # Valores exibidos no eixo x
    ax.set(xticks=list(np.arange(0, self.demand_quantity, 100)) + [self.break_even_point])

    # Retira as linhas de cima e da direita do gráfico
    for direction in ["top", "right"]:

      ax.spines[direction].set_visible(False)

    # Exibe um gráfico com grades
    ax.grid(True)

    ax.legend()

    plt.tight_layout()
    plt.show()

    fig.savefig(f"{os.path.join(PROJECT_DIRPATH, "graphics", f"{ordinate_axis_variable}.png")}")