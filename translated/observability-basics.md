# 追踪与跨度：你应该了解的可观测性基础知识（Traces & Spans: Observability Basics You Should Know）

> 作者：Anjali Udasi（Last9）
> 原文日期：2025 年 4 月 23 日

了解追踪（traces）与跨度（spans）如何帮助你“看见”分布式系统内部，从而更快地排障、构建更可靠的软件。

在现代软件架构中，应用不只是在变大——它们正变得越来越“分布式”。微服务、无服务器函数和容器运行在多个环境中，想要理解系统内部正在发生什么，感觉就像是在一场风暴中追踪某颗特定的雨滴。

这正是追踪与跨度登场的地方。这些可观测性工具并不是空洞的流行词——它们是你理解复杂分布式系统的秘密武器。下面我们来拆解：什么是追踪、什么是跨度，它们为什么重要，以及如何用它们更快排障、构建更可靠的系统。

## 理解追踪与跨度：核心概念

追踪（trace）记录了一次请求在分布式系统中流转的完整旅程。可以把追踪想象成一次请求从头到尾的完整故事——从用户点击按钮，一直到他们看到结果。

跨度（span）是构成追踪的积木。每个跨度代表这段旅程中的一个工作单元——比如一次数据库查询、一次 API 调用，或一次函数执行。跨度之间彼此嵌套，用以展示操作之间的父子关系。

用简单的话来概括它们的关系：

- 一条追踪包含多个跨度
- 每个跨度代表一次操作
- 跨度带有计时数据与元数据
- 跨度可以嵌套，以展示操作之间的关联

```
Trace
├── Span (API Gateway)
│   ├── Span (Auth Service)
│   └── Span (User Service)
│       └── Span (Database Query)
└── Span (Response Formatting)
```

> 💡 如果你好奇追踪、跨度如何与指标（metrics）、日志（logs）、事件（events）协同配合，可以参阅另一篇文章，它把四者都讲清楚了。

## 追踪与跨度给 DevOps 从业者带来的好处

设想你正在运行一个由几十个微服务构成的复杂系统。突然，用户反馈结账流程变慢了。没有追踪的话，你得逐个服务去排查，白白浪费宝贵时间。

有了追踪与跨度，你可以：

- **瞬间定位瓶颈**：准确看到是哪个服务或函数耗时过长
- **跨服务边界调试**：跟随请求在各个服务之间跳转
- **理解依赖关系**：直观呈现你的服务之间如何连接、如何相互依赖
- **提升性能**：精准地识别并修复慢操作
- **缩短平均恢复时间（MTTR）**：问题出现时更快找到根因

## 追踪与跨度的技术实现

下面进入正题，看看分布式系统中追踪具体是如何工作的。

### 追踪上下文与传播

要让追踪跨服务边界工作，每个服务都需要知道它正在处理的是同一次请求的一部分。这是通过**上下文传播（context propagation）**实现的——在服务之间传递追踪 ID（trace ID）与跨度 ID（span ID）。

当请求首次进入你的系统时，会被分配一个唯一的追踪 ID。随着请求在服务之间流转，这个 ID 也随之传递（通常以 HTTP 头部形式携带）。每个服务接着创建自己的跨度，但把它们链接到同一条追踪上。

### 跨度属性与事件

跨度不只是时间戳——它们承载着丰富的数据：

- **名称（Name）**：这个跨度代表什么操作
- **计时（Timing）**：开始与结束时间
- **状态（Status）**：成功、出错等
- **属性（Attributes）**：自定义键值对（比如 user_id 或 cart_size）
- **事件（Events）**：跨度内值得注意的节点
- **链接（Links）**：与其他跨度的连接

### 采样策略

追踪所有请求会产生海量数据。因此大多数系统会使用**采样（sampling）**——只采集一定比例的追踪。常见的采样策略包括：

- **头部采样（Head-based sampling）**：在请求开始时决定是否采样
- **尾部采样（Tail-based sampling）**：在请求完成后再决定（更利于捕获错误）
- **优先级采样（Priority sampling）**：始终追踪重要操作，对常规操作才采样

> 💡 如果你想了解可观测性（observability）、遥测（telemetry）与监控（monitoring）三者之间的区别，可以参阅这篇文章：Observability vs Telemetry vs Monitoring。

## 追踪实施指南：工具与框架

准备给你的系统接入追踪了吗？你需要这些：

### OpenTelemetry：业界标准

OpenTelemetry 已成为实现追踪与跨度的首选框架。它提供：

- 覆盖所有主流编程语言的库
- 厂商中立的 API 与 SDK
- 针对流行框架的自动埋点（automatic instrumentation）
- 一致的采集与导出数据方式

### 追踪工具箱

以下工具可以帮助你采集、存储和可视化追踪：

| 工具 | 类型 | 最适合 |
|---|---|---|
| Last9 | 一体化可观测性 | 成本效益高、高基数、定价可预测的可观测性 |
| Jaeger | 开源追踪 | 自托管的追踪可视化 |
| Zipkin | 开源追踪 | 简单的分布式追踪 |
| Grafana Tempo | 追踪后端 | 与 Grafana 仪表盘集成 |
| OpenTelemetry Collector | 数据采集管道 | 遥测数据的处理与路由 |

如果你在寻找一款符合预算的可观测性方案，Last9 值得一看。它按摄入事件计费，价格可预测；而且我们的平台能在规模化场景下处理高基数数据，并与 OpenTelemetry、Prometheus 集成，把指标、日志、追踪汇聚到一处。

### 在代码中实现追踪

下面是一个在 Node.js 应用中使用 OpenTelemetry 创建跨度的简化示例：

```javascript
// 初始化 OpenTelemetry SDK（应用内只需执行一次）
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const provider = new NodeTracerProvider();
const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// 获取一个 tracer
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

// 在代码中创建跨度
async function processOrder(orderId) {
  const span = tracer.startSpan('process-order');

  // 给跨度添加属性
  span.setAttribute('order.id', orderId);
  span.setAttribute('customer.type', 'premium');

  try {
    // 执行具体工作……

    // 创建子跨度
    const dbSpan = tracer.startSpan('database-query', {
      parent: span,
    });

    try {
      // 执行数据库查询……
      dbSpan.end();
    } catch (error) {
      dbSpan.setStatus({ code: SpanStatusCode.ERROR });
      dbSpan.recordException(error);
      dbSpan.end();
      throw error;
    }

    span.end();
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR });
    span.recordException(error);
    span.end();
    throw error;
  }
}
```

> 💡 想知道 OpenTelemetry 与传统 APM（应用性能监控）工具相比如何？这篇文章拆解了关键差异：OpenTelemetry vs Traditional APM Tools。

## 进阶追踪技巧

一旦你把基础追踪跑起来，以下进阶技巧能让你的可观测性再上一个台阶。

### 分布式上下文管理

在复杂系统中，你需要管理追踪 ID 之外的上下文。W3C Trace Context 规范为以下内容提供了标准：

- **traceparent**：包含追踪 ID 与父跨度 ID
- **tracestate**：允许厂商添加自定义上下文数据

使用这些头部，可以确保你的追踪在不同服务与不同厂商之间都能正常工作。

### 追踪、指标与日志之间的关联

可观测性的真正威力，来自把不同的信号连接起来：

- **范例追踪（Exemplar traces）**：把指标关联到产生它们的追踪上
- **日志中的追踪 ID**：把追踪 ID 写入日志消息，便于交叉引用
- **自定义属性**：在所有遥测类型中使用一致的属性

### 错误处理与异常追踪

当异常发生时，跨度能提供关键的上下文：

- 为跨度标记错误状态
- 连同堆栈记录异常
- 为跨度添加展示错误演进过程的事件
- 创建跨服务边界携带错误上下文的行李项（baggage items）

> 💡 想更深入地了解如何前瞻问题、提升系统可靠性，可以参阅这篇关于主动监控的文章：Proactive Monitoring。

## 现实世界中的追踪模式与反模式

### 有效的追踪模式

- **有意义的跨度命名**：使用一致的命名约定，比如 `service_name/operation`
- **合适的粒度**：只为重要操作创建跨度，而不是每次函数调用都建
- **正确的上下文传播**：确保追踪上下文流经所有通信通道
- **有用的属性**：添加有助于排障的属性，比如用户 ID 或功能开关（feature flags）
- **性能意识**：警惕过度创建跨度带来的开销

### 应避免的追踪反模式

- **过度埋点（Over-instrumentation）**：创建过多跨度会导致性能问题
- **上下文缺失**：未能传播上下文会切断跨服务边界的追踪
- **命名不一致**：使用不同的命名标准会让追踪更难解读
- **数据过多**：把过大的载荷放进跨度会压垮你的追踪后端
- **忽略第三方服务**：外部调用缺少跨度会制造盲点

> 💡 探索可观测性在 LLM 的性能与可靠性方面扮演的关键角色：LLM Observability。

## 追踪与跨度的商业价值：超越技术收益

追踪不只是用于排障——它也能带来商业洞察：

- 端到端追踪关键用户旅程
- 度量关键业务操作的性能
- 基于追踪数据设定 SLO（服务水平目标，Service Level Objectives）
- 用真实用户的视角量化性能问题的代价
- 通过为跨度添加相关属性来构建业务上下文

当你能展示技术改进如何影响用户体验与业务指标时，你就架起了 DevOps 与业务相关方之间的桥梁。

## 结语

追踪与跨度让你拥有看穿分布式系统的“X 光视野”。它们揭示服务之间隐藏的连接、精准定位性能瓶颈，并大幅加速调试。

随着系统日益复杂，这种可观测性已不是奢侈品——而是必需品。

> 💡 如果你想继续深入交流分布式追踪与可观测性，欢迎加入我们的 Discord 社区，与分享经验与最佳实践的 DevOps 从业者一起讨论。

## 常见问题（FAQ）

### 追踪与日志有什么区别？

日志采集的是离散事件，而追踪展示的是跨服务的操作之间的关系。日志告诉你“发生了什么”，追踪则告诉你“它是如何发生的”。

### 接入追踪会让我的应用变慢吗？

现代追踪库带来的开销极小——配置得当的话，性能影响通常低于 3%。配合采样，还能进一步降低影响。

### 接入追踪需要改动我所有的代码吗？

不一定。许多框架提供自动埋点，只需极少的代码改动就能接入追踪。OpenTelemetry 为大多数语言的流行框架提供了自动埋点。

### 分布式追踪会产生多少数据？

这因流量、采样率和跨度细节而异，差别很大。对于繁忙的系统，每天可能产生从 GB 到 TB 级别的数据。因此，选择合适的可观测性平台对成本控制至关重要。

### 追踪能帮助安全与合规吗？

能！追踪会为请求在系统中的流转创建一条审计轨迹。配合合适的属性，你可以追踪哪些用户或服务在何时访问了什么数据。

### 追踪和跨度如何与其他可观测性信号配合？

追踪与指标、日志互为补充。指标从高层次展示系统健康度，日志提供详细事件，追踪则把各个点连起来，展示请求跨服务的流转路径。

---

来源：Last9《Traces & Spans: Observability Basics You Should Know》，作者 Anjali Udasi，2025-04-23
