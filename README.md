# fuckncov
中国人民大学疫情防控通自动打卡工具docker版

<h3>
  使用方法
</h3>
<div>
  在一台安装了docker的x86服务器上执行以下命令<br>
</div>


<code>
  docker run -d --name='fuckncov' --env TZ='Asia/Shanghai' --env USERNAME='你的账号' --env PASSWORD='你的密码' 0x1317bf7/fuckncov
</code>

<br>
<h3>
  高级操作
</h3>


<table>
  <tr>
    <td><h4>环境变量<h4></td>
    <td><h4>描述<h4></td>
  </tr>
  <tr>
    <td>USERNAME</td>
    <td>微人大账号</td>
  </tr>
  <tr>
    <td>PASSWORD</td>
    <td>微人大密码</td>
  </tr>
  <tr>
    <td>ADDRESS</td>
    <td>定位地址,不填默认上次提交的地址,在疫情防控通网页中输入vm.oldInfo.geo_api_info获取位置</td>
  </tr>
  <tr>
    <td>DAY_OF_WEEK</td>
    <td>每周打卡日期,默认0-6,参考crontab</td>
  </tr>
  <tr>
    <td>WEB_LOGIN</td>
    <td>若服务器需要在go.ruc.edu.cn连接校园网,填True,默认False</td>
  </tr>
  <tr>
    <td>TIME</td>
    <td>打卡时间,默认14:10</td>
  </tr>
  <tr>
    <td>USERAGENT</td>
    <td>模拟浏览器UA</td>
  </tr>
</table>
