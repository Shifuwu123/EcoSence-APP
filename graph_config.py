import flet as ft

################################################################################
# Configuracion Gráficas ##############################################
class grid_line(ft.ChartGridLines):
    def __init__(self):
        super().__init__()
        self.interval = 1
        self.color = ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)
        self.width = 1


class graph_major(ft.LineChart):
    def __init__(
        self,
        data_series: list[ft.LineChartData] | None = None,
    ):
        super().__init__()
        self.data_series = data_series
        self.border = ft.border.all(
            3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)
        )
        self.horizontal_grid_lines = grid_line()
        self.vertical_grid_lines = grid_line()
        self.tooltip_bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY)
        self.min_y = 0
        self.max_y = 6
        self.min_x = 0
        self.max_x = 11
        self.expand = True

# Fin configuracion Gráficas ############################################
################################################################################
