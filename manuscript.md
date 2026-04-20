# Presentation Manuscript — MoE & Long Context

> 演讲稿，与 slides.md 同步维护。中文口语化表述，术语保留英文。

---

## Slide 1 — Title

> 大家好，欢迎来到今天的分享。我们今天的主题是 **Mixture of Experts 与 Long Context**，也就是混合专家模型和长上下文技术。这两个方向是当前大语言模型研究中非常活跃的领域，我们会从基础概念讲起，让大家对它们有一个清晰的认识。

---

## Slide 2 — 目录

> 我们先来看一下今天的内容安排。首先是背景介绍，然后分别讲 MoE 和 Long Context 的基础知识，接着看它们如何结合，最后有一个动手体验的 Demo 环节和总结。

---

## Slide 3 — 背景介绍：为什么关注 MoE & Long Context

> 我们先来看看为什么要关注这两个方向。
>
> 首先，大语言模型的参数量在持续增长——从 GPT-3 的 1750 亿到 GPT-4 估计的 1.8 万亿参数，训练和推理的成本急剧上升。
>
> 其次，用户对长文本理解的需求越来越多：比如长文档摘要、整个代码库的分析、多轮对话等等。
>
> MoE 提供了一种高效扩展模型容量的方式——关键思想是：不是所有参数都需要同时激活。
>
> 而 Long Context 与 MoE 的结合，正是当前 LLM 研究的前沿热点。

---

## Slide 4 — 背景介绍：核心问题

> 那么核心问题是什么呢？简单来说就是：**如何在有限的计算资源下，让模型既"大"又"长"？**
>
> "大"意味着模型容量足够、能力足够强，这就是 MoE 要解决的问题。
>
> "长"意味着能处理足够长的上下文，这是 Long Context 技术的目标。
>
> 而两者的交汇点在于：利用 MoE 的稀疏激活特性，来降低处理长上下文时的计算开销。

---

## Slide 5 — 背景介绍：路线图

> 这张表展示了我们今天的路线图。我们会依次覆盖 MoE 基础、Long Context 基础、两者的结合、一个动手 Demo，最后是总结与展望。大家可以随时提问。

---

## Slide 6 — MoE 是什么

> 接下来我们进入 MoE 基础部分。
>
> 传统的 Dense Model，也就是稠密模型，每个 token 都要经过模型的所有参数，计算量和参数量是成正比的。
>
> MoE 的核心思想是：把 Transformer 中的 FFN 层替换成 N 个并行的 Expert，每个 token 只激活其中 Top-k 个。这样总参数量可以很大，但每次推理实际用到的参数量很小。
>
> 举个例子，Mixtral 8×7B 总参数大约 470 亿，但每个 token 只激活大约 130 亿参数，计算量大幅降低。

---

## Slide 7 — MoE Layer 结构

> 我们来看 MoE Layer 的具体结构。
>
> 一个 token 进来之后，首先经过 Router，也叫门控网络。Router 会为这个 token 计算它对每个 Expert 的偏好分数，通常用 Softmax 得到概率分布。
>
> 然后选择概率最高的 Top-k 个 Expert 进行计算，其余 Expert 不参与。最终输出是被选中 Expert 输出的加权和，权重就是 Router 给出的概率值。
>
> 这个设计的精妙之处在于：不同的 token 可以被路由到不同的 Expert，模型可以学会让不同的 Expert 专注于不同类型的知识或任务。

---

## Slide 8 — 训练挑战与负载均衡

> MoE 的训练并不简单，最大的挑战是 Expert Collapse，也就是专家坍塌。
>
> 如果不加约束，Router 会倾向于总是把 token 发给少数几个表现好的 Expert，导致其余 Expert 得不到训练，最终退化成一个小模型。
>
> 解决方案是引入 Auxiliary Loss，也就是辅助损失。这个公式的直觉是：如果某个 Expert 实际接收的 token 比例 f_i 和 Router 分配给它的平均概率 P_i 都很高，那惩罚就大。这样就鼓励 token 均匀分配到各个 Expert。
>
> 另外还有 Capacity Factor 的概念，限制每个 Expert 最多处理多少 token，防止某个 Expert 过载。
>
> 值得一提的是，MoE 天然适合并行——不同的 Expert 可以放在不同的 GPU 上，这就是 Expert Parallelism。

---

## Slide 9 — 代表性工作一览

> 我们来看几个代表性的 MoE 模型。
>
> Switch Transformer 是 2021 年 Google 的工作，用了 128 个 Expert，总参数达到 1.6 万亿，但每次只激活一个 Expert。
>
> GShard 同样来自 Google，把 Expert 数量推到了 2048 个。
>
> Mixtral 8×7B 是 2023 年 Mistral AI 的开源模型，8 个 Expert 中每次激活 2 个，总参数 470 亿但激活参数只有 130 亿，上下文支持 32K。
>
> DBRX 和 DeepSeek-V3 则进一步扩大了规模。特别是 DeepSeek-V3，256 个 Expert 中激活 8 个，总参数 6710 亿，上下文窗口达到 128K。
>
> 可以看到一个明显的趋势：Expert 数量在增多，激活比例在降低，上下文窗口在持续扩大。MoE 已经从研究走向了生产级部署。

---

## Slides 10-21

> *(待补充)*
