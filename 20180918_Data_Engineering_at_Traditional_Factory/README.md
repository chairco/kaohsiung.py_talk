## async 資料工程 await Serial port


邁入工業 4.0 中如何從設備裡擷取訊息進行數據分析並產生有用的回饋是重要任務。工廠設備裡使用 Serial port 串接硬體資料是常見的介面，本次 talk 分享將會介紹為何會使用 Python asyncio 函式庫來建構橋接 Serial port 的資料工程以及過程中遭遇的問題及解決方法。


+ [活動網址](https://www.meetup.com/Kaohsiung-Python-Meetup/events/254619272/?rv=ea1_v2&_xtd=gatlbWFpbF9jbGlja9oAJDE1Y2VjOGVhLTJlMGEtNGM3MS05YmRlLTQ4MDZhOWI0ZTEwZg)

+ [投影片](https://slides.com/chairco/async_await_serialport/)


## 範例環境設定


本次分享共有: 

1. Django 建立的 server 環境
2. client 可以運作實際以及模擬 serail port 環境


### 套件安裝

本次使用出色的 pipenv 最為套件管理，預設環境為 Python 3.7.0，請先確認電腦上已經安裝 Python 3.7.0 的版本，接著開始安裝所需要的套件:

```
pipenv install
```

### 設定 Server:

```
# 進入 Django 資料夾
cd server/src

# 建立資料庫
python manager.py migrate

# 建立超級管理者
python manager.py createsuperuser

# 將 server 跑起來
python manager.py runserver
```


### 設定資料庫:

打開瀏覽器進入[](http://localhost:8000/admin/boards/device/)建立 Device Table 的資料。
因為 table fk 關係，模擬的 client 會需要 Device 預設有兩筆資料如下(內容不一定要相同):

![#](https://imgur.com/a/Dc2Q30d)


### Client 端測試:

開啟新的`終端機`視窗接著到 client 資料夾底下，並試著執行 help 確認如下圖顯示

```
cd client
python mock.py --help
```

![#](https://imgur.com/a/XhcLes0)


接著可以執行模擬，假裝 serail port 送資料到 server，先試著送 20 筆吧

```
python mock.py --num 20
```

同時可以把網頁切換到[儀表板](http://localhost:8000/boards/dashboard/)看看圖形收到資料後是否有改變: 

![#](http://recordit.co/4hzoaFgxYb)