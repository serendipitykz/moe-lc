---
theme: mint
title: MoE & Long Context
drawings:
  persist: false
transition: slide-left
mdc: true
---

# MoE & Long Context

混合专家模型与长上下文

<div class="pt-12">
  <span class="px-2 py-1 rounded">
    ACM Class 2026 · 大语言模型课程
  </span>
</div>

---

# 目录

<Toc maxDepth="1" />

---

# 背景介绍

## 为什么我们需要关注 MoE 和 Long Context？

<v-clicks>

- 🚀 大语言模型参数量持续增长（GPT-3 175B → GPT-4 ~1.8T），**训练和推理成本急剧上升**
- 📏 用户对**长文本理解**的需求日益增长：长文档摘要、代码库分析、多轮对话……
- 💡 MoE 提供了一种**高效扩展模型容量**的方式——不是所有参数都需要同时激活
- 🔗 Long Context 与 MoE 的结合，是当前 LLM 研究的**前沿热点**

</v-clicks>

---

# 背景介绍

## 核心问题

<br>

> **如何在有限的计算资源下，让模型既"大"又"长"？**

<br>

<v-clicks>

- **"大"** → 模型容量足够大，能力足够强 → **MoE**
- **"长"** → 能处理足够长的上下文 → **Long Context**
- 两者的交汇：用 MoE 的稀疏激活特性，降低处理长上下文的计算开销

</v-clicks>

---

# 背景介绍

## 本次 Presentation 路线图

<br>

| 章节 | 内容 |
|------|------|
| **MoE 基础** | 稀疏混合专家架构、门控机制、路由策略 |
| **Long Context 基础** | 上下文窗口的挑战、位置编码、高效注意力 |
| **MoE × Long Context** | 两者如何结合、前沿工作 |
| **Demo** | 动手体验环节 |
| **总结与展望** | 关键 takeaways、开放问题 |

---

# MoE 基础

## 什么是 Mixture of Experts？

<v-clicks>

- 传统 Dense Model：每个 token 经过**所有**参数 → 计算量 ∝ 参数量
- MoE 的核心思想：将 FFN 层替换为 **N 个并行的 Expert**，每个 token 只激活其中 **Top-k 个**
- 结果：**总参数量很大，但每次推理的激活参数量很小**

</v-clicks>

<br>

<div v-click class="text-center text-sm opacity-70">

例：Mixtral 8×7B 总参数 ~47B，但每个 token 仅激活 ~13B 参数

</div>

---

# MoE 基础

## MoE Layer 结构

<br>

```
Input Token x
      │
      ▼
┌─────────────┐
│   Router    │  ← Gating Network: G(x) = Softmax(W_g · x)
│  (门控网络)  │
└─────┬───────┘
      │ Top-k 选择
      ▼
┌─────┬─────┬─────┬─────┐
│ E_1 │ E_2 │ ... │ E_N │  ← N 个 Expert (各自是一个 FFN)
└──┬──┴──┬──┴─────┴──┬──┘
   │     │           │
   └─────┴─────┬─────┘
         加权求和 Σ g_i · E_i(x)
               │
               ▼
         Output y
```

<v-clicks>

- **Router** 为每个 token 计算各 Expert 的权重
- 只有 **Top-k** 权重最大的 Expert 被激活并计算
- 输出是被选中 Expert 输出的**加权和**

</v-clicks>

---

# MoE 基础

## 训练挑战与负载均衡

<v-clicks>

- **Expert Collapse（专家坍塌）**：Router 倾向于总是选择少数几个 Expert → 其余 Expert 得不到训练
- **Auxiliary Loss（辅助损失）**：在训练 loss 中加入负载均衡项，鼓励 token 均匀分配

</v-clicks>

<div v-click>

$\mathcal{L}_{\text{aux}} = \alpha \cdot N \cdot \sum_{i=1}^{N} f_i \cdot P_i$

<div class="text-sm opacity-70 mt-2">

其中 $f_i$ = Expert $i$ 实际接收的 token 比例，$P_i$ = Router 分配给 Expert $i$ 的平均概率

</div>

</div>

<v-clicks>

- **Capacity Factor**：限制每个 Expert 最多处理的 token 数，防止过载
- **Expert Parallelism**：不同 Expert 可分布在不同 GPU 上，天然适合并行

</v-clicks>

---

# MoE 基础

## 代表性工作一览

<br>

| 模型 | 年份 | Expert 数 | 激活参数 | 总参数 | 上下文长度 |
|------|------|-----------|----------|--------|-----------|
| **Switch Transformer** | 2021 | 128 | ~同 T5-Base | 1.6T | 512 |
| **GShard** | 2021 | 2048 | — | 600B | — |
| **Mixtral 8×7B** | 2023 | 8 | 13B | 47B | 32K |
| **DBRX** | 2024 | 16 (4 active) | 36B | 132B | 32K |
| **DeepSeek-V3** | 2024 | 256 (8 active) | 37B | 671B | 128K |

<v-clicks>

- 趋势：Expert 数量增多、激活比例降低、上下文窗口持续扩大
- MoE 已从研究走向**生产级部署**（Mixtral、DBRX、DeepSeek 均已开源）

</v-clicks>

---

# Long Context 基础

## 为什么 Long Context 难？

<v-clicks>

- **Self-Attention 的复杂度是 $O(n^2)$**：上下文长度翻倍 → 计算量和显存都变为 4 倍
- **KV Cache 显存爆炸**：推理时需缓存所有历史 token 的 Key/Value，128K 上下文可轻松占满 80GB GPU
- **位置编码外推困难**：训练时见过 4K 长度，推理时能否泛化到 32K、128K？
- **"Lost in the Middle"**：模型对中间位置的信息检索能力显著下降

</v-clicks>

<div v-click class="text-center text-sm opacity-70 mt-4">

上下文长度的演进：GPT-3 (2K) → GPT-3.5 (4K/16K) → GPT-4 (8K/128K) → Gemini 1.5 (1M/10M)

</div>

---

# Long Context 基础

## 位置编码方案

<br>

| 方案 | 核心思想 | 外推能力 |
|------|----------|----------|
| **Sinusoidal PE** | 固定的正弦/余弦函数 | ❌ 差 |
| **RoPE** | 旋转位置编码，将位置信息编码为旋转矩阵 | ⚠️ 有限 |
| **ALiBi** | 不用位置编码，直接在 attention score 上加距离惩罚 | ✅ 较好 |
| **NTK-aware Scaling** | 修改 RoPE 的基频，保留高频信息 | ✅ 好 |
| **YaRN** | 对 RoPE 不同频率分量分别缩放 | ✅✅ 很好 |

<v-clicks>

- RoPE 是当前主流方案（LLaMA、Mistral、Qwen 等均采用）
- 外推的关键挑战：**训练时没见过的位置，推理时能否正确编码？**

</v-clicks>

---

# Long Context 基础

## 高效注意力机制

<v-clicks>

- **Sliding Window Attention**
  - 每个 token 只关注局部窗口内的 token（如前后 4K）
  - 通过多层堆叠实现"间接"全局注意力
  - 代表：Mistral 7B, Longformer

- **Sparse Attention**
  - 结合局部窗口 + 全局 token + 随机连接
  - 将 $O(n^2)$ 降低到 $O(n\sqrt{n})$ 或 $O(n \log n)$
  - 代表：BigBird, LongT5

- **Flash Attention**
  - 不改变注意力的数学计算，而是**优化 GPU 内存访问模式**
  - 利用 tiling 技术避免 $O(n^2)$ 的中间矩阵写入 HBM
  - 实测加速 2-4×，显存降低 5-20×
  - 已成为长上下文训练的**标配基础设施**

</v-clicks>

---

# Long Context 基础

## 长上下文训练策略

<v-clicks>

- **渐进式扩展 (Progressive Extension)**
  - 先在短上下文上训练，再逐步扩展到长上下文
  - 节省训练成本：长序列训练的数据量可以较少

- **LongRoPE**
  - 搜索 RoPE 各维度的最优缩放因子
  - 支持从 4K 扩展到 2048K（200 万 token）

- **Continual Pre-training**
  - 在已有模型基础上，用长文本数据继续预训练
  - 代表：LLaMA 2 Long (32K)、CodeLlama (100K)

- **数据工程同样关键**
  - 长上下文训练需要**真正的长文档**（书籍、代码库、论文集）
  - 简单拼接短文本效果有限

</v-clicks>
