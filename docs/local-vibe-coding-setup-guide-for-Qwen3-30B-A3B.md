# Local Vibe Coding Setup Guide — Qwen3-30B-A3B-4bit on Apple Silicon

> **Hardware:** MacBook Pro M1 Max · 64 GB unified memory  
> **Model:** `mlx-community/Qwen3-30B-A3B-4bit` (MoE — 30B total / 3B active params)  
> **Runtime:** oMLX (MLX-based inference server)  
> **Measured decode speed:** 42.1 tok/s · Prefix hit rate: 75.9 %

---

## Table of Contents

1. [Why This Model for Vibe Coding](#1-why-this-model-for-vibe-coding)
2. [Hardware Reality Check](#2-hardware-reality-check)
3. [Runtime Comparison — MLX vs llama.cpp vs Ollama](#3-runtime-comparison--mlx-vs-llamacpp-vs-ollama)
4. [oMLX Configuration](#4-omlx-configuration)
5. [Cache Architecture](#5-cache-architecture)
6. [Context Window Strategy](#6-context-window-strategy)
7. [Performance Profiles](#7-performance-profiles)
8. [Prefill vs Decode — Know Your Bottleneck](#8-prefill-vs-decode--know-your-bottleneck)
9. [GPU Upgrade Considerations](#9-gpu-upgrade-considerations)
10. [Maintenance](#10-maintenance)
11. [Quick Reference](#11-quick-reference)

---

## 1. Why This Model for Vibe Coding

Qwen3-30B-A3B is a **Mixture-of-Experts (MoE)** model. This architecture is unusually well-suited for local inference on Apple Silicon:

| Property | Dense 30B | Qwen3-30B-A3B (MoE) |
|---|---|---|
| Total parameters | 30B | 30B |
| Active parameters per token | 30B | **3B** |
| Memory for weights (Q4) | ~15–17 GB | ~15–17 GB |
| KV cache per token | ~0.8 MB | **~48 KB** |
| Decode bottleneck | Bandwidth | **Bandwidth (lighter)** |
| Prefill bottleneck | Compute | **Compute (lighter)** |

The MoE architecture means only 3B parameters are activated per forward pass. Unified memory never needs to round-trip through PCIe, and the KV cache stays compact — critical advantages on Apple Silicon.

**At Q4 quantisation, the model weight footprint is ~15–17 GB**, leaving ~47 GB of the 64 GB unified pool for OS, KV cache, and hot cache.

---

## 2. Hardware Reality Check

### M1 Max 64 GB — Memory Budget

```
Total unified memory              64.0 GB
─────────────────────────────────────────
macOS + background apps           ~8–9 GB
Model weights (Q4)               ~15–17 GB
oMLX hot cache (configured)       28.0 GB
  └─ currently used                9.4 GB
─────────────────────────────────────────
Headroom                         ~10–13 GB
```

### Key Specs

| Metric | Value |
|---|---|
| Memory bandwidth | 400 GB/s |
| GPU compute (FP16 Matrix) | ~20 TFLOPS |
| Unified memory | No PCIe bottleneck |
| KV cache cost at 128k context | ~6.1 GB |

### What Fits Comfortably

- ✅ Model weights in unified memory at full bandwidth
- ✅ 64k context — KV cache ~3.1 GB
- ✅ 128k context — KV cache ~6.1 GB (within hot cache headroom)
- ✅ All inference served from RAM, never touching SSD during decode

---

## 3. Runtime Comparison — MLX vs llama.cpp vs Ollama

Benchmarked on Qwen3.5-35B-A3B (equivalent MoE architecture), M4 Max 128 GB:

| Runtime | Tok/s | Notes |
|---|---|---|
| MLX Python native | ~130 | Fastest; no HTTP overhead |
| MLX HTTP server | ~90–108 | What tools like Cursor/Continue see |
| llama.cpp (Metal) | ~71 | Solid; GGUF format; broad compatibility |
| Ollama (llama.cpp backend) | ~43 | Most convenient; HTTP + JSON overhead |

> **Key insight:** llama.cpp's Metal backend translates CUDA compute patterns into Metal shaders. MLX is built from the ground up for Apple Silicon's unified memory architecture — it never performs unnecessary memory copies that UMA makes redundant.

### MoE Amplifies the MLX Advantage

- Dense models: MLX ~1.4–1.6× faster than llama.cpp
- **MoE models: MLX up to 3× faster than llama.cpp**

Qwen3-30B-A3B is MoE. Use MLX.

### Effective Throughput vs Reported Speed

The tok/s figure shown in any UI measures the **decode phase only**. Real-world effective throughput also includes prefill:

```
Effective throughput = output tokens ÷ total wall-clock time
```

At long contexts (8k+ input tokens), prefill can dominate total time. At 8.5k context, prefill accounts for ~94% of total wall-clock time. This is where prefix caching matters most (see §5).

---

## 4. oMLX Configuration

### Recommended Settings

```
Max Context Window:      128k   (KV cache cost only ~6.1 GB — fits easily)
Max Tokens:              8k     (sufficient for code generation tasks)
Hot Cache Limit:         28 GB  (sweet spot — 3× actual usage, safe OS headroom)
```

> **Hot cache ceiling:** oMLX caps the hot cache at 50% of system RAM. On 64 GB, the maximum is 32 GB. The current 28 GB setting is the recommended sweet spot — increasing to 32 GB provides marginal benefit while tightening OS headroom.

### Why 128k Context is Safe Here

Unlike dense models, the MoE KV cache is compact:

```
KV cache cost (measured):  ~48 KB per token

32k context  →  ~1.5 GB
64k context  →  ~3.1 GB
128k context →  ~6.1 GB   ← fits within 28 GB hot cache with 12+ GB headroom
```

The earlier rule of thumb (dense model at ~0.8 MB/token) does not apply to this MoE architecture.

### Paths

```
Active base_path:         ~/.omlx
SSD cache directory:      ~/.omlx/cache
Response-state:           ~/.omlx/cache/response-state
```

---

## 5. Cache Architecture

oMLX implements a **two-tier prefix cache** — hot memory + persistent SSD. This is the single most impactful performance feature for vibe coding.

```
┌─────────────────────────────────────────────┐
│            Incoming Request                 │
└─────────────────┬───────────────────────────┘
                  │
          Prefix match?
         /              \
       Yes               No
        │                 │
  ┌─────▼──────┐    ┌─────▼──────┐
  │ Memory     │    │ SSD Cache  │
  │ Cache      │    │ (persist.) │
  │ 9.4/28 GB  │    │ 36.8/92 GB │
  │ 97 blocks  │    │ 537 files  │
  └─────┬──────┘    └─────┬──────┘
        │                 │
   Serve at          Load to RAM,
   400 GB/s          then serve
        │                 │
        └────────┬────────┘
                 │
          Decode phase
          (42.1 tok/s)
```

### Observed Cache Health

| Metric | Value | Assessment |
|---|---|---|
| Memory used | 9.4 / 28 GB (33%) | ✅ Plenty of headroom |
| SSD used | 36.8 / 92 GB (40%) | ✅ Comfortable |
| Block size | 2048 tokens | — |
| Indexed blocks (memory) | 97 | — |
| SSD files | 537 | ~1.1M tokens of persistent KV cache |
| **Prefix Hit Rate** | **75.9%** | ✅ Excellent for vibe coding |
| **Memory Hit Rate** | **100%** | ✅ All hits served from RAM |
| Memory Evictions | 0 | ✅ No pressure |
| Prefix Evictions | 0 | ✅ No pressure |

### What 75.9% Prefix Hit Rate Means

Three quarters of requests skip prefill entirely. For vibe coding, the things being cached are exactly the right things:

- System prompt (reused every turn)
- Open file contents (reused across edits)
- Conversation history (reused for follow-up questions)

The 42.1 tok/s decode speed is the **floor**. In practice, cached requests feel significantly faster because the prefill wait disappears.

### SSD Tier as Long-Term Memory

```
537 SSD files × 2048 tokens/block = ~1.1M tokens of persistent KV state
```

Previously computed KV blocks survive restarts. Reopening the same project files the next day hits the SSD cache, which loads into memory — the cold-start prefill cost is paid only once per unique context.

---

## 6. Context Window Strategy

### Choosing Your Context Window

| Context | KV Cache | Practical capacity | Recommendation |
|---|---|---|---|
| 32k | ~1.5 GB | ~5–6 large files + history | Minimum for serious coding |
| 64k | ~3.1 GB | ~10–12 large files + history | Good default |
| **128k** | **~6.1 GB** | **~entire medium codebase** | **Recommended for this setup** |

### 128k Context — First Hit vs Cached

```
First hit (novel 128k context):
  Prefill:  slow (compute-bound, O(n²) attention)
  Cost:     paid once, then cached to SSD

Subsequent hits (same files / system prompt):
  Prefix cache hit → skip prefill entirely
  Effective speed: decode-only (42.1 tok/s)
```

For vibe coding where you return to the same codebase repeatedly, the first-hit cost amortises quickly across your session.

### When 128k Matters

- Loading an entire repo as context for refactoring
- Long design document + codebase combinations
- Extended multi-file coding sessions without truncation

---

## 7. Performance Profiles

### Decode Speed by Context (estimated)

```
Short context   (<4k tokens):   42+ tok/s  (full speed, minimal attention overhead)
Medium context  (16k tokens):   ~38–42 tok/s
Long context    (64k tokens):   ~35–40 tok/s
Very long       (128k tokens):  ~30–38 tok/s
```

Decode speed degrades slowly with context because attention over the KV cache grows — but the MoE architecture keeps this lighter than a dense model.

### Effective Throughput with Caching

```
Cache miss (novel context):   42.1 tok/s decode, plus prefill wait
Cache hit (75.9% of turns):   ~42.1 tok/s effective (no prefill)

Weighted average effective throughput ≈ 42.1 × 0.759 + (42.1 × penalty) × 0.241
```

In practice, vibe coding sessions feel close to the full decode speed because system prompts and file contents almost always hit the cache after the first turn.

---

## 8. Prefill vs Decode — Know Your Bottleneck

Understanding which phase is slow tells you what hardware actually helps.

| Phase | What happens | Bottleneck | Scales with |
|---|---|---|---|
| **Prefill** | All input tokens processed in parallel | Compute (TFLOPS) | Matrix multiply throughput |
| **Decode** | One token generated at a time | Memory bandwidth (GB/s) | How fast weights are read |

### Implications

- **Faster GPU memory bandwidth** → faster decode (token generation)
- **Higher TFLOPS** → faster prefill (processing your input)
- **Prefix caching** → eliminates prefill cost entirely for repeated context

On M1 Max, the 400 GB/s unified memory bandwidth drives the 42.1 tok/s decode rate. Prefill on novel long contexts is compute-limited at ~20 TFLOPS FP16.

---

## 9. GPU Upgrade Considerations

If you add a discrete GPU (e.g. AMD Radeon AI PRO R9600 in a connected workstation):

### R9600 Key Specs

| Metric | M1 Max | R9600 |
|---|---|---|
| Memory bandwidth | 400 GB/s | 640 GB/s |
| FP16 Matrix (prefill) | ~20 TFLOPS | 99 TFLOPS |
| INT4 TOPS | ~38 TOPS | 794 TOPS |
| VRAM | 64 GB (unified) | 32 GB (dedicated) |

### What Gets Better

- **Decode speed:** ~60–67 tok/s (vs 42.1) — bandwidth scaling: 42.1 × (640/400) × 0.87 ROCm efficiency
- **Prefill speed:** ~5× faster — compute scaling from 20 → 99 TFLOPS
- **128k first-hit prefill:** minutes → ~30–60 seconds

### What Does Not Change

- Prefix cache hit rate (75.9%) — this is workflow-dependent, not hardware-dependent
- Quality of cached responses
- Context window limits (software-configured)

### Requirements for Full R9600 Performance

- Linux with ROCm 6.4+ (Windows ROCm support remains limited)
- llama.cpp ROCm backend or ROCm-enabled MLX equivalent
- Flash Attention support on ROCm for efficient long-context prefill

### Verdict for Current Setup

Given the 75.9% cache hit rate, most sessions never hit the prefill bottleneck in practice. The R9600 is most valuable for workflows that regularly introduce **novel long contexts** — full repo loads, large document ingestion, or multi-codebase work.

---

## 10. Maintenance

### SSD Cache Growth

The SSD cache grows with each unique 2048-token block. Monitor periodically:

```bash
du -sh ~/.omlx/cache
```

Prune when disk space is a concern:

```bash
# Remove all cached response state (cache rebuilds automatically on next use)
rm -rf ~/.omlx/cache/response-state/*
```

> **Note:** Clearing the SSD cache removes all persisted KV blocks. The first session after clearing will re-prefill all contexts. Memory cache rebuilds within one session.

### Health Check

Key metrics to watch in the oMLX cache dashboard:

| Metric | Healthy | Action needed |
|---|---|---|
| Memory Hit Rate | 100% | — |
| Prefix Hit Rate | >60% | If lower, system prompt or file paths may be changing between turns |
| Memory Evictions | 0 | If >0, consider raising hot cache limit (max 32 GB on 64 GB RAM) |
| Prefix Evictions | 0 | If >0, hot cache is under pressure |
| Memory used | <80% of limit | If >80%, raise hot cache limit |

---

## 11. Quick Reference

### Settings Summary

```
Model:               mlx-community/Qwen3-30B-A3B-4bit
Runtime:             oMLX (MLX backend)
Max Context Window:  128k
Max Tokens:          8k
Hot Cache Limit:     28 GB  (max: 32 GB = 50% of 64 GB RAM)
```

### Performance Summary

```
Decode speed:        42.1 tok/s  (memory bandwidth bound, 400 GB/s)
Prefix hit rate:     75.9%       (most turns skip prefill entirely)
Memory hit rate:     100%        (all cache hits served from RAM)
KV cache cost:       ~48 KB/token (MoE — much lighter than dense models)
128k context cost:   ~6.1 GB     (well within 28 GB hot cache)
```

### Why This Stack Works

```
MoE architecture   → compact KV cache, only 3B params active per token
MLX runtime        → built for Apple Silicon UMA, up to 3× faster than llama.cpp on MoE
Two-tier cache     → 75.9% of turns skip prefill; SSD persists across restarts
128k context       → entire codebases fit; first-hit cost amortised by cache
Unified memory     → no PCIe bottleneck; full 400 GB/s to every byte of the model
```

---

*Generated from a live benchmarking session on MacBook Pro M1 Max 64 GB · May 2026*
