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
