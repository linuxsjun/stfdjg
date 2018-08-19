
## 企业微信扫码认证

#### 发送
* appid         企业微信的CorpID
* agentid       授权方的网页应用ID
* redirect_uri  重定向地址，需要进行UrlEncode
* state         (非必需)用于保持请求和回调的状态，授权请求后原样带回给企业。该参数可用于防止csrf攻击（跨站请求伪造攻击），建议企业带上该参数，可设置为简单的随机数加session进行校验
```angular2html
https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=ww74c5af840cdd5cb6&agentid=1000013&redirect_uri=http://127.0.0.1:8000/pure_list/&state=web_login@gyoss9
```
#### 扫码&同意 & 网页跳转

```angular2html
通过返回
redirect_uri?code=CODE&state=STATE

未通过返回
redirect_uri?state=STATE

```
#### 获取用户userid
```angular2html
https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE
https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=iMkZJU69HN8OJcYmF9nluCdrtA4FyuU93bNnx_u9eDPcsd2k_X1mHujHy9N2aFD-E8wYgY4A8kxqJuVR30uKk72T8m8dP5LA7ZIhLuD9NT3e1APSXZilVwob8yGFNELwGxlV5xsZL2pQOpLIVLlLud33UvnC2wAbB5vi93bpJ3buLnjOB9yjlrbY4IFCrFqhe1e-oqCnS6QF-mbvnF5vdQ&code=eDJ5sv-wr5JYKDZAQxRCRIOZFOefK2Kalhd5ncy-4cw
```
#### 返回JSON
```angular2html
    {
       "errcode": 0,
       "errmsg": "ok",
       "UserId":"USERID",
    }
```