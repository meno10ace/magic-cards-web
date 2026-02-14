import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import io
import zipfile  # ZIPを扱うための道具
from PIL import Image # 画像サイズを確認するための道具

st.title("🎨 手作り英単語カードメーカー (画像ZIP対応版)")

# --- ファイルアップロードエリア ---
col1, col2 = st.columns(2)
with col1:
    csv_file = st.file_uploader("1. 単語リスト(CSV)", type=['csv'])
with col2:
    zip_file = st.file_uploader("2. 画像まとめ(ZIP)", type=['zip'])

if csv_file and zip_file:
    # 1. CSVとZIPの中身を読み込む
    df = pd.read_csv(csv_file, header=None)
    words = df[0].tolist()
    
    # ZIPファイルをメモリ上で展開
    z = zipfile.ZipFile(zip_file)
    file_list = z.namelist() # ZIPの中に入っているファイル名の一覧

    if st.button("PDFを作成する"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=landscape(A4))
        width, height = landscape(A4)

        for word in words:
            # --- 表面 (英単語) ---
            c.setFont("Helvetica-Bold", 100)
            c.drawCentredString(width / 2, height / 2, word)
            c.showPage()

            # --- 裏面 (画像) ---
            img_name = f"{word}.png" # 「単語名.png」という名前を探す
            
            # ZIPの中に該当するファイル名があるか確認
            if img_name in file_list:
                img_data = z.read(img_name) # 画像データを読み込む
                img_io = io.BytesIO(img_data)
                # 画像を描画 (中央に配置)
                c.drawImage(Image.open(img_io), (width-400)/2, (height-400)/2, width=400, height=400, preserveAspectRatio=True)
            else:
                c.setFont("Helvetica-Bold", 50)
                c.drawCentredString(width / 2, height / 2, f"(No Image: {word}.png)")
            
            c.showPage()

        c.save()
        
        st.success("画像付きPDFが完成しました！")
        st.download_button(
            label="完成したPDFを保存",
            data=buf.getvalue(),
            file_name="FlashCards_with_Images.pdf",
            mime="application/pdf"
        )
