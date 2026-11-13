import flet as ft

def main(page: ft.Page):
    page.title = "Liquid Glass UI"
    page.padding = 0
    page.bgcolor = "#0F172A"

    # 1. Colorful background elements to refract through the glass
    background = ft.Stack(
        [
            ft.Container(
                width=260,
                height=260,
                border_radius=130,
                gradient=ft.LinearGradient(
                    colors=["#EC4899", "#8B5CF6"],
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                ),
                top=80,
                left=-40,
            ),
            ft.Container(
                width=220,
                height=220,
                border_radius=110,
                gradient=ft.LinearGradient(
                    colors=["#06B6D4", "#3B82F6"],
                    begin=ft.Alignment.TOP_RIGHT,
                    end=ft.Alignment.BOTTOM_LEFT,
                ),
                bottom=100,
                right=-30,
            ),
        ],
        expand=True,
    )

    # 2. The Liquid Glass Card
    glass_card = ft.Container(
        width=320,
        padding=24,
        border_radius=28,
        blur=ft.Blur(20, 20, ft.BlurTileMode.MIRROR),
        bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
        border=ft.Border.all(1.5, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=24,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            [
                ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.WHITE, size=36),
                ft.Text(
                    "Liquid Glass",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Real-time backdrop blur with specular highlights running in Python.",
                    size=14,
                    color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                ),
                ft.Container(height=10),
                ft.Button(
                    "Continue",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=16),
                    ),
                ),
            ],
            tight=True,
        ),
    )

    page.add(
        ft.Stack(
            [
                background,
                ft.Container(content=glass_card, alignment=ft.Alignment.CENTER, expand=True),
            ],
            expand=True,
        )
    )

ft.run(main)

