
## Efficient Spatial Queries with R-Trees: Nearest Neighbor & Skyline Search

---

## 🖥️ Program Requirements

### ✅ Environment

- **OS:** macOS Ventura (or compatible)
- **CPU:** Apple M3 (ARM-based)
- **Memory:** 16 GB
- **Python:** 3.11.0  
- **Packages Used:**
  - Standard: `math`, `os`, `time`
  - Custom: `Create_Rtree`

---

## 📂 Directory & File Structure

```

📁 project-root/
├── Task1.py                  # Nearest Neighbor Search
├── Task2.py                  # Skyline Search
├── create\_rtree.py           # Core R-Tree implementation
├── create\_rtree\_task2.py     # R-Tree for Task 2
├── parking\_dataset.txt       # Input for Task 1
├── city2.txt                 # Input for Task 2
├── sequential\_output.txt
├── best\_first\_output.txt
├── divide\_and\_conquer\_output.txt

````

---

## 🚀 Execution Instructions

### Task 1: Nearest Neighbor

```bash
python Task1.py
````

### Task 2: Skyline Search

```bash
python Task2.py
```

Ensure all scripts and dataset files are in the same directory.

---

## 🧠 Program Overview

### 🔎 Task 1 – Nearest Neighbor Search

| Function/Class         | Description                            |
| ---------------------- | -------------------------------------- |
| `Main()`               | Loads datasets and runs all algorithms |
| `sequential_search()`  | Brute-force distance calculation       |
| `best_first_search()`  | R-tree + Best-First search             |
| `divide_and_conquer()` | R-tree on subsets                      |
| `tree_traversal()`     | Recursive MBR-based navigation         |
| `euclidean_distance()` | Distance function                      |

### 🧭 Task 2 – Skyline Search

| Function/Class              | Description                       |
| --------------------------- | --------------------------------- |
| `Main()`                    | Loads home listing data           |
| `sequential_scan_skyline()` | Brute-force skyline points        |
| `bbs_skyline_search()`      | BBS with R-tree                   |
| `bbs_divide_and_conquer()`  | Skyline search with dataset split |
| `dominate()`                | Dominance checking                |

---

## 🌲 R-Tree Functions (Common)

| Function            | Description                   |
| ------------------- | ----------------------------- |
| `Insert()`          | Adds data to R-tree           |
| `choose_subtree()`  | Selects optimal subtree       |
| `handle_overflow()` | Manages node splits           |
| `perimeter()`       | Calculates bounding perimeter |
| `update_mbr()`      | Expands MBRs dynamically      |

---

## 📊 Performance Summary

### Task 1 – Nearest Neighbor

| Algorithm          | Total Time (s) | Avg. Time per Query (s) |
| ------------------ | -------------- | ----------------------- |
| Sequential Search  | 13.98          | 0.0699                  |
| Best-First Search  | 0.0263         | 0.00013                 |
| Divide-and-Conquer | 0.0231         | 0.00012                 |

### Task 2 – Skyline Search

| Algorithm          | Total Time (s) |
| ------------------ | -------------- |
| Sequential Skyline | 3.72           |
| BBS                | 0.0128         |
| Divide-and-Conquer | 29.87          |

---

## 📈 Key Insights

* **Best-First Search** is fast and efficient for Task 1 due to R-tree pruning.
* **Divide-and-Conquer** excels in Task 1 by minimizing the search area.
* **BBS (Branch-and-Bound Skyline)** outperforms all others in Task 2.
* Tree-based indexing greatly outpaces sequential methods in both speed and scalability.

---

## ⚠️ Limitations

* High memory usage during tree construction.
* Dominance checking can become expensive for large datasets.

---

## 🚀 Future Improvements

* Implement **parallel R-tree construction** for faster Divide-and-Conquer.
* Explore **Quadtrees or kd-trees** for optimized skyline queries.

---

## 📌 Conclusion

> This project highlights how spatial data structures like **R-trees**, combined with **Best-First** and **Branch-and-Bound** algorithms, significantly improve performance in nearest neighbor and skyline search operations. Efficient for real-world spatial applications like navigation systems and real estate filtering.

---

### 🧾 License

MIT License (Add your preferred license here)

---
