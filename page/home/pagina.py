import flet as ft

def main(page: ft.Page):
    page.title = "Connect to WiFi"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 530
    page.window_always_on_top = True

    ssid_field = ft.TextField(
        label="SSID",
        border_radius=8,
        border_color=ft.colors.GREEN,
        focused_border_color=ft.colors.GREEN,
        cursor_color=ft.colors.GREEN
    )

    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        border_radius=8,
        border_color=ft.colors.GREEN,
        focused_border_color=ft.colors.GREEN,
        cursor_color=ft.colors.GREEN
    )

    def check_connection(e):
        ssid = ssid_field.value
        password = password_field.value
        print(f'SSID: {ssid}')
        print(f'Password: {password}')


    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Connect to WiFi",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREEN,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Enter your WiFi network details to connect.",
                            size=14,
                            color=ft.colors.LIGHT_GREEN_ACCENT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ssid_field,
                        password_field,
                        ft.ElevatedButton(
                            text="Check Connection",
                            on_click=check_connection,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.GREEN,
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                ),
                padding=16,
                border_radius=8,
                bgcolor=ft.colors.GREY_900,
                alignment=ft.alignment.center,
            ),
            color=ft.colors.GREEN,
            elevation=4,
        )
    )

ft.app(target=main)
