# USB/SDカードメディア復元ツール

USBやSDカードから直接シグネチャスキャンを行い、壊れたファイルも復元可能なPythonスクリプトです。JPEGファイルは終了マーカー（FFD9）が補完されます。

---

## 機能

* JPEG, PNG, GIF, MP4, CR2, NEF, ARW 形式に対応
* 壊れたファイルも保存し、JPEGは自動で終了マーカーを補完
* ファイルサイズが不明な場合はデフォルトサイズで切り出し
* 復元ファイルは `recovered_files` ディレクトリに出力

---

## 動作環境

* Python 3.x
* Windows または macOS
* 管理者権限（Windows PowerShell）／sudo 権限（macOS）が必要

---

## インストール方法

1. Python がインストールされていない場合は以下からインストール

   * [Python公式サイト](https://www.python.org/downloads/)

2. このリポジトリをクローンまたはスクリプトをダウンロード

   ```powershell
   git clone <リポジトリURL>
   cd <フォルダ名>
   ```

---

## 使用方法

### Windows（PowerShell）

1. **管理者権限で PowerShell を起動**

2. USB/SDカードの物理ドライブ番号を確認

   ```powershell
   Get-PhysicalDisk
   ```

   * またはディスク管理で確認
   * 例: `\\.\PhysicalDrive1`

3. スクリプトを実行

   ```powershell
   python .\recover_media.py \\.\PhysicalDrive1
   ```

4. 復元されたファイルは `recovered_files` フォルダに出力されます

---

### macOS

1. **ターミナルを開く**

2. USB/SDカードのデバイスパスを確認

   ```bash
   diskutil list
   ```

   * 例: `/dev/disk2`
   * 必要に応じてアンマウント

     ```bash
     sudo diskutil unmountDisk /dev/disk2
     ```

3. スクリプトを実行

   ```bash
   sudo python3 recover_media.py /dev/disk2
   ```

4. 復元されたファイルは `recovered_files` フォルダに出力されます

---

## 注意事項

* **必ず管理者権限／sudo 権限で実行**してください
* 読み取り専用で実行されますが、重要データは必ずバックアップを取ってから使用してください
* 大容量ドライブの場合、復元に時間がかかります
* 壊れたファイルは元の状態に完全に復元できない場合があります

---

## 出力例

```
[+] jpg_ok_0.jpg を復元
[+] png_partial_0.png を復元
JPG → 3 個復元完了
PNG → 2 個復元完了
GIF → 0 個復元完了
...
```
