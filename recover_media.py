# -*- coding: utf-8 -*-
# USBやSDカードから直接シグネチャスキャンで復元（壊れたファイルも保存・JPEGはFFD9補完）

import sys
import os

def recover_files(device_path):
    output_dir = "recovered_files"
    os.makedirs(output_dir, exist_ok=True)

    # シグネチャ定義: (開始, 終端, デフォルトサイズ)
    signatures = {
        "jpg": (b"\xff\xd8", b"\xff\xd9", 5 * 1024 * 1024),   # 5MB 仮
        "png": (b"\x89PNG\r\n\x1a\n", b"IEND\xaeB`\x82", 3 * 1024 * 1024),
        "gif": (b"GIF", b"\x00;", 2 * 1024 * 1024),
        "mp4": (b"ftyp", b"moov", 32 * 1024 * 1024),
        "cr2": (b"\x49\x49\x2a\x00", b"", 64 * 1024 * 1024),
        "nef": (b"\x49\x49\x2a\x00", b"", 64 * 1024 * 1024),
        "arw": (b"\x49\x49\x2a\x00", b"", 64 * 1024 * 1024),
    }

    chunk_size = 1024 * 1024  # 1MBずつ読み込み
    buffer = b""
    file_count = {ext: 0 for ext in signatures}

    with open(device_path, "rb", buffering=0) as f:
        while True:
            try:
                chunk = f.read(chunk_size)
            except Exception as e:
                print(f"[!] 読み取りエラー: {e}")
                break

            if not chunk:
                break

            buffer += chunk
            if len(buffer) > chunk_size * 4:
                buffer = buffer[-chunk_size*4:]

            for ext, (sig_start, sig_end, default_size) in signatures.items():
                s = buffer.find(sig_start)
                while s != -1:
                    recovered = False
                    if sig_end:
                        e = buffer.find(sig_end, s + len(sig_start))
                        if e != -1:
                            # 正常に終端が見つかった場合
                            e += len(sig_end)
                            file_name = os.path.join(output_dir, f"{ext}_ok_{file_count[ext]}.{ext}")
                            with open(file_name, "wb") as out:
                                out.write(buffer[s:e])
                            file_count[ext] += 1
                            recovered = True
                            buffer = buffer[e:]
                        else:
                            # 壊れている場合 → デフォルトサイズで切り出し
                            if len(buffer) - s >= default_size:
                                file_name = os.path.join(output_dir, f"{ext}_broken_{file_count[ext]}.{ext}")
                                with open(file_name, "wb") as out:
                                    chunk_data = buffer[s:s+default_size]
                                    # JPEG の場合は終了マーカーを補完
                                    if ext == "jpg" and not chunk_data.endswith(b"\xff\xd9"):
                                        chunk_data += b"\xff\xd9"
                                    out.write(chunk_data)
                                file_count[ext] += 1
                                recovered = True
                                buffer = buffer[s+default_size:]
                            else:
                                # 🔽 ここを追加：バッファの終端まで保存して強制補完
                                if ext == "jpg" and len(buffer) - s > 1024:
                                    file_name = os.path.join(output_dir, f"{ext}_truncated_{file_count[ext]}.{ext}")
                                    with open(file_name, "wb") as out:
                                        chunk_data = buffer[s:]
                                        if not chunk_data.endswith(b"\xff\xd9"):
                                            chunk_data += b"\xff\xd9"
                                        out.write(chunk_data)
                                    file_count[ext] += 1
                                    recovered = True
                                    buffer = b""  # バッファを空にする
                    else:
                        # 終端不明形式は固定サイズで切り出す
                        if len(buffer) - s >= default_size:
                            file_name = os.path.join(output_dir, f"{ext}_partial_{file_count[ext]}.{ext}")
                            with open(file_name, "wb") as out:
                                out.write(buffer[s:s+default_size])
                            file_count[ext] += 1
                            recovered = True
                            buffer = buffer[s+default_size:]

                    if recovered:
                        print(f"[+] {file_name} を復元")
                        s = buffer.find(sig_start)
                    else:
                        break

    for ext in file_count:
        print(f"{ext.upper()} → {file_count[ext]} 個復元完了")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("win使い方: 管理者権限で python recover_media.py \\\\.\\PhysicalDriveN")
        sys.exit(1)

    recover_files(sys.argv[1])
