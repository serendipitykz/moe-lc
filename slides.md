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

---

## 为什么 MoE 适合 Long Context

### 核心优势

- **稀疏激活降低计算量**
  - 每个 token 仅激活 top-k experts（通常 k=1 或 2）
  - 总 FLOPs ≈ Dense 模型的 1/8 ~ 1/4，但容量接近 8x 参数
  
- **并行化友好**
  - Expert 间无依赖，天然适合 Expert Parallelism
  - Long sequence 可在 expert 维度分摊计算压力

- **内存效率**
  - 激活值仅存储活跃 expert 的中间结果
  - KV Cache 增长与 sequence length 线性相关，MoE 不额外放大

### 实验证据

| 模型类型 | 32k Context 推理速度 | 显存占用 |
|---------|---------------------|---------|
| Dense 7B | 1.0x (baseline) | 24 GB |
| MoE 8×7B | **2.3x** | 26 GB |

---

## 前沿工作：MoE × Long Context 的工程实践

### 代表性模型

**Mixtral 8×7B (2023.12)**
- 32k context window with Sliding Window Attention
- 每层 8 个 experts，top-2 routing
- 推理时仅激活 ~13B 参数，性能超越 Llama2-70B

**DBRX (2024.03, Databricks)**
- 16 experts per layer, fine-grained MoE
- 支持 32k context，优化了 expert load balancing

**Jamba (2024.03, AI21 Labs)**
- **Mamba (SSM) + MoE** 混合架构
- 256k context length，O(n) 复杂度
- 在 long-range dependency 任务上超越纯 Transformer

**DeepSeek-V2/V3 (2024)**
- Multi-head Latent Attention (MLA) + MoE
- 128k context，极致的 KV Cache 压缩

---

## 架构设计选择：MoE 遇上 Long Context 的工程权衡

### 关键设计维度

**1. MoE 层的频率**
- 全层 MoE：最大容量，但通信开销大
- 交替 MoE：奇数层 Dense + 偶数层 MoE（如 Mixtral）
- **Long Context 场景推荐**：浅层 Dense（捕捉局部模式）+ 深层 MoE（全局推理）

**2. Expert 数量与粒度**
- 粗粒度（8-16 experts）：通信高效，但专家化不足
- 细粒度（64-128 experts）：更强专业化，需要更复杂的 routing

**3. Shared Expert 机制**
- 部分 experts 对所有 token 激活（如 DeepSeek-V2）
- 作用：稳定训练 + 保留 dense 模型的泛化能力

### 实践建议

```python
# 伪代码：Long Context MoE 层配置
if layer_depth < total_layers * 0.3:
    use_dense_ffn()  # 浅层用稠密层
else:
    use_moe_ffn(
        num_experts=16,
        top_k=2,
        shared_expert=True,  # 添加 shared expert
        capacity_factor=1.25  # 长序列需要更大容量
    )
```

---

## Demo 介绍：动手体验 MoE × Long Context

### Demo 目标

通过交互式对比实验，直观感受：
1. **Dense vs MoE 推理效率对比**
   - 相同任务下的速度、显存、输出质量
2. **Long Context 检索任务**
   - "大海捞针"测试：在 32k token 文档中定位关键信息

### 操作方式

```
📱 扫描二维码 / 访问链接
🖱️ 选择模型类型（Dense 7B / MoE 8×7B）
⌨️ 输入测试 prompt 或使用预设场景
📊 实时查看推理指标与结果
```

### 预设场景

| 场景 | 描述 | 上下文长度 |
|------|------|-----------|
| 📄 文档问答 | 从技术手册中提取特定参数 | 16k tokens |
| 📚 多文档推理 | 跨 5 篇论文总结共同结论 | 28k tokens |
| 🔍 精确检索 | 在代码库中找到特定函数调用 | 32k tokens |

---

## Demo 页面：交互式体验

### 实验面板

<div style="border: 2px solid #e0e0e0; border-radius: 8px; padding: 20px; background: #fafafa;">

**输入区域**
```
Prompt: "请在以下 32k token 的日志文件中，
找到第一次出现 'OutOfMemoryError' 的时间戳和堆栈信息。"

[上传文件] 或 [使用示例数据]
```

**模型选择**
- ⚪ Dense 7B (Llama2-7B)  
- 🔘 MoE 8×7B (Mixtral-8×7B)

**[开始推理]**

---

**实时指标对比**

|  | Dense 7B | MoE 8×7B |
|---|---------|----------|
| ⏱️ 推理时间 | 8.3s | **3.6s** |
| 💾 峰值显存 | 24.1 GB | **26.4 GB** |
| 🎯 激活参数 | 7B | **~13B** |
| ✅ 准确定位 | ✓ | ✓ |

**输出结果**
```
✓ 找到目标：时间戳 2024-01-15 14:23:17
堆栈：java.lang.OutOfMemoryError: Java heap space
    at DataProcessor.loadBatch(DataProcessor.java:142)
    ...
```

</div>

### 可视化

```
[Expert Activation Heatmap]
显示 32k tokens 在 8 个 experts 上的分配模式

Token 0-8k:   ████░░░░ (Expert 0,1 高激活)
Token 8k-16k: ░░████░░ (Expert 2,3 高激活)
Token 16k-24k:░░░░██░░ (Expert 4,5 高激活)
Token 24k-32k:░░░░░░██ (Expert 6,7 高激活)
```

**观察要点**：
- MoE 模型在不同文本段落激活不同 expert
- 速度提升 ~2.3x，显存仅增加 10%
- 长文本场景下 MoE 的稀疏激活优势明显

---

## Key Takeaways：核心要点回顾

### 1️⃣ MoE 通过稀疏激活实现高效扩展
- 总参数 ≫ 激活参数，以 sublinear 成本获得 model capacity
- Top-k routing 机制让每个 token 只"咨询"少数专家
- **关键挑战**：负载均衡、训练稳定性

### 2️⃣ Long Context 需要架构与训练的协同创新
- 位置编码外推（RoPE, ALiBi）+ 高效注意力（Flash Attention, Sliding Window）
- 渐进式上下文扩展策略（YaRN, LongRoPE）
- **瓶颈**：O(n²) 复杂度、KV Cache 显存墙

### 3️⃣ MoE × Long Context = 1 + 1 > 2
- 稀疏激活天然降低长序列的计算开销
- Expert Parallelism 分摊长文本的推理压力
- **前沿实践**：Mixtral (32k), Jamba (256k), DeepSeek-V3 (128k)

### 4️⃣ 工程实践的权衡艺术
- MoE 层频率、Expert 粒度、Shared Expert 机制
- 通信开销 vs 计算效率、专业化 vs 泛化能力
- **没有银弹**：需根据任务、硬件、数据特点定制

### 5️⃣ 这只是开始，不是终点
- MoE 和 Long Context 仍在快速演进
- 新架构（Mamba, RWKV）与 MoE 的结合充满可能
- **保持批判性思考**：不盲从 scaling law

---

## 开放问题与批判性思考

### 🤔 MoE 是 Scaling 的最优路径吗？

**支持观点**
- ✅ 参数效率：相同 FLOPs 下容量更大
- ✅ 推理友好：激活参数少，速度快
- ✅ 模块化：易于增量扩展和专家替换

**质疑声音**
- ❌ **训练复杂度**：负载均衡、expert collapse 难调试
- ❌ **通信瓶颈**：跨节点 Expert Parallelism 带宽要求高
- ❌ **泛化风险**：过度专业化可能损害 zero-shot 能力
- ❌ **Alternative 存在**：Dense 模型 + 更好的压缩（如 MQA, GQA）也能高效

### 🔮 Long Context 的上限在哪？

**技术边界**
- **1M tokens？** 当前 Gemini 1.5 已达到，但实用性存疑
- **位置编码崩溃**：超长距离的相对位置表示仍是难题
- **Lost in the Middle**：模型在超长文本中间部分的注意力衰减

**根本问题**
- **人类真的需要 1M context 吗？** 还是需要更好的检索 + 推理？
- **Retrieval-Augmented Generation (RAG)** 可能是更实用的方案
- **认知科学启示**：人类的工作记忆也是有限的，或许"分而治之"才是正道

### 💡 未来方向

**混合架构**
- Mamba (SSM) + MoE：O(n) 复杂度 + 稀疏激活
- Transformer + RWKV：全局注意力 + 线性 RNN

**动态计算**
- Adaptive routing：根据 token 难度动态分配计算
- Early exit：简单 token 提前输出，节省深层计算

**硬件协同**
- 专用 MoE 加速器（如 Google TPU v5）
- 内存层次优化：HBM + DRAM 协同管理 KV Cache

---

## Q&A / 参考文献

### 📚 核心论文

**MoE 基础**
- Shazeer et al. (2017) "Outrageously Large Neural Networks: The Sparsely-Gated MoE Layer"
- Fedus et al. (2022) "Switch Transformers: Scaling to Trillion Parameter Models"
- Jiang et al. (2024) "Mixtral of Experts" [Technical Report]

**Long Context**
- Su et al. (2021) "RoFormer: Enhanced Transformer with Rotary Position Embedding"
- Press et al. (2022) "Train Short, Test Long: Attention with Linear Biases (ALiBi)"
- Dao et al. (2022) "FlashAttention: Fast and Memory-Efficient Exact Attention"
- Peng et al. (2023) "YaRN: Efficient Context Window Extension"

**MoE × Long Context**
- AI21 Labs (2024) "Jamba: A Hybrid Transformer-Mamba Language Model"
- DeepSeek AI (2024) "DeepSeek-V2: A Strong MoE Language Model"
- Databricks (2024) "DBRX: A New State-of-the-Art Open LLM"

### 🙏 致谢

感谢各位的聆听！

**开源社区**: Hugging Face, vLLM, TGI  
**研究团队**: Mistral AI, DeepSeek, AI21 Labs  
**硬件支持**: [如有赞助商可列出]

### 💬 Q&A

**现在欢迎提问！**

常见问题：
- 如何选择 MoE vs Dense 模型？
- Long Context 训练的数据准备？
- 生产环境部署 MoE 的最佳实践？

**联系方式**  
📧 [your-email]  
🐙 GitHub: [your-repo]  
🔗 Slides & Code: [demo-link]s