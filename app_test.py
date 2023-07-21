import os
import folium
import pandas as pd
from time import sleep as slp
from selenium import webdriver
import glob
from selenium.webdriver.chrome.options import Options
import IPython
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="位置情報履歴可視化ツール",
    page_icon="🗾",
    layout="wide"
)

# タイトル。最もサイズが大きい。ページタイトル向け
st.title('あなたの位置情報履歴を可視化')

# ヘッダ。２番目に大きい。項目名向け
st.header('あなたの軌跡を')

# 普通のテキスト。Html や Markdown のパースをしない。
st.text('ここでは緯度や経度を記録したCSVファイルを読み取り、あなたの行動を地図上で可視化できます。')
st.text('※エラー表示が出ていますが、ファイルがないため起こるものであり、アップロードしていただければ通常通りご使用いただけます')

# ファイルアップローダー
data = st.file_uploader("Choose a file",type="csv")

if data is not None:
  # データの読み込み
  data = pd.read_csv(data)
  # 人物のリスト
  person_list = data["person"].unique()
  # 地図オブジェクトの作成
  map = folium.Map(tiles='OpenStreetMap')
  color_list=['red','blue','green','purple','orange','darkred','lightred','beige','darkblue','darkgreen','cadetblue','darkpurple','white','pink','lightblue','lightgreen','gray','black','lightgray']
  color_list=["purple"]
  # 各人物の軌跡を追加
  for idx, person in enumerate(person_list):
    data_temp = data[data["person"] == person]
    data_temp_lat_lon = data_temp[["緯度", "経度"]]
    locs = data_temp_lat_lon.values
    line_color = color_list[idx % len(color_list)]
    folium.PolyLine(locs, color=line_color, popup=person).add_to(map)
  # 地図の範囲を調整
  map.fit_bounds([[data["緯度"].min(), data["経度"].min()], [data["緯度"].max(), data["経度"].max()]])
  # 地図を表示
  st_folium(map, width=1200, height=800)
