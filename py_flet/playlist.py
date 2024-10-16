import flet as ft
import os
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# id取得
my_id = os.getenv("my_id")
my_secret = os.getenv("my_secret")

# spotify apiでアクセストークンを取得
ccm = SpotifyClientCredentials(client_id = my_id, client_secret = my_secret)
sp = spotipy.Spotify(client_credentials_manager = ccm)

# プレイリストidの取得
playlist_id = "0Xq3Nvbh5mkcTAbv73v0nt"
def get_to_playlist(playlist_id):
    url = sp.playlist(playlist_id)

# プレイリストの曲を取得
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    return results["items"]

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
    
    # スクロール可能
    list_view = ft.ListView(expand=True, spacing=10)
    
    # プレイリストの曲を取得
    tracks = get_playlist_tracks(playlist_id)
    
    # 曲 アーティスト ジャケット
    for item in tracks:
        track = item["track"]
        track_name = track["name"]
        artist_name = ", ".join([artist["name"] for artist in track["artists"]])
        album_images = track["album"].get("images", [])
        
        # ジャケットの解像度の高い画像を選択
        album_images_url = album_images[0]["url"]
        
        # 画像とテキストを表示
        row = ft.Row(
            [
                ft.Image(src=album_images_url, width=100, height=100),
                ft.Text(f"{track_name} - {artist_name}")
            ],
        )
        list_view.controls.append(row)
        
    page.add(list_view)


ft.app(main)