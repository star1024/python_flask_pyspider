這是個鼎邦專案(爬蟲部分)
=============
*python版本3.6*  
*採用Pyspider與Flask架構*
*工作流程為客戶執行爬取請求存入資料庫,並透過介面查詢執行狀態*

##1.目錄結構
*Flask框架*  
```
*main.py :為啟動服務器,static & templates資料夾存放HTML檔*
*client.py :為取得main.py參數->餵給pysipder服務器*
```

*std folder*  
```
*存放pysipder腳本*
*以券商分類*
| Ａ證券   | Ｂ證券  |
| --------|:------:|
| 網頁表格1| 網頁表格1|
| 網頁表格2| 網頁表格2|
```

*tests folder* 
```
單元測試腳本
```