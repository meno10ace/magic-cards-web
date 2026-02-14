# --- 裏面 (画像) ---
            # 拡張子を除いたファイル名が単語と一致するものを探す
            found_file = None
            extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG'] # 探す拡張子のリスト
            
            for ext in extensions:
                target_name = f"{word}{ext}"
                # ZIP内の全ファイルをチェック（フォルダ階層も考慮）
                for f in file_list:
                    if f.endswith(f"/{target_name}") or f == target_name:
                        found_file = f
                        break
                if found_file:
                    break
            
            if found_file:
                img_data = z.read(found_file)
                img_io = io.BytesIO(img_data)
                # 画像を描画 (中央配置、アスペクト比維持)
                c.drawImage(Image.open(img_io), (width-400)/2, (height-400)/2, width=400, height=400, preserveAspectRatio=True)
            else:
                c.setFont("Helvetica-Bold", 50)
                c.drawCentredString(width / 2, height / 2, f"Not Found: {word}")
