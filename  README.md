這是個鼎邦專案(爬蟲部分)
=============
* python版本3.6  
* 採用Pyspider與Flask架構
* 工作流程為客戶執行爬取請求存入資料庫,並透過介面查詢執行狀態

1.目錄結構
-------------
>Flask框架 
```
* main.py 為啟動服務器,static & templates資料夾存放HTML檔
* client.py 為取得main.py參數->餵給pysipder服務器
```

>std folder

```
* 存放pysipder腳本

* 以券商分類
| Ａ證券   | Ｂ證券  |
| --------|:------:|
| 網頁表格1| 網頁表格1|
| 網頁表格2| 網頁表格2|

* model.py模組化腳本內容
```

>tests folder 
```
單元測試腳本
```

2.modules的引用
-------------
* 使用 absolute imports 引用其他 modules, spy.std.model
* .pth添加專案路徑讓pyspider框架可import使用專案腳本
```
from spy.std.yuanta_folder import yuanta

from importlib import reload
reload(yuanta)

class Handler(yuanta.Handler):
   
    pass
```

3.其他維護內容
-------------
>chromedriver需不定期因應瀏覽器版本更新.exe檔[chromedriver downloads](https://chromedriver.chromium.org/downloads)

>pyspider常見錯誤因素
* TimeoutError(pyspider.resultdb):沒抓到資料/帳號密碼錯誤
* NameError(pyspider.taskdb):程式碼出現錯誤