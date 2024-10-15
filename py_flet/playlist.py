import flet as ft

def main(page: ft.Page):
    page.title = "My Favorite Music"
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.PINK
    )
    img = ft.Image(
        src="https://storage.googleapis.com/spotifynewsroom-jp.appspot.com/1/2020/12/Spotify_Icon_RGB_Green.png",
        width=100,
        height=100,
    )
    row = ft.Row(
        controls=[
            img,
            ft.FilledButton(text="るーずの好きな曲", url="https://open.spotify.com/playlist/0Xq3Nvbh5mkcTAbv73v0nt"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    page.add(
        row,
    )


ft.app(main)