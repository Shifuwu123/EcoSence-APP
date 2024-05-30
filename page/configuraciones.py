
def configuracion():
    return [
        ft.AppBar(title=ft.Text("Configuration")),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: page.go("/")
                        ),
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            "Go Statistics",
                            on_click=lambda _: page.go("/statistics"),
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]
