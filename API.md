# WiFi配网系统 API文档

## 接口概述

本文档描述了WiFi配网系统提供的两个主要接口：同步配网接口和异步配网接口。这两个接口都用于配置设备的WiFi连接和主机名。

## 1. 同步配网接口

### 接口信息

- **接口地址**：`/connect`
- **请求方法**：POST
- **Content-Type**：`application/x-www-form-urlencoded`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ssid | string | 是 | WiFi名称 |
| password | string | 是 | WiFi密码 |
| hostname | string | 否 | 设备主机名 |

### 响应格式

```json
{
    "success": true,
    "reboot": true
}
```

### 响应参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 操作是否成功 |
| reboot | boolean | 是否需要重启设备 |
| message | string | 错误信息（仅在失败时返回）|

### 示例

```bash
curl -X POST http://192.168.255.1/connect \
     -d "ssid=MyWiFi" \
     -d "password=MyPassword" \
     -d "hostname=MyDevice"
```

## 2. 异步配网接口

### 接口信息

- **接口地址**：`/api/connect`
- **请求方法**：POST
- **Content-Type**：`application/json`

### 请求参数

```json
{
    "ssid": "MyWiFi",
    "password": "MyPassword",
    "hostname": "MyDevice"
}
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ssid | string | 是 | WiFi名称 |
| password | string | 是 | WiFi密码 |
| hostname | string | 否 | 设备主机名 |

### 响应格式

```json
{
    "success": true,
    "message": "WiFi配置已接收，正在后台处理",
    "reboot": true
}
```

### 响应参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 操作是否成功 |
| message | string | 操作结果说明 |
| reboot | boolean | 是否需要重启设备 |

### 示例

```bash
curl -X POST http://192.168.255.1/api/connect \
     -H "Content-Type: application/json" \
     -d '{
           "ssid": "MyWiFi",
           "password": "MyPassword",
           "hostname": "MyDevice"
         }'
```

## 错误码说明

| 情况 | success | message |
|------|---------|----------|
| 成功 | true | WiFi配置已接收，正在后台处理 |
| 缺少SSID | false | 请提供WiFi名称(SSID) |
| 缺少密码 | false | 请提供WiFi密码 |
| 无效请求数据 | false | 无效的请求数据格式 |

## 使用注意事项

1. **接口选择建议**
   - 同步接口（`/connect`）：适用于需要立即知道配网结果的场景
   - 异步接口（`/api/connect`）：适用于不需要等待配网结果的场景，响应更快

2. **网络连接**
   - 调用接口前，确保设备处于AP模式，且客户端已连接到设备的WiFi热点
   - 默认AP模式下的设备IP地址为：192.168.255.1

3. **重启说明**
   - 配网成功后设备会自动重启
   - 重启过程中设备会断开当前的网络连接

4. **错误处理**
   - 如果配网失败，设备会自动清除已保存的WiFi配置
   - 设备会自动回退到AP模式

5. **主机名设置**
   - 主机名参数为可选项
   - 如果提供主机名，设备会在重启前修改系统主机名