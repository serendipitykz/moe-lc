# Presentation Roadmap — MoE & Long Context

> 总时长约 45 分钟，面向初学者，中文讲解为主，术语保留英文。

## 第一部分：开场与背景 (≈5 min)

| Slide # | 标题 | 要点 |
|---------|------|------|
| 1 | Title Slide | 课程名、演讲标题、演讲者 |
| 2 | 目录 | 自动生成 `<Toc>` |
| 3 | 背景介绍 — 为什么关注 MoE & Long Context | 参数量增长趋势、长文本需求、MoE 的价值 |
| 4 | 背景介绍 — 核心问题 | "大"与"长"的矛盾，MoE × Long Context 的交汇 |
| 5 | 背景介绍 — 路线图 | 本次 Presentation 各章节概览表 |

## 第二部分：MoE 基础 (≈10 min)

| Slide # | 标题 | 要点 |
|---------|------|------|
| 6 | MoE 是什么 | 稀疏 vs 稠密模型；MoE Layer 结构图解（Router + N Experts） |
| 7 | Gating / Routing 机制 | Top-k gating、Softmax 门控、token → expert 分配流程 |
| 8 | 训练挑战与负载均衡 | Expert collapse、Auxiliary loss、Capacity factor |
| 9 | 代表性工作 | Switch Transformer, GShard, Mixtral; 参数量 vs 激活量对比 |

## 第三部分：Long Context 基础 (≈10 min)

| Slide # | 标题 | 要点 |
|---------|------|------|
| 10 | 为什么 Long Context 难 | O(n²) attention、显存瓶颈、位置编码外推 |
| 11 | 位置编码方案 | RoPE、ALiBi、NTK-aware Scaling；外推能力对比 |
| 12 | 高效注意力机制 | Sliding Window、Sparse Attention、Flash Attention |
| 13 | 长上下文训练策略 | 渐进式扩展、YaRN、LongRoPE |

## 第四部分：MoE × Long Context (≈8 min)

| Slide # | 标题 | 要点 |
|---------|------|------|
| 14 | 为什么 MoE 适合 Long Context | 稀疏激活降低 FLOPs、Expert 可并行 |
| 15 | 前沿工作 | Mixtral 8x7B (32k ctx)、DBRX、Jamba (Mamba + MoE)、DeepSeek-V2/V3 |
| 16 | 架构设计选择 | MoE 层频率、Expert 数量、Shared Expert |

## 第五部分：Demo / 动手体验 (≈7 min)

| Slide # | 标题 | 要点 |
|---------|------|------|
| 17 | Demo 介绍 | 说明 demo 目标与操作方式 |
| 18 | Demo 页面 | 交互式体验（如：对比 Dense vs MoE 推理、或 Long Context 检索任务） |

## 第六部分：总结与展望 (≈5 min)

| Slide # | 标题 | 要点 |
|---------|------|------|
| 19 | Key Takeaways | 3-5 条核心结论 |
| 20 | 开放问题与批判性思考 | MoE 是否是 scaling 的最优路径？Long Context 的上限在哪？ |
| 21 | Q&A / 参考文献 | 引用列表、致谢 |

---

## 进度追踪

- [x] 第一部分：开场与背景 (Slides 1-5)
- [x] 第二部分：MoE 基础 (Slides 6-9)
- [x] 第三部分：Long Context 基础 (Slides 10-13)
- [ ] 第四部分：MoE × Long Context (Slides 14-16)
- [ ] 第五部分：Demo (Slides 17-18)
- [ ] 第六部分：总结与展望 (Slides 19-21)
- [ ] Manuscript 完善
- [ ] 样式 / 主题调优
