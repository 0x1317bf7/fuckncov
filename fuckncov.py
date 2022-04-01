# encoding=utf-8
import asyncio
import random
import time

from pyppeteer import launch

import values

values.init()

script_web_login = '''
function loginAccount() {
    var domain = $('#domain').val();
    var portal = new Portal(CONFIG);
    if (domain && domain.substring(0, 1) !== '@') domain = '@' + domain.split('@')[1];
        portal.userInfo.username = "$USERNAME";
        portal.userInfo.password = "$PASSWORD";
        portal.userInfo.domain   = domain || '';
        portal.login({
            type: 'account',
            success: function (message) {
                portal.setCookie('username', portal.userInfo.username);
                if ($('#remember').prop('checked')) portal.remember(true);
                if (!$('#remember').prop('checked')) portal.remember(false);
                if (!CREATER.highBurstPlan)  portal.toSuccess();
                if (CREATER.highBurstPlan) portal.highBurstPlan(portal.getUrlParams('wlanuserfirsturl') || 'https://www.ruc.edu.cn');
        }
    });
}
loginAccount();
'''.replace("$USERNAME", values.username).replace("$PASSWORD", values.password)

script_login = '''
$.ajax({ 
    type: 'POST',
    cache: false, 
    url: '/uc/wap/login/check',
    data: { username: '$USERNAME', password: '$PASSWORD', }, 
    dataType: 'json',
    success: function (resp) {
        window.location.href = 'https:\/\/m.ruc.edu.cn\/ncov\/wap\/default';
    },
    error: function () { } 
    }
);
'''.replace("$USERNAME", values.username).replace("$PASSWORD", values.password)

script_submit = '''
new Vue({
    el: '#app',
    methods: {
        xsave: function(info) {
            if (vm.hasFlag == 1) {
                return;
            }
            $.ajax({
                url: '/ncov/wap/default/save',
                type: 'POST',
                dataType: 'JSON',
                data: info,
                success: function (resp) { },
                error: function () { }
            });
        },
        createAddress: function(address) {
            var q = address.position.Q;
            var r = address.position.R;
            q += this.randomDecimal(-0.0005, 0.0005);
            r += this.randomDecimal(-0.001, 0.001);
            var Q = this.transformDecimal(q, 12);
            var R = this.transformDecimal(r, 12);
            var lng = this.transformDecimal(r, 6);
            var lat = this.transformDecimal(q, 6);
            address.position.Q = Q;
            address.position.R = R;
            address.position.lng = lng;
            address.position.lat = lat;
            return address;
        },
        auto_run: function() {
            var address = window.decodeURIComponent('$address$');
            var hasAddress = true;
            if (address == null || address.length < 10) {
                address = vm.oldInfo.geo_api_info;
                hasAddress = false;
            }
            var json = JSON.parse(address);
            if (hasAddress) {
                json = this.createAddress(json);
            }  
            var info = vm.info;
            info.geo_api_info = JSON.stringify(json);
            info.address = json.formattedAddress;
            info.province = json.addressComponent.province;
            info.showprovince = json.addressComponent.province;
            if ($.trim(json.addressComponent.city) === '' && ['北京市', '上海市', '重庆市', '天津市'].indexOf(info.province) > -1) {
                info.city = json.addressComponent.province;
            } else {
                info.city = json.addressComponent.city;
            }
            info.area = json.addressComponent.province + ' ' + json.addressComponent.city + ' ' + json.addressComponent.district;
            info.sfzx = (info.address == "北京市海淀区海淀街道中国人民大学") ? "1" : "0";
            info.tw = this.randomInteger(1, 2);
            info.mjry = "0";
            info.zgfxdq = "0";
            info.jcjgqr = "0";
            info.sfcxtz = "0";
            info.sfjcbh = "0";
            info.csmjry = "0";
            info.sfcyglq = "0";
            info.szsqsfybl = "0";
            info.sfcxzysx = "0";
            this.xsave(info);
        },
        randomInteger: function(minNum, maxNum) {
            switch (arguments.length) {
                case 1:
                    return parseInt(Math.random() * minNum + 1, 10);
                case 2:
                    return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
                default:
                    return 0;
            }
        },
        randomDecimal: function(min, max) {
            var range = max - min;
            var rand = Math.random();
            var num = min + rand * range;
            return num;
        },
        transformDecimal: function(number, i) {
            var decimalNum = null;
            var num = Number(number);
            if(!isNaN(num)) {
                var arr = num.toString().split(".");
                if(arr.length > 1 && arr[1].length > i) {
                    var decimal = arr[1].slice(i, i+1);
                    if(decimal === '5') {
                        num += Math.pow(0.1, i+1);
                    }
                    decimalNum = num.toFixed(i);
                } else {
                    decimalNum = num;
                }
                decimalNum = Number(decimalNum);
            }
            return decimalNum;
        }
    }
}).auto_run();
'''

if values.address is not None:
    script_submit = script_submit.replace("$ADDRESS$", values.address)

url_web_login = '''https://go.ruc.edu.cn'''
url = '''https://m.ruc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fm.ruc.edu.cn%2Fncov%2Fwap%2Fdefault'''

async def run():
    print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
    print("init browser")
    browser = await launch(
        {'args': ['--disable-infobars', '--blink-settings=imagesEnabled=false', '--no-first-run', '--disable-gpu',
                  '--no-sandbox'], 'headless': True},
        userDataDir="/User_Data/Default",
        executablePath="chromium-browser"
    )

    page = await browser.newPage()

    await page.setUserAgent(values.useragent)

    await page.setViewport({'width': 1536, 'height': 824})

    await page.evaluateOnNewDocument(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    # await page.evaluateOnNewDocument('''delete navigator.__proto__.webdriver''')

    if values.web_login:
        print("go to login " + url_web_login)
        await page.goto(url_web_login)

        print("exec script_web_login")
        await page.evaluate(script_web_login, force_expr=False)

    await page.waitFor(10000 + random.random() * 3000)

    print("go to " + url)
    await page.goto(url)

    await page.waitFor(10000 + random.random() * 3000)

    print("exec script_login")
    await page.evaluate(script_login, force_expr=False)

    await page.waitFor(10000 + random.random() * 10000)

    print("exec script_submit")
    await page.evaluate(script_submit, force_expr=True)

    await page.waitFor(10000 + random.random() * 10000)

    print("close browser")
    await browser.close()


def main():
    values.init()
    if not values.debug:
        time.sleep(random.random() * 60 * 60)
    asyncio.get_event_loop().run_until_complete(run())


if __name__ == "__main__":
    main()
