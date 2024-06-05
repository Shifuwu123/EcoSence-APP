"""
Aquí creare la card que mostrara el grafico con las estadisticas del cultivo
"""

import flet as ft
from decorators.app_class import containers_app_page as container

class chart_axis_left(ft.ChartAxisLabel):
    def __init__(self, position):
        super().__init__()
        self.value = position
        self.label = ft.Text(f"{position}m", size=14, weight=ft.FontWeight.BOLD)

class chart_axis_bottom(ft.ChartAxisLabel):
    def __init__(self, position: int, hr_ago: int):
        hr_ago = f"{hr_ago}H AGO" if hr_ago != 0 else 'NOW'

        time_label = ft.Container(
            content=ft.Text(
                hr_ago,
                size=16,
                weight=ft.FontWeight.BOLD
            ),
            margin=ft.margin.only(top=10),
        )

        super().__init__()
        self.value = position
        self.label = time_label

class chart_title(ft.ChartAxis):
    def __init__(self):
        super().__init__()
        self.labels = [
            chart_axis_left(2),
            chart_axis_left(4),
            chart_axis_left(6),
            chart_axis_left(8),
            chart_axis_left(10),
            chart_axis_left(12),
        ]
        self.labels_size = 40

class chart_title2(ft.ChartAxis):
    def __init__(self):
        super().__init__()
        self.labels = [
            chart_axis_bottom(position=0, hr_ago=6),
            chart_axis_bottom(position=2, hr_ago=5),
            chart_axis_bottom(position=4, hr_ago=4),
            chart_axis_bottom(position=6, hr_ago=3),
            chart_axis_bottom(position=8, hr_ago=2),
            chart_axis_bottom(position=10, hr_ago=1),
            chart_axis_bottom(position=12, hr_ago=0),
        ]
        self.labels_size = 32
        
        
class grid_line(ft.ChartGridLines):
    def __init__(self):
        super().__init__()
        self.interval = 1
        self.color = ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)
        self.width = 1

def grafico() -> ft.Container:
    card = container(
        ft.LineChart(
            data_series=[],
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=grid_line(),
            vertical_grid_lines=grid_line(),
            left_axis=chart_title(),
            bottom_axis=chart_title2(),
            min_y=0,
            max_y=12,
            min_x=0,
            max_x=12,
            expand=True
        )
    )
    return card