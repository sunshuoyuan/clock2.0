import network
import ntptime
import time

def setup_wifi(ssid, password):
    """设置并连接WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"连接到WiFi: {ssid}")
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

def get_ntp_time(max_retries=3):
    """通过NTP获取时间，带重试机制"""
    # 使用可靠的NTP服务器IP地址（避免DNS解析问题）
    ntp_servers = [
        "132.163.97.4",    # NIST, USA
        "129.6.15.30",      # NIST, USA
        "216.239.35.0",     # Google, USA
        "162.159.200.123",  # Cloudflare, Global
        "203.107.6.88"      # Alibaba, China
    ]
    
    # 保存原始NTP主机设置
    original_host = ntptime.host if hasattr(ntptime, 'host') else None
    
    for attempt in range(max_retries):
        try:
            # 尝试不同的NTP服务器
            server = ntp_servers[attempt % len(ntp_servers)]
            print(f"尝试从 {server} 获取时间 (尝试 {attempt+1}/{max_retries})")
            
            # 设置NTP服务器
            ntptime.host = server
            
            # 获取时间
            ntptime.settime()
            
            # 获取并格式化当前时间
            t = time.localtime()
            formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                t[0], t[1], t[2], t[3], t[4], t[5])
            
            print("NTP时间获取成功!")
            print("当前时间:", formatted_time)
            return True
            
        except OSError as e:
            print(f"错误: {e} (代码: {e.args[0]})")
            # 常见的错误代码处理建议
            if e.args[0] == -202:
                print("错误 -202: 网络问题，请检查连接")
            elif e.args[0] == 110:  # ETIMEDOUT
                print("错误 110: 连接超时，尝试下一个服务器")
            time.sleep(2)  # 重试前等待
            
        except Exception as e:
            print("未知错误:", e)
            time.sleep(2)
    
    # 恢复原始NTP主机设置
    if original_host:
        ntptime.host = original_host
    
    print("NTP时间获取失败，所有尝试均未成功")
    return False

# 主程序
def main(ssid, pw):
    # WiFi配置
    WIFI_SSID = ssid
    WIFI_PASSWORD = pw
    
    # 先连接WiFi
    if setup_wifi(WIFI_SSID, WIFI_PASSWORD):
        # 获取NTP时间
        get_ntp_time()
        
        # 显示本地时间（无论NTP是否成功）
        t = time.localtime()
        local_time = "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
        print("设备本地时间:", local_time)
    else:
        print("无法连接到WiFi，跳过时间同步")
        
if __name__ == '__main__':
    main("djs2.4", "11111111")