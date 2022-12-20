# 衛服部醫事查詢系統爬蟲
* python:3.10-slimAlpine
* tesseract-ocr Version latest
* google chromium Version latest

### 簡介:
衛服部醫事查詢系統爬蟲

### 使用方式
<pre> docker build . </pre>
該 images 資料庫，請於 env_config.py 內設定相關參數

### 注意事項
該爬蟲除了需要使用到 google chromium 還需要安裝 tesseract-ocr 作為驗證碼辨識引擎
