import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import io

st.title("🎨 手作り英単語カードメーカー")
st.write("CSVをアップロードするだけで、可愛いカードPDFが作れます。")

# --- 設定エリア ---
uploaded_file = st.file_uploader("単語リスト(CSV)を選んでください", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file, header=None)
    words = df[0].tolist()
    
    if st.button("PDFを作成する"):
        # メモリ上にPDFを作成
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=landscape(A4))
        width, height = landscape(A4)

        for word in words:
            # 表面
            c.setFont("Helvetica-Bold", 100) # ウェブ版はまず標準フォントで
            c.drawCentredString(width / 2, height / 2, word)
            c.showPage()
            # 裏面（一旦、文字だけ。画像は後で連携可能！）
            c.setFont("Helvetica-Bold", 50)
            c.drawCentredString(width / 2, height / 2, f"(Image of {word})")
            c.showPage()

        c.save()
        
        # ダウンロードボタンを表示
        st.success("PDFが完成しました！")
        st.download_button(
            label="PDFをダウンロード",
            data=buf.getvalue(),
            file_name="English_Cards.pdf",
            mime="application/pdf"
        )