# sjtuAixinwuFan
绿色爱心屋批量自动登录工具

## 使用方法
退出爱心屋，用Jaccount重新登陆到爱心屋，按快捷键F12打开浏览器调试窗口，在Console选项卡中输入此行内容：
> **_document.cookie.split('; ').forEach(function(c){if(c.includes('JASiteCookie'))console.error(c)})_**

回车执行，红字部分即为cookies中JASiteCookie数据，记录了在爱心屋网站的登陆状态。将红字部分粘贴到此处（aixinwu.csv文件中），即开通自动登录服务。 
*风险提醒：JASiteCookie数据的拥有者可完全控制此爱心屋账号。*
