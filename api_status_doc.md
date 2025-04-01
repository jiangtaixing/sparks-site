# 主机状态查询 API 文档

## GET /api/status/:hostname

该接口用于查询指定主机的当前状态，根据主机最后一次报告时间判断其状态。

### 请求方法

`GET`

### 请求URL

```
http://localhost:3000/api/status/:hostname
```

### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| hostname | String | 是 | 主机名称，用于查询指定主机的状态 |

### 请求示例

```
GET http://localhost:3000/api/status/server001
```

### 响应参数

响应体为JSON格式，包含以下字段：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| success | Boolean | 请求是否成功 |
| hostname | String | 主机名称 |
| status | String | 主机状态，可能的值："success"（正常）或"failure"（异常） |
| lastReportTime | String | 主机最后一次报告时间（ISO格式） |
| currentTime | String | 服务器当前时间（ISO格式） |
| timeDifference | String | 最后报告时间与当前时间的差值（分钟） |

### 响应示例

#### 成功响应（主机状态正常）

```json
{
  "success": true,
  "hostname": "server001",
  "status": "success",
  "lastReportTime": "2023-06-01T12:00:00.000Z",
  "currentTime": "2023-06-01T12:00:30.000Z",
  "timeDifference": "0 分钟"
}
```

#### 成功响应（主机状态异常）

```json
{
  "success": true,
  "hostname": "server001",
  "status": "failure",
  "lastReportTime": "2023-06-01T11:30:00.000Z",
  "currentTime": "2023-06-01T12:00:00.000Z",
  "timeDifference": "30 分钟"
}
```

#### 失败响应（未找到主机记录）

```json
{
  "success": false,
  "message": "未找到该主机的记录",
  "hostname": "unknown_server"
}
```

### 状态码

| 状态码 | 描述 |
| --- | --- |
| 200 | 请求成功 |
| 404 | 未找到指定主机的记录 |

### 状态判断规则

- 当主机最后一次报告时间距离当前时间小于1分钟时，状态为"success"（正常）
- 当主机最后一次报告时间距离当前时间大于或等于1分钟时，状态为"failure"（异常）

### 注意事项

- 主机需要先通过 POST /api/report 接口报告状态，才能通过此接口查询
- 建议配合监控系统使用，定期检查主机状态