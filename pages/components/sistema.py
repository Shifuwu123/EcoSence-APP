import flet as ft
from decorators.app_class import containers_app_page as container

class responsive_row(ft.ResponsiveRow):
    def __init__(self, controls: list[ft.Control]):
        super().__init__()
        self.spacing=5
        self.columns=10
        self.alignment=ft.MainAxisAlignment.CENTER
        self.vertical_alignment=ft.CrossAxisAlignment.CENTER
        self.controls=controls

def system_info(rele1_txf, rele1_button, rele2_txf, rele2_button):
    card = ft.Card(
        color=ft.colors.GREEN_ACCENT_400,
        margin=10,
        elevation=2.0,
        col=1,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                container(
                    ft.Text("Sistema")
                ),
                container(
                    ft.Column(
                        controls=[
                            #Rele 1
                            responsive_row(
                                [
                                    rele1_txf,
                                    rele1_button,
                                ]
                            ),
                            
                            # Rele 2
                            responsive_row(
                                [
                                    rele2_txf,
                                    rele2_button,
                                ]
                            ),
                        ]
                    ),
                
                ),
            ],
        ),
    )

    return card
