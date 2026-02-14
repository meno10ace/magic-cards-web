import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import io
import zipfile
from PIL import Image

st.title("🎨 手作り英単語カードメーカー")

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

        for word in words:
            # --- 表面 (英単語) ---
            c.setFont("Helvetica-Bold", 100)
            c.drawCentredString(width / 2, height / 2, word)
            c.showPage()

            # --- 裏面 (画像) ---
            found_file = None
            extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG']
            
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
                c.drawImage(Image.open(img_io), (width-400)/2, (height-400)/2, width=400, height=400, preserveAspectRatio=True)
            else:
                c.setFont("Helvetica-Bold", 50)
                c.drawCentredString(width / 2, height / 2, f"Not Found: {word}")
            
            c.showPage()

        c.save()
        
        st.success("画像付きPDFが完成しました！")
        st.download_button(
            label="完成したPDFを保存",
            data=buf.getvalue(),
            file_name="English_Cards.pdf",
            mime="application/pdf"
        )
