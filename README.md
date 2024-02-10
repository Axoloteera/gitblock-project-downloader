# gitblock-project-downloader
野营作品下载器

## 如何解密野营作品?  

野营作品是AES加密的,来自野营前端源码`lib-player.min.js`的具体解密代码格式化后如下:  
```javascript
function(A) {
        try {
            var B = "4A9745825F24883B657AFC4E4626A0F2253D8DE48C2B32D85F26989E9BFF78B9"
              , g = CryptoJS.enc.Utf8.parse(B.substr(0, 32))
              , Q = CryptoJS.enc.Utf8.parse(B.substr(0, 16))
              , E = btoa(function(A) {
                for (var B = [], g = 0; g < A.length; g += 32768)
                    B.push(String.fromCharCode.apply(null, A.subarray(g, g + 32768)));
                return B.join("")
            }(A.data))
              , e = CryptoJS.AES.decrypt(E, g, {
                iv: Q,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            }).toString(CryptoJS.enc.Utf8);
            if ("{" == e.charAt(0))
                return e
        } catch (A) {}
        return A.decodeText()
    }
```  

因此,我们在js中可以使用`CryptoJS`, 并配置如下:  
![图片](https://github.com/Gtd232/gitblock-project-downloader/assets/79702405/8057ff58-4258-40d3-8378-d2a054f9fb24)  

密钥为`4A9745825F24883B657AFC4E4626A0F2`,偏移量为`4A9745825F24883B`.
