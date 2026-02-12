# [2021] 檔案上傳到件 Uploadify 升級到 UploadiFive 的筆記

> **原文發布日期:** 2021-03-12
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/12/UploadiFive
> **標籤:** 無

---

微軟於2021年透過Windows更新全面禁止IE使用Flash

因此使用 swf 的 Uploadify 需要更新成 html5 的 UploadiFive

比較大的問題是檔案類型過濾在這版本其實有問題

UploadiFive  'fileType' filter does not work

這邊筆記下遇到的坑順便提供修正後的版本

原本Uploadify的網站目前已經收掉了

現在會轉址到作者的 Github

https://github.com/RonnieSan/uploadify

好像原本是有收費版，目前看來已經開源免費提供了

目前版本停在 1.2.3 (2020/1)

因為 flash 已經停止支援

作者已經不提供舊版程式

目前只提供 html5 版本的 UploadiFive

原本用舊IE還可以苟延殘喘

現在因為強制讓ie禁用flash

所以變成強制要更新到 h5 版本

基本使用方式可以參考官方範例

https://github.com/RonnieSan/uploadify/blob/master/index.php

```

<form>
 <div id="queue"></div>
 <input id="file_upload" name="file_upload" type="file" multiple="true">
 <a style="position: relative; top: 8px;" href="javascript:$('#file_upload').uploadifive('upload')">Upload Files</a>
</form>
```

對應關係大致如下

[HTML] div id => [JS] 'queueID' : 'queue'

[HTML] input id => [JS] $('#file\_upload') => [HTML] a href="javascript:$('#file\_upload')

其中 href 後面的 uploadifive('upload') 其實是去呼叫 uploadifive 的 upload 方法 (其他還有 clear 之類的)

```

$(function() {
 $('#file_upload').uploadifive({
  'auto'             : false,
  'checkScript'      : 'check-exists.php',
  'formData'         : {'folder': 'uploadFile'},
  'queueID'          : 'queue',
  'uploadScript'     : 'uploadifive.php',
  'onUploadComplete' : function(file, data) { console.log(data); }
 });
});
```

JS 部分

- checkScript 如果沒有要檢查是否重複可以整個拿掉 (因為我是升級舊版本，原本就沒有實作這個功能)
- formData 因為舊版有 folder 這個設定，所以新版可以加在這邊無痛轉移，不然會少post參數到server端
- uploadScript 這邊設改成你server端處理上傳檔案個那隻程式，C# 可能類似 uploadifive.ashx 這種檔案
- onUploadComplete 是上傳完成後的處理，回傳參數比舊版少了不少，只剩下 file 跟 data 兩個參數
  file跟原本依樣可以拿size,name...等等，data就是server端回傳的資料，有需要可以自己 console.log 瞧瞧

其他設定部分可以到 js 原始檔內看註解

https://github.com/RonnieSan/uploadify/blob/master/jquery.uploadifive.js

Options 部分如下

```

'auto'            : true,               // Automatically upload a file when it's added to the queue
'buttonClass'     : false,              // A class to add to the UploadiFive button
'buttonText'      : 'Select Files',     // The text that appears on the UploadiFive button
'checkScript'     : false,              // Path to the script that checks for existing file names
'dnd'             : true,               // Allow drag and drop into the queue
'dropTarget'      : false,              // Selector for the drop target
'fileObjName'     : 'Filedata',         // The name of the file object to use in your server-side script
'fileSizeLimit'   : 0,                  // Maximum allowed size of files to upload
'fileType'        : false,              // Type of files allowed (image, etc), separate with a pipe character |
'formData'        : {},                 // Additional data to send to the upload script
'height'          : 30,                 // The height of the button
'itemTemplate'    : false,              // The HTML markup for the item in the queue
'method'          : 'post',             // The method to use when submitting the upload
'multi'           : true,               // Set to true to allow multiple file selections
'overrideEvents'  : [],                 // An array of events to override
'queueID'         : false,              // The ID of the file queue
'queueSizeLimit'  : 0,                  // The maximum number of files that can be in the queue
'removeCompleted' : false,              // Set to true to remove files that have completed uploading
'simUploadLimit'  : 0,                  // The maximum number of files to upload at once
'truncateLength'  : 0,                  // The length to truncate the file names to
'uploadLimit'     : 0,                  // The maximum number of files you can upload
'uploadScript'    : 'uploadifive.php',  // The path to the upload script
'width'           : 100                 // The width of the button
```

Event部分如下

```

'onAddQueueItem'   : function(file) {},                        // Triggered for each file that is added to the queue
'onCancel'         : function(file) {},                        // Triggered when a file is cancelled or removed from the queue
'onCheck'          : function(file, exists) {},                // Triggered when the server is checked for an existing file
'onClearQueue'     : function(queue) {},                       // Triggered during the clearQueue function
'onDestroy'        : function() {}                             // Triggered during the destroy function
'onDrop'           : function(files, numberOfFilesDropped) {}, // Triggered when files are dropped into the file queue
'onError'          : function(file, fileType, data) {},        // Triggered when an error occurs
'onFallback'       : function() {},                            // Triggered if the HTML5 File API is not supported by the browser
'onInit'           : function() {},                            // Triggered when UploadiFive if initialized
'onQueueComplete'  : function() {},                            // Triggered once when an upload queue is done
'onProgress'       : function(file, event) {},                 // Triggered during each progress update of an upload
'onSelect'         : function() {},                            // Triggered once when files are selected from a dialog box
'onUpload'         : function(file) {},                        // Triggered when an upload queue is started
'onUploadComplete' : function(file, data) {},                  // Triggered when a file is successfully uploaded
'onUploadFile'     : function(file) {},                        // Triggered for each file being uploaded
```

其中比較有問題的是

`'fileType'        : false,              // Type of files allowed (image, etc), separate with a pipe character |`

官方範例： `'fileType' : 'image/png',`

這裡列舉一下我踩到的幾個坑

1. **jquery.uploadifive.min.js** 這隻壓縮的JS其實不能跑！
   這隻壓縮的JS其實不能跑！
   不能跑！！！
   https://github.com/RonnieSan/uploadify/blob/master/Sample/jquery.uploadifive.min.js
   直接跑你會拿到以下錯誤
   `​jquery.uploadifive.min.js:6 Uncaught TypeError: Cannot set property '$e' of undefined`
   https://github.com/RonnieSan/uploadify/issues/9
   解法：你需要自行拿原版去壓一次！
   https://javascript-minifier.com/
2. 這段檢查只有在拖曳檔案內實作，直接開檔案總管選擇檔案是不會檢查附檔名的
3. 這邊是用 | 這個破折號來做多類型的分隔符號，但這不受瀏覽器支援，
   導致你用檔案總管選擇檔案的時候會找不到檔案，要自己切成 \*.\* 才看得到你要上傳的檔案。
   舉例來說你設定 `image/png|image/jpg` ，預設只會顯示 `*.image/png|image/jpg` ，這副檔名的檔案
   因為不可能會有這副檔名，所以你只會看到一堆資料夾但看不到你的jpg檔案，你要手動切換成 \*.\* 才看得到
4. 使用 file.type 來檢查是否符合你設定的值，但這個屬性其實很多檔案類型 JS 會回傳空值，
   因為 `'' != 'image/png'` ，導致諸如 RAR,7Z,PDF...等等檔案皆無法正常上傳。

解法只能自己改檢查機制，再一併補到非拖曳上傳的那個 function

這裡提供我修正的版本 UploadiFive 1.3.0

https://github.com/jakeuj/uploadify

或是參考我修改的內容自己改一遍也可以

https://github.com/jakeuj/uploadify/commit/eab99ef4cb369dc96dca3df0695380635e93d230#diff-592cf5afcbc4be0f76b563c92b6158157ecb645ec10094ed31f6c6c9fc05a26e

使用上最大差別是

**fileType** 這個參數改用 [**副檔名]** 來定義，並且分隔符號改成 [**逗號 ,]** 分隔

`'fileType' : '.jpg,.jpeg,.gif,.png'`

參考範例

https://github.com/jakeuj/uploadify/blob/master/Sample/index.php

大致先這樣，希望有幫到同是天涯淪落人

參考來源：

https://stackoverflow.com/questions/23399306/uploadifive-1-2-2-filetype-filter-capability-restriction-does-not-work

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- HTML
- Javascript
- jQuery
- UploadiFive
- Uploadify

- 回首頁

---

*本文章從點部落遷移至 Writerside*
