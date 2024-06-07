"""
Aquí creare la card que mostrara el grafico con las estadisticas del cultivo
"""

import flet as ft


class chart_axis_left(ft.ChartAxisLabel):
    def __init__(self, position):
        super().__init__()
        self.value = position
        self.label = ft.Container(
            alignment=ft.alignment.center,
            margin=ft.margin.only(right=5),
            content=ft.Text(f"{position}m", size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT)
        )


class chart_axis_bottom(ft.ChartAxisLabel):
    def __init__(self, position: int, hr_ago: int):
        hr_ago = f"{hr_ago}H" if hr_ago != 0 else "NOW"

        if hr_ago == "NOW":
            time = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text(hr_ago, size=12, weight=ft.FontWeight.BOLD)
            )

        else:
            time = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(hr_ago, size=12, weight=ft.FontWeight.BOLD),
                        ft.Text("AGO", size=12, weight=ft.FontWeight.BOLD),
                    ]
                ),
            )

        time_label = ft.Container(
            content=time,
            margin=ft.margin.only(top=5, bottom=5),
        )

        super().__init__()
        self.value = position
        self.label = time_label


class chart_value(ft.ChartAxis):
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


class chart_time(ft.ChartAxis):
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
    from data import data_temperatura as data_series

    card = ft.LineChart(
        data_series=data_series,
        border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
        horizontal_grid_lines=grid_line(),
        vertical_grid_lines=grid_line(),
        left_axis=chart_value(),
        bottom_axis=chart_time(),
        min_y=0,
        max_y=12,
        min_x=0,
        max_x=12,
        expand=True,
    )

    return card
