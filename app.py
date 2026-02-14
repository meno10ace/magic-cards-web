import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import zipfile
import os
from PIL import Image

st.title("🎨 手作り英単語カードメーカー")

# --- フォントの設定 ---
font_path = "comicbd.ttf" 

if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('ComicSans', font_path))
    target_font = 'ComicSans'
else:
    target_font = 'Helvetica-Bold'
    st.warning(f"⚠️ {font_path} が見つかりません。標準フォントで作成します。")

col1, col2 = st.columns(2)
with col1:
    csv_file = st.file_uploader("1. 単語リスト(CSV)", type=['csv'])
with col2:
    zip_file = st.file_uploader("2. 画像まとめ(ZIP)", type=['zip'])

if csv_file and zip_file:
    df = pd.read_csv(csv_file, header=None)
    words = df[0].tolist()
    
    z = zipfile.ZipFile(zip_file)
    file_list = z.namelist()

    if st.button("PDFを作成する"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=landscape(A4))
        width, height = landscape(A4) # A4横のサイズを取得

        # 用紙の80%のサイズを計算
        draw_width = width * 0.8
        draw_height = height * 0.8
        
        # 中央に配置するための余白を計算
        margin_x = (width - draw_width) / 2
        margin_y = (height - draw_height) / 2

        for word in words:
            # --- 表面 (英単語) ---
            # 文字サイズを用紙の高さの約40%（巨大！）に設定
            c.setFont(target_font, height * 0.4)
            c.drawCentredString(width / 2, (height / 2) - (height * 0.1), str(word))
            c.showPage()

            # --- 裏面 (画像) ---
            found_file = None
            extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
            
            for ext in extensions:
                target_name = f"{word}{ext}"
                for f in file_list:
                    if f.endswith(f"/{target_name}") or f == target_name:
                        found_file = f
                        break
                if found_file:
                    break
            
            if found_file:
                img_data = z.read(found_file)
                img_io = io.BytesIO(img_data)
                img = Image.open(img_io)
                
                # 画像を用紙の80%の範囲に収まるように描画
                c.drawInlineImage(img, margin_x, margin_y, width=draw_width, height=draw_height, preserveAspectRatio=True)
            else:
                c.setFont(target_font, 50)
                c.drawCentredString(width / 2, height / 2, f"Not Found: {word}")
            
            c.showPage()

        c.save()
        
        st.success("80%サイズ調整版が完成しました！")
        st.download_button(
            label="完成したPDFを保存",
            data=buf.getvalue(),
            file_name="English_Cards_80percent.pdf",
            mime="application/pdf"
        )
