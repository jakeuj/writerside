# HttpClient

筆記下透過 .http 上傳檔案的方法

## 使用 `multipart/form-data` 上傳檔案

```
POST https://asia-east1-test-403908.cloudfunctions.net/test
Content-Type: multipart/form-data; boundary=boundary

--boundary
Content-Disposition: form-data; name="file"; filename="test.pdf"

// The 'input.txt' file will be uploaded

< D:\test.pdf
```