# Web应用开发架构图

## Mermaid流程图代码

```mermaid
graph TB
    subgraph Client["客户端层"]
        C[客户端浏览器<br/>携带session和cookie]
    end
    
    subgraph LB["负载均衡层"]
        LoadBalancer[负载均衡器]
    end
    
    subgraph AppLayer["应用服务层"]
        subgraph App1["应用服务器1"]
            M1[学员模块]
            M2[视频模块]
            M3[直播模块]
        end
        
        subgraph App2["应用服务器2"]
            M4[学员模块]
            M5[视频模块]
            M6[直播模块]
        end
    end
    
    subgraph CacheLayer["缓存层"]
        MC[Memcache<br/>缓存存储解耦<br/>库读取压力]
    end
    
    subgraph DBLayer["数据库层"]
        MasterDB[(主数据库<br/>主库<br/>写操作)]
        SlaveDB[(从数据库<br/>从库<br/>读操作)]
    end
    
    C -->|HTTP请求| LoadBalancer
    LoadBalancer -->|分发请求| App1
    LoadBalancer -->|分发请求| App2
    
    App1 -->|读| MC
    App2 -->|读| MC
    
    App1 -->|写| MasterDB
    App2 -->|写| MasterDB
    
    MC -->|缓存未命中/读| SlaveDB
    App1 -->|直接读| SlaveDB
    App2 -->|直接读| SlaveDB
    
    MasterDB -->|数据同步| SlaveDB
    
    style Client fill:#e1f5ff
    style LB fill:#fff4e1
    style AppLayer fill:#f0f0f0
    style CacheLayer fill:#e8f5e9
    style DBLayer fill:#fce4ec
    style MasterDB fill:#ffcdd2
    style SlaveDB fill:#ffcdd2
    style MC fill:#c8e6c9
```

## 架构说明

### 1. 客户端层
- 用户通过浏览器访问，携带session和cookie信息
- 发起HTTP/HTTPS请求到负载均衡器

### 2. 负载均衡层
- 接收客户端请求
- 根据负载均衡策略（轮询、最少连接等）将请求分发到不同的应用服务器
- 实现高可用和流量分发

### 3. 应用服务层
- 多个应用服务器实例（水平扩展）
- 每个服务器包含相同的业务模块：
  - 学员模块：用户管理、认证等
  - 视频模块：视频播放、点播等
  - 直播模块：实时直播服务
- 实现无状态设计，便于扩展

### 4. 缓存层（Memcache）
- 缓存热点数据，减少数据库访问压力
- 实现存储解耦，提高读取性能
- 降低数据库读取压力，提升系统响应速度

### 5. 数据库层
- **主数据库（Master）**：处理所有写操作
- **从数据库（Slave）**：处理读操作
- 主从同步：主库数据自动同步到从库
- 读写分离：提高数据库性能和可用性

## 数据流向

### 读操作流程
1. 客户端请求 → 负载均衡器 → 应用服务器
2. 应用服务器先查询Memcache缓存
3. 缓存命中：直接返回数据
4. 缓存未命中：从从库读取数据，并更新缓存

### 写操作流程
1. 客户端请求 → 负载均衡器 → 应用服务器
2. 应用服务器写入主数据库
3. 主数据库同步数据到从数据库
4. 根据策略更新或失效缓存

## 关键技术点

- **缓存存储解耦**：通过Memcache实现应用与数据库的解耦
- **库读取压力**：通过缓存和读写分离降低数据库压力
- **水平扩展**：应用服务器可以根据负载动态扩容
- **高可用性**：多实例部署，单点故障不影响整体服务
- **读写分离**：优化数据库性能，主库负责写，从库负责读

