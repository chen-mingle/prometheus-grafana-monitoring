import psutil
import time
from prometheus_client import Gauge, start_http_server

# 定义监控指标
cpu_gauge = Gauge("server_cpu_usage_percent", "服务器CPU使用率百分比")
mem_gauge = Gauge("server_mem_usage_percent", "服务器内存使用率百分比")
disk_gauge = Gauge("server_disk_usage_percent", "根磁盘/使用率百分比")
load1_gauge = Gauge("server_load1", "系统1分钟平均负载")
sshd_status = Gauge("server_sshd_running", "sshd服务状态：1正常运行，0异常")

# 告警阈值
CPU_THRESHOLD = 85
MEM_THRESHOLD = 85
DISK_THRESHOLD = 85
ALERT_LOG = "./alert.log"

def write_alert(message):
    """写入告警日志"""
    with open(ALERT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {message}\n")

def collect_loop():
    while True:
        # CPU采集
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_gauge.set(cpu_usage)
        if cpu_usage > CPU_THRESHOLD:
            write_alert(f"CPU告警，当前使用率：{cpu_usage}%")

        # 内存采集
        mem_info = psutil.virtual_memory()
        mem_percent = mem_info.percent
        mem_gauge.set(mem_percent)
        if mem_percent > MEM_THRESHOLD:
            write_alert(f"内存告警，当前使用率：{mem_percent}%")

        # 根磁盘采集
        disk_info = psutil.disk_usage("/")
        disk_percent = disk_info.percent
        disk_gauge.set(disk_percent)
        if disk_percent > DISK_THRESHOLD:
            write_alert(f"磁盘告警，根分区使用率：{disk_percent}%")

        # 1分钟系统负载
        load1, _, _ = psutil.getloadavg()
        load1_gauge.set(load1)

        # sshd服务状态检测
        sshd_running = 0
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and "sshd" in proc.info["name"]:
                sshd_running = 1
                break
        sshd_status.set(sshd_running)
        if sshd_running == 0:
            write_alert("告警：sshd服务没有运行！")

        time.sleep(10)

if __name__ == "__main__":
    # 暴露8000端口提供metrics
    start_http_server(8000)
    collect_loop()
