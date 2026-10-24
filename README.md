# prometheus-grafana-monitoring
基于Python + Prometheus + Grafana + Docker‑Compose实现的Linux轻量服务器监控告警系统
> 云原生运维方向实践项目，使用Docker Compose一键部署

## ✨ 项目简介
使用Python开发自定义Exporter采集资源指标，基于Prometheus时序数据库采集指标，配置阈值告警规则，搭配Grafana实现可视化监控。理解Prometheus Pull采集模型、告警Pending/Firing机制。

## 🧱 架构
Python自定义采集脚本（Exporter） → Prometheus（拉取指标+告警规则） → Grafana（可视化面板）
- Python：psutil采集资源指标，暴露符合Prometheus规范的metrics接口
- Prometheus：Pull模式定时抓取指标，配置告警规则
- Grafana：时序图表可视化展示CPU、内存使用率
- 编排：Docker Compose 统一管理所有服务

## 📦 项目目录
prometheus-grafana-monitoring/
├── collect/                 # Python 采集脚本、Dockerfile
├── imgs/                    # 项目截图
├── alert-rules.yml          # Prometheus 告警规则
├── prometheus.yml           # Prometheus 主配置、抓取 job
├── docker-compose.yml       # 服务编排文件
├── .gitignore
└── README.md
