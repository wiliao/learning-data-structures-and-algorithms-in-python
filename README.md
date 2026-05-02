# Data Structures and Algorithms in Python

> 📘 Companion repository for *"Data Structures and Algorithms in Python"* by Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser

[![Python](https://img.shields.io/badge/Python-3.1+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Book](https://img.shields.io/badge/Book-Wiley-0077B5.svg)](https://www.wiley.com/college/goodrich)

---

## 📖 Book Overview

**Data Structures and Algorithms in Python** provides a comprehensive introduction to data structures and algorithms, emphasizing their design, analysis, and implementation using Python 3.1+. This textbook is designed for:

- Beginning-level data structures courses
- Intermediate-level introduction to algorithms courses
- Self-study for software engineers and computer science students

### 🎯 Learning Outcomes

By studying this book, readers will:

✅ Understand common data collection abstractions (stacks, queues, lists, trees, maps)  
✅ Master algorithmic strategies for efficient data structure implementations  
✅ Analyze algorithmic performance theoretically and experimentally  
✅ Wisely use existing data structures in Python's standard library  
✅ Gain hands-on experience implementing foundational data structures  
✅ Apply data structures and algorithms to solve complex real-world problems  

### 🔑 Key Features

- **Object-Oriented Approach**: Consistent use of ADTs and design patterns throughout
- **Complete Python Implementations**: Nearly all data structures and algorithms include working code
- **Real-World Applications**: File systems, cryptography, text analysis, Huffman coding, DNA alignment, search engines
- **450+ Illustrations**: Visual aids to clarify complex concepts
- **750+ Exercises**: Reinforcement, creativity, and project problems with varying difficulty
- **Online Resources**: Source code, hints, solutions, slides at [wiley.com/college/goodrich](https://www.wiley.com/college/goodrich)

---

## 📚 Table of Contents

### Part I: Foundations
| Chapter | Topic | Key Concepts |
|---------|-------|-------------|
| 1 | Python Primer | Objects, operators, control flow, functions, exceptions, iterators |
| 2 | Object-Oriented Programming | Classes, inheritance, encapsulation, design patterns, namespaces |
| 3 | Algorithm Analysis | Big-Oh notation, asymptotic analysis, seven fundamental functions |
| 4 | Recursion | Linear/binary/multiple recursion, design techniques, tail recursion |

### Part II: Core Data Structures
| Chapter | Topic | Key Concepts |
|---------|-------|-------------|
| 5 | Array-Based Sequences | Dynamic arrays, amortization, Python list/tuple/str internals |
| 6 | Stacks, Queues, and Deques | ADTs, array/linked implementations, applications |
| 7 | Linked Lists | Singly/doubly/circular lists, positional list ADT |
| 8 | Trees | General/binary trees, traversals, expression trees, Euler tours |

### Part III: Advanced Structures & Algorithms
| Chapter | Topic | Key Concepts |
|---------|-------|-------------|
| 9 | Priority Queues | Heap data structure, heap-sort, adaptable priority queues |
| 10 | Maps, Hash Tables, Skip Lists | Hashing, collision resolution, sorted maps, skip lists |
| 11 | Search Trees | BSTs, AVL trees, splay trees, (2,4) trees, red-black trees |
| 12 | Sorting and Selection | Merge-sort, quick-sort, bucket/radix sort, selection algorithms |

### Part IV: Applications & Advanced Topics
| Chapter | Topic | Key Concepts |
|---------|-------|-------------|
| 13 | Text Processing | Pattern matching (KMP, Boyer-Moore), tries, compression, LCS |
| 14 | Graph Algorithms | DFS/BFS, topological sort, shortest paths (Dijkstra), MST (Prim/Kruskal) |
| 15 | Memory Management & B-Trees | Garbage collection, caching, external memory, B-trees |

### Appendices
- **A**: Character Strings in Python
- **B**: Useful Mathematical Facts

---

## 🗂️ Repository Structure

```
├── README.md                 # This file
├── LICENSE                   # Educational use license
├── requirements.txt          # Python dependencies
├── src/
│   ├── ch01_python_primer/
│   ├── ch02_oop/
│   ├── ch03_algorithm_analysis/
│   ├── ch04_recursion/
│   ├── ch05_array_sequences/
│   ├── ch06_stacks_queues/
│   ├── ch07_linked_lists/
│   ├── ch08_trees/
│   ├── ch09_priority_queues/
│   ├── ch10_maps_hash_tables/
│   ├── ch11_search_trees/
│   ├── ch12_sorting/
│   ├── ch13_text_processing/
│   ├── ch14_graphs/
│   └── ch15_memory_btrees/
├── exercises/                # Solutions to selected exercises
├── projects/                 # Capstone project implementations
├── tests/                    # Unit tests for implementations
└── docs/                     # Additional notes and visualizations
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.1 or later
- Basic familiarity with high-level programming concepts
- High-school level mathematics

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/data-structures-algorithms-python.git
cd data-structures-algorithms-python

# Install dependencies (if any)
pip install -r requirements.txt

# Run tests to verify setup
python -m pytest tests/ -v
```

### Usage Example
```python
# Example: Using the Binary Search implementation from Chapter 4
from src.ch04_recursion.binary_search import binary_search

data = [2, 4, 5, 7, 8, 9, 12, 14, 17, 19, 22, 25, 27, 28, 33, 37]
result = binary_search(data, 22, 0, len(data)-1)
print(f"Found at index: {result}")  # Output: Found at index: 10
```

---

## 🎓 Study Guide

### Recommended Learning Path
1. **Weeks 1-2**: Chapters 1-2 (Python & OOP refresher)
2. **Weeks 3-4**: Chapters 3-4 (Analysis & Recursion fundamentals)
3. **Weeks 5-7**: Chapters 5-8 (Core linear/tree structures)
4. **Weeks 8-10**: Chapters 9-12 (Advanced structures & sorting)
5. **Weeks 11-13**: Chapters 13-15 (Applications & advanced topics)

### Exercise Difficulty Levels
| Level | Description | Recommended For |
|-------|-------------|----------------|
| 🔹 Reinforcement | Direct application of concepts | All learners |
| 🔹🔹 Creativity | Problem-solving & extension | Intermediate |
| 🔹🔹🔹 Projects | Capstone implementations | Advanced |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Contribution Guidelines
- ✅ Follow PEP 8 style guide
- ✅ Include docstrings for all public functions/classes
- ✅ Add unit tests for new implementations
- ✅ Update documentation as needed
- ✅ Reference relevant chapters/exercises

---

## 📄 License

This repository is for **educational purposes only**. 

- The book content is © 2013 John Wiley & Sons, Inc.
- Code implementations in this repository are provided under an MIT License for learning purposes
- Please purchase the official textbook to support the authors: [Wiley](https://www.wiley.com/college/goodrich)

---

## 🔗 Resources

### Official Resources
- [Book Website](https://www.wiley.com/college/goodrich) - Source code, hints, instructor materials
- [Python Documentation](https://docs.python.org/3/) - Language reference
- [Visualgo](https://visualgo.net) - Interactive algorithm visualizations

### Recommended Supplements
- [LeetCode](https://leetcode.com) - Practice problems
- [GeeksforGeeks](https://geeksforgeeks.org) - Algorithm explanations
- [CP-Algorithms](https://cp-algorithms.com) - Advanced algorithm techniques

---

## 🙏 Acknowledgments

- Authors: **Michael T. Goodrich** (UC Irvine), **Roberto Tamassia** (Brown University), **Michael H. Goldwasser** (Saint Louis University)
- Publisher: John Wiley & Sons, Inc.
- Reviewers and contributors from the computer science education community

> *"The design and analysis of efficient data structures has long been recognized as a vital subject in computing."* — Preface

---

*⭐ If you find this repository helpful, please star it and share with fellow learners!*
