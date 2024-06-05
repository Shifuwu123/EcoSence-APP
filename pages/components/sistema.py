import flet as ft


def system_info(rele1_txf, rele1_button, rele2_txf, rele2_button):
    return ft.Container(
        bgcolor=ft.colors.GREEN,
        height=305,
        padding=10,
        alignment=ft.alignment.center,
        col=1,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_600,
                    padding=15,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("System"),
                ),
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_600,
                    padding=15,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.ResponsiveRow(
                                spacing=5,
                                columns=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    rele1_txf,
                                    rele1_button,
                                ],
                            ),
                            ft.ResponsiveRow(
                                spacing=5,
                                columns=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    rele2_txf,
                                    rele2_button,
                                ],
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
