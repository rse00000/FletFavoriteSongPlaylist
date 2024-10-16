import flet as ft
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# id取得
my_id = os.getenv("my_id")
my_secret = os.getenv("my_secret")

# spotify apiでアクセストークンを取得
ccm = SpotifyClientCredentials(client_id=my_id, client_secret=my_secret)
sp = spotipy.Spotify(client_credentials_manager=ccm)

# プレイリストのURL
spotify_standard_url = "https://open.spotify.com/playlist/"

def main(page: ft.Page):
    page.title = "My Favorite Music"
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PINK)

    url_input = ft.TextField(label="Enter URL", hint_text="urlを入力してね!")
    playlist_id = ""  # グローバルに使えるようにプレイリストIDを定義

    def add_url(e):
        nonlocal playlist_id  # 外部スコープのplaylist_idを使用
        url = url_input.value

        if spotify_standard_url in url:
            playlist_id = url.replace(spotify_standard_url, "")
            page.add(get_playlist_display(playlist_id))  # プレイリストの表示を更新

        page.update()

    url_field = ft.Row(
        controls=[
            url_input,
            ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_url),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    page.add(url_field)

    # プレイリストの曲を取得
    def get_playlist_tracks(playlist_id):
        results = sp.playlist_tracks(playlist_id)
        return results["items"]

    def get_playlist_display(playlist_id):
        list_view = ft.ListView(expand=True, spacing=10)
        tracks = get_playlist_tracks(playlist_id)

        # 曲 アーティスト ジャケット
        for item in tracks:
            track = item["track"]
            track_name = track["name"]
            artist_name = ", ".join([artist["name"] for artist in track["artists"]])
            album_images = track["album"].get("images", [])

            # ジャケットの解像度の高い画像を選択
            album_images_url = album_images[0]["url"] if album_images else ""

            # アルバムのリンクを取得
            album_link = track["external_urls"]["spotify"]

            # 画像とテキストを中央揃えして表示する行を作成
            track_row = ft.Row(
                controls=[
                    ft.IconButton(
                        content=ft.Image(album_images_url, width=100, height=100),
                        tooltip="アルバムを開く",
                        on_click=lambda e, link=album_link: page.launch_url(link),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                track_name,
                                max_lines=2,  # 曲名が長い場合は2行まで表示
                                width=200,    # テキスト部分の固定幅を設定
                                overflow=ft.TextOverflow.ELLIPSIS,  # 長い場合は省略
                                text_align=ft.TextAlign.CENTER,  # テキストを中央揃え
                            ),
                            ft.Text(
                                artist_name,
                                max_lines=1,  # アーティスト名は1行で表示
                                width=200,    # テキスト部分の固定幅を設定
                                overflow=ft.TextOverflow.ELLIPSIS,  # 長い場合は省略
                                text_align=ft.TextAlign.CENTER,  # テキストを中央揃え
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # テキストを縦方向で中央揃え
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # 画像とテキストを中央揃えで横に配置
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 行全体を垂直方向で中央揃え
            )
            list_view.controls.append(track_row)  # リストに曲の行を追加
            
        return list_view

    # 初期表示
    page.update()

ft.app(main)
