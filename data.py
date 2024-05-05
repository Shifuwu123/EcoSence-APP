import flet as ft
from graph_config import *

data_temperatura = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(0, 3.44),
            ft.LineChartDataPoint(2.6, 3.44),
            ft.LineChartDataPoint(4.9, 3.44),
            ft.LineChartDataPoint(6.8, 3.44),
            ft.LineChartDataPoint(8, 3.44),
            ft.LineChartDataPoint(9.5, 3.44),
            ft.LineChartDataPoint(11, 3.44),
        ],
        stroke_width=4,
        curved=True,
        stroke_cap_round=True,
        color=ft.colors.with_opacity(0.5, ft.colors.PINK),
    )
]

data_humedad = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(0.5, 1),
            ft.LineChartDataPoint(2, 3),
            ft.LineChartDataPoint(4.5, 2),
            ft.LineChartDataPoint(6, 4),
            ft.LineChartDataPoint(8, 3),
            ft.LineChartDataPoint(10, 5),
        ],
        stroke_width=4,
        curved=True,
        stroke_cap_round=True,
        color=ft.colors.WHITE,
    )
]

data_luz = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(0, 1),
            ft.LineChartDataPoint(2, 3),
            ft.LineChartDataPoint(4, 2),
            ft.LineChartDataPoint(6, 4),
            ft.LineChartDataPoint(8, 3),
            ft.LineChartDataPoint(10, 5),
        ],
        stroke_width=4,
        curved=True,
        stroke_cap_round=True,
        color=ft.colors.YELLOW,
    )
]

data_tierra = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(0.5, 2),
            ft.LineChartDataPoint(2.5, 3),
            ft.LineChartDataPoint(4.5, 4),
            ft.LineChartDataPoint(6.5, 5),
            ft.LineChartDataPoint(8.5, 4),
            ft.LineChartDataPoint(10.5, 3),
        ],
        stroke_width=4,
        curved=True,
        stroke_cap_round=True,
        color=ft.colors.BROWN,
    )
]

data_agua = [
    ft.LineChartData(
        data_points=[
            ft.LineChartDataPoint(0.2, 4),
            ft.LineChartDataPoint(2.4, 3),
            ft.LineChartDataPoint(4.6, 2),
            ft.LineChartDataPoint(6.8, 5),
            ft.LineChartDataPoint(8.2, 4),
            ft.LineChartDataPoint(10, 6),
        ],
        stroke_width=4,
        curved=True,
        stroke_cap_round=True,
        color=ft.colors.CYAN,
    )
]


grafico = {
    "Temperatura": data_temperatura,
    "Humedad": data_humedad,
    "Luz": data_luz,
    "Tierra": data_tierra,
    "Agua": data_agua,
}
