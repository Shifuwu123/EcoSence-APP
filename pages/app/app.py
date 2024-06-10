import flet as ft

class responsive_row(ft.ResponsiveRow):
    def __init__(self, controls: list[ft.Control], width: int):
        super().__init__()
        self.controls=controls,
        self.alignment=ft.MainAxisAlignment.CENTER,
        self.vertical_alignment=ft.CrossAxisAlignment.CENTER,
        # Hacer la pagina responsiva
        self.columns=2,
        self.spacing=15,
        self.run_spacing=5,
        self.width=width,
    

def app_page(info_crop, info_system, info_params, info_stats, width):
    info_crop.col = {"xs": 2, "md":1}
    info_system.col = {"xs": 2, "md":1}
    info_params.col = {"xs": 2, "md":1}
    info_stats.col = {"xs": 2, "md":1}

    return [
        ft.AppBar(title=ft.Text("EcoSense - SYSTEM ONLINE")),
        ft.ListView(
            expand=1,
            spacing=10,
            controls=[
                responsive_row(
                    controls=[info_crop, info_system],
                    width=width,
                ),
                responsive_row(
                    controls=[info_params, info_stats],
                    width=width,
                ),
            ]
        ),
    ]