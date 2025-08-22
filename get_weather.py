import network
import urequests
import json
import time

# WiFi配置
WIFI_SSID = "CU_v3Je"
WIFI_PASSWORD = "n35967hs"

# 心知天气配置
API_KEY = "SNvT9_a96JhbZrA4F"  # 心知天气API密钥
UNIT = "c"  # 温度单位
language = "zh-Hans"
today = []
tomorrow = []
after_tomorrow = []
# IP定位服务配置（使用ip-api.com，免费且无需密钥）
IP_LOCATION_URL = "http://ip-api.com/json/?fields=status,message,city,countryCode,lat,lon"
day_num = 0


def connect_wifi(ssid=WIFI_SSID, password=WIFI_PASSWORD):
    """设置并连接WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("连接到WiFi: {0}".format(ssid))
        wlan.connect(ssid, password)

        # 等待连接
        for _ in range(15):
            if wlan.isconnected():
                print("WiFi连接成功!")
                print("IP地址:", wlan.ifconfig()[0])
                return True
            time.sleep(1)
        print("WiFi连接失败!")
        return False
    return True


def get_device_location():
    """通过IP地址获取设备位置信息"""
    try:
        print("获取设备位置...")
        response = urequests.get(IP_LOCATION_URL)
        data = json.loads(response.text)
        response.close()

        if data.get("status") == "success":
            return {
                "city": data.get("city"),
                "country_code": data.get("countryCode"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon")
            }
        else:
            print("定位失败: {0}".format(data.get('message')))
            return None
    except Exception as e:
        print("定位错误: {0}".format(e))
        return None


def get_3day_forecast(location):
    """获取未来三天天气预报"""
    # 使用城市名称或经纬度定位
    location_param = location["city"] if location["city"] else "{0}:{1}".format(location['latitude'],
                                                                                location['longitude'])

    url = "https://api.seniverse.com/v3/weather/daily.json?key={0}&location={1}&language={2}&unit={3}&start=0&days=3".format(
        API_KEY, location_param, language, UNIT)

    try:
        print("获取天气预报...")
        response = urequests.get(url)

        if response.status_code != 200:
            print("天气API错误: {0}".format(response.text))
            response.close()
            return None

        data = json.loads(response.text)
        response.close()
        return data
    except Exception as e:
        print("天气请求错误: {0}".format(e))
        return None


def parse_specific_day(data, location, day_index):
    """解析并显示指定天的天气预报
    这边的location参数应该是为了获取地区来获取相应的天气的，但实际上他好像根本就没使用到，我也不知道有什么用，也不知道删了行不行，反正就先这样吧"""
    if not data or "results" not in data:
        print("无有效天气数据")
        if data:
            print("完整响应:", data)
        return []

    try:
        results = data["results"]
        if not results:
            print("无天气预报结果")
            return []

        location_info = results[0]["location"]
        city = location_info["name"]
        country = location_info["country"]

        daily_list = results[0]["daily"]

        # 检查day_index是否有效
        if day_index < 0 or day_index >= len(daily_list):
            print("无效的日期索引: {0}。可用范围: 0-{1}".format(day_index, len(daily_list) - 1))
            return []

        daily = daily_list[day_index]
        date_str = daily["date"][5:10]  # 提取MM-DD
        weather_day = daily["text_day"]
        weather_night = daily["text_night"]
        low_temp = daily["low"]
        high_temp = daily["high"]

        # 创建友好的日期名称
        day_names = ["今天", "明天", "后天"]
        day_name = day_names[day_index] if day_index < len(day_names) else date_str

        print("\n=== {0}, {1} 指定日天气预报 ===".format(city, country))
        print("日期: {0} ({1})".format(date_str, day_name))
        print("白天: {0}".format(weather_day))
        print("夜间: {0}".format(weather_night))
        print("温度: {0}~{1}°{2}".format(low_temp, high_temp, UNIT.upper()))
        return [date_str, day_index, daily["code_day"], daily["code_night"], low_temp, high_temp, UNIT.upper()]

    except KeyError as e:
        print("数据解析错误, 缺少字段: {0}".format(e))


def get_weather():
    # 主程序
    if connect_wifi():
        location = get_device_location()

        if location:
            print("检测到位置: {0}, {1}".format(location['city'], location['country_code']))
            forecast_data = get_3day_forecast(location)

            if forecast_data:
                # 在这里指定要输出的天数索引
                # 0 = 今天, 1 = 明天, 2 = 后天
                day_to_show = 0  # 这里设置为显示明天的天气

                # 注意：现在调用的是 parse_specific_day，并传递了三个参数
                global today
                today = parse_specific_day(forecast_data, location, day_to_show)
                day_to_show = 1
                global tomorrow
                tomorrow = parse_specific_day(forecast_data, location, day_to_show)
                day_to_show = 2
                global after_tomorrow
                after_tomorrow = parse_specific_day(forecast_data, location, day_to_show)
            else:
                print("获取天气预报失败")
        else:
            print("无法确定位置，使用默认城市")
            location = {"city": "北京", "country_code": "CN", "latitude": 39.9042, "longitude": 116.4074}
            forecast_data = get_3day_forecast(location)

            if forecast_data:
                day_to_show = day  # 显示明天的天气
                parse_specific_day(forecast_data, location, day_to_show)


get_weather()
print(today)
print(tomorrow)
print(after_tomorrow)
