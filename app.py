import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
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
        width, height = landscape(A4)

        # 描画可能エリアの計算 (用紙の80%)
        limit_w = width * 0.8
        limit_h = height * 0.8
        margin_x = (width - limit_w) / 2
        margin_y = (height - limit_h) / 2

        for word in words:
            word_str = str(word)
            # --- 表面 (英単語) ---
            # 文字サイズを自動調整
            max_font_size = height * 0.4 # 最大サイズ
            current_font_size = max_font_size
            
            # 横幅が 80% 枠に収まるまでフォントを小さくする
            while current_font_size > 10:
                text_width = stringWidth(word_str, target_font, current_font_size)
                if text_width <= limit_w:
                    break
                current_font_size -= 5
            
            c.setFont(target_font, current_font_size)
            # 上下の位置も中央に来るように少し調整
            c.drawCentredString(width / 2, (height / 2) - (current_font_size / 3), word_str)
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
                if found_file: break
            
            if found_file:
                img_data = z.read(found_file)
                img_io = io.BytesIO(img_data)
                img = Image.open(img_io)
                c.drawInlineImage(img, margin_x, margin_y, width=limit_w, height=limit_h, preserveAspectRatio=True)
            else:
                c.setFont(target_font, 50)
                c.drawCentredString(width / 2, height / 2, f"Not Found: {word}")
            
            c.showPage()

        c.save()
        st.success("文字サイズ自動調整版が完成しました！")
        st.download_button(label="完成したPDFを保存", data=buf.getvalue(), file_name="English_Cards_AutoFit.pdf", mime="application/pdf")
