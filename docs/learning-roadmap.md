# 🗺️ Learning Roadmap — Data Structures & Algorithms in Python

> A structured path to mastering data structures and algorithms using the book by **Goodrich, Tamassia & Goldwasser**.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.14+** installed (see `pyproject.toml`)
- Basic Python syntax knowledge (variables, loops, functions, conditionals)
- A virtual environment set up:
  ```bash
  python -m venv .venv && source .venv/bin/activate
  pip install -e ".[dev]"
  ```
- A code editor (VS Code recommended) with Python extension

---

## 📦 Dependency Management — `pyproject.toml` vs `requirements.txt`

This project uses **`pyproject.toml`** (the modern Python standard) for dependency management. A `requirements.txt` is **not needed** for most of your learning journey, but here's when you might consider one:

### 🔹 Current setup (recommended)

```toml
# pyproject.toml
dependencies = []                    # Add 3rd-party libs here when needed
[project.optional-dependencies]
dev = ["pytest>=7.0"]               # Development-only tools
```

Install with:
```bash
pip install -e ".[dev]"
```

This is the **preferred approach** because:
- It's the official Python packaging standard (PEP 621)
- Single source of truth for your project metadata
- Works seamlessly with modern tools (build, publish, install)

### 🔸 When you might still want a `requirements.txt`

| Scenario | Action |
|----------|--------|
| **You need a 3rd-party library** (e.g., `numpy`, `matplotlib`, `networkx`) | Add it to `dependencies` in `pyproject.toml` |
| **You want to pin exact versions for reproducibility** | Generate a `requirements.txt` via `pip freeze > requirements.txt` |
| **You're deploying to a server / CI pipeline** | Create `requirements.txt` from `pyproject.toml` via `pip install -e . && pip freeze > requirements.txt` |
| **You're sharing code with someone who doesn't use `pyproject.toml`** | Provide a `requirements.txt` as a fallback |

### 🔹 For this project (data structures & algorithms)

> **💡 You likely won't need any external dependencies at all.** All data structures and algorithms in this book can be implemented using **only Python's standard library**. The `dependencies = []` list in your `pyproject.toml` is perfectly fine as-is.

If you later decide you want `requirements.txt`, you can generate it anytime:
```bash
pip freeze > requirements.txt
```

But for learning purposes, stick with `pyproject.toml` + `pip install -e ".[dev]"` — it's cleaner and more modern.

---

## 🧭 How to Use This Roadmap

Each **phase** builds on the previous one. Within each phase, chapters are ordered by dependency. For each chapter:

| Step | Action |
|------|--------|
| ① | **Read** the chapter in the book |
| ② | **Study** the code in `src/chXX_*/` |
| ③ | **Implement** the core data structure / algorithm from scratch in `exercises/` |
| ④ | **Practice** by solving exercises from the book (marked R/C/P) |
| ⑤ | **Test** your implementation with `pytest` in `tests/` |

---

## 🟢 Phase 1: Foundations

> **Goal**: Build the programming and analytical fundamentals needed for the rest of the book.

### Chapter 1 — Python Primer
- **Topics**: Objects, operators, control flow, functions, exceptions, iterators, comprehensions
- **Implement**: Write helper utilities you'll reuse later (linked lists, stack/queue base classes)
- **Exercises to try**: R-1.1 through R-1.12 (reinforcement), C-1.13 through C-1.28 (creativity)
- **✅ Milestone**: You can fluently read and write idiomatic Python

### Chapter 2 — Object-Oriented Programming
- **Topics**: Classes, inheritance, polymorphism, encapsulation, namespaces, shallow vs deep copies
- **Implement**: A simple `Sequence` abstract base class to understand inheritance
- **Key Pattern**: Abstract Data Types (ADTs) — the central design pattern of the book
- **Exercises to try**: R-2.1–R-2.9, C-2.10–C-2.16
- **✅ Milestone**: You can design your own ADT with proper encapsulation

### Chapter 3 — Algorithm Analysis
- **Topics**: Big-Oh, Omega, Theta notation, seven fundamental functions, experimental analysis
- **Implement**: Write timing scripts to experimentally verify asymptotic growth
- **Key Skill**: Learn to analyze any algorithm's time/space complexity
- **Exercises to try**: R-3.1–R-3.9, C-3.10–C-3.20
- **✅ Milestone**: You can analyze the runtime of any simple algorithm

### Chapter 4 — Recursion
- **Topics**: Linear recursion, binary recursion, multiple recursion, tail recursion, backtracking
- **Implement**: Recursive binary search, recursive file system traversal, Towers of Hanoi
- **Key Insight**: Every recursive solution can be iterative (and vice versa) — know both
- **Exercises to try**: R-4.1–R-4.8, C-4.9–C-4.19, P-4.22–P-4.25
- **✅ Milestone**: You can naturally think in terms of recursion

---

## 🟡 Phase 2: Core Data Structures

> **Goal**: Master the fundamental data structures that form the backbone of computer science.

### Chapter 5 — Array-Based Sequences
- **Topics**: Dynamic arrays, amortization, Python's list/tuple/str internals
- **Implement**: A dynamic array from scratch (similar to `list`)
- **Key Concept**: **Amortized analysis** — why `append` is O(1) on average
- **Exercises to try**: R-5.1–R-5.12, C-5.13–C-5.28, P-5.29–P-5.36
- **✅ Milestone**: You understand what's happening under the hood when you use a Python list

### Chapter 6 — Stacks, Queues, and Deques
- **Topics**: Stack ADT, Queue ADT, Deque ADT, array vs linked implementations
- **Implement**: `ArrayStack`, `LinkedQueue`, `CircularDeque`
- **Applications**: Matching delimiters, undo/redo, FIFO scheduling
- **Exercises to try**: R-6.1–R-6.8, C-6.9–C-6.21, P-6.22–P-6.24
- **✅ Milestone**: You can recognize stack/queue/deque application scenarios on sight

### Chapter 7 — Linked Lists
- **Topics**: Singly linked lists, doubly linked lists, circular linked lists, positional list ADT
- **Implement**: Singly linked list with header/trailer sentinels, doubly linked list, circular list
- **Key Insight**: Sentinels simplify edge cases dramatically
- **Exercises to try**: R-7.1–R-7.14, C-7.15–C-7.30, P-7.31–P-7.36
- **✅ Milestone**: You can implement and reverse any type of linked list in your sleep

### Chapter 8 — Trees
- **Topics**: General trees, binary trees, tree traversals (preorder/inorder/postorder/level-order), expression trees, Euler tours
- **Implement**: `LinkedBinaryTree`, recursive traversals, expression tree evaluation
- **Applications**: File system hierarchy, HTML DOM, expression parsing
- **Exercises to try**: R-8.1–R-8.17, C-8.18–C-8.44, P-8.45–P-8.52
- **✅ Milestone**: You can recursively solve any tree problem

---

## 🟠 Phase 3: Advanced Structures & Algorithms

> **Goal**: Dive deeper into specialized data structures and sorting/selection algorithms.

### Chapter 9 — Priority Queues
- **Topics**: Priority queue ADT, binary heap, heap-sort, adaptable priority queues
- **Implement**: Binary heap (min-heap), heap-sort, `AdaptableHeapPriorityQueue`
- **Key Concept**: The heap is a **complete binary tree** stored in an array
- **Applications**: Task scheduling, Dijkstra's algorithm, event-driven simulation
- **Exercises to try**: R-9.1–R-9.14, C-9.15–C-9.30, P-9.31–P-9.36
- **✅ Milestone**: You understand why heap-sort is O(n log n) in all cases

### Chapter 10 — Maps, Hash Tables, and Skip Lists
- **Topics**: Map ADT, hash functions, collision resolution (separate chaining, open addressing), sorted maps, skip lists
- **Implement**: `HashMap` (separate chaining), `ProbeHashMap` (linear probing), `SortedTableMap`, `SkipList`
- **Key Concept**: A good hash function spreads keys uniformly
- **Exercises to try**: R-10.1–R-10.18, C-10.19–C-10.40, P-10.41–P-10.50
- **✅ Milestone**: You understand what makes a good hash function and when to use which map

### Chapter 11 — Search Trees
- **Topics**: Binary search trees, AVL trees, splay trees, (2,4) trees, red-black trees
- **Implement**: BST, AVL tree (with rotations), red-black tree
- **Key Insight**: Balanced trees ensure O(log n) operations — the balancing logic is the hard part
- **Exercises to try**: R-11.1–R-11.19, C-11.20–C-11.47, P-11.48–P-11.55
- **✅ Milestone**: You can manually trace insertions/rotations in an AVL or red-black tree

### Chapter 12 — Sorting and Selection
- **Topics**: Merge-sort, quick-sort, bucket sort, radix sort, selection algorithms (quick-select)
- **Implement**: Merge-sort (top-down and bottom-up), quick-sort (in-place with Lomuto/Hoare partition), randomized quick-select
- **Key Comparison**: Merge-sort vs quick-sort vs heap-sort — when to use each
- **Exercises to try**: R-12.1–R-12.16, C-12.17–C-12.36, P-12.37–P-12.47
- **✅ Milestone**: You can analyze and implement any comparison-based sort

---

## 🔴 Phase 4: Applications & Advanced Topics

> **Goal**: Apply data structures to real-world problems and explore advanced topics.

### Chapter 13 — Text Processing
- **Topics**: Pattern matching (Brute-force, KMP, Boyer-Moore), tries, Huffman coding, longest common subsequence (LCS)
- **Implement**: KMP algorithm, Huffman coding (compress + decompress), LCS with DP
- **Key Insight**: Text algorithms show the power of clever precomputation (failure functions, prefix tables)
- **Exercises to try**: R-13.1–R-13.12, C-13.13–C-13.30, P-13.31–P-13.38
- **✅ Milestone**: You understand how your text editor's "find" feature works under the hood

### Chapter 14 — Graph Algorithms
- **Topics**: Graph ADT, DFS, BFS, topological sort, shortest paths (Dijkstra, Bellman-Ford), MST (Prim, Kruskal)
- **Implement**: Adjacency list graph, DFS/BFS, Dijkstra, Prim's, Kruskal's (with union-find)
- **Applications**: GPS navigation, social networks, web crawling, network routing
- **Exercises to try**: R-14.1–R-14.24, C-14.25–C-14.49, P-14.50–P-14.66
- **✅ Milestone**: You can model real-world problems as graphs and apply the right algorithm

### Chapter 15 — Memory Management & B-Trees
- **Topics**: Garbage collection, caching strategies, external memory, B-trees
- **Implement**: A simple B-tree with insertion and search
- **Key Concept**: B-trees are the data structure behind databases and file systems
- **Exercises to try**: R-15.1–R-15.12, C-15.13–C-15.17, P-15.18–P-15.19
- **✅ Milestone**: You understand how databases organize data on disk

---

## 🏗️ Suggested Project Milestones

Build these projects as you progress to solidify your understanding:

| Phase | Project | Concepts Used |
|-------|---------|---------------|
| 🟢 | **HTML Tag Validator** | Stack, parsing |
| 🟡 | **Expression Calculator** | Stack, tree, recursion |
| 🟡 | **File System Tree Viewer** | Tree traversals |
| 🟠 | **Task Scheduler** | Priority queue, heap |
| 🟠 | **Spell Checker** | Hash table, trie |
| 🔴 | **Web Crawler** | Graph, BFS, hash table |
| 🔴 | **Route Planner** | Graph, Dijkstra, MST |
| 🔴 | **Text File Compressor** | Huffman coding |

---

## 📅 Suggested Timeline

| Duration | Phase | Commitment |
|----------|-------|------------|
| Weeks 1–2 | 🟢 Foundations (Ch 1–4) | 5–7 hrs/week |
| Weeks 3–5 | 🟡 Core Structures (Ch 5–8) | 6–8 hrs/week |
| Weeks 6–8 | 🟠 Advanced Structures (Ch 9–12) | 7–10 hrs/week |
| Weeks 9–11 | 🔴 Applications (Ch 13–15) | 8–10 hrs/week |
| Week 12+ | 🧪 Review & Projects | as needed |

> ⏱️ Adjust based on your pace — the goal is deep understanding, not speed.

---

## 🧪 Testing Strategy

Write tests as you go using `pytest`:

```bash
# Run all tests
pytest

# Run tests for a specific chapter
pytest tests/ch06_stacks_queues/

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src
```

Your project is already configured with `pytest` in the dev dependencies:
```bash
pip install -e ".[dev]"
```

---

## 📚 Additional Resources

| Resource | Link |
|----------|------|
| Book Companion Site | [wiley.com/college/goodrich](https://www.wiley.com/college/goodrich) |
| Python Official Docs | [docs.python.org/3](https://docs.python.org/3/) |
| Big-O Cheat Sheet | [bigocheatsheet.com](https://www.bigocheatsheet.com) |
| VisuAlgo (algorithm visualization) | [visualgo.net](https://visualgo.net) |
| LeetCode (practice) | [leetcode.com](https://leetcode.com) |
| GeeksforGeeks | [geeksforgeeks.org](https://www.geeksforgeeks.org) |

---

## 💡 Tips for Success

1. **Code every algorithm by hand** — don't just read the code, type it out
2. **Trace through examples** on paper before running code
3. **Draw diagrams** — especially for trees, graphs, and pointer manipulations
4. **Explain concepts out loud** — teaching is the best way to learn
5. **Re-implement from memory** after a few days to check retention
6. **Don't skip the math** — Big-Oh analysis is what separates "knowing" from "mastering"
7. **Use the exercises** — R (reinforcement) builds confidence, C (creativity) builds depth, P (projects) builds application skills

---

> 🚀 **Consistency beats intensity. Study a little every day rather than cramming. Happy learning!**
