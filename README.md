# DumFish_dev
# Python Chess Engine (with Cython Acceleration)

This is a simple chess engine written in **pure Python**, with optional speedup using **Cython**.  
It supports the **UCI (Universal Chess Interface)** protocol so it can be connected to GUIs like **CuteChess** or **Arena**.  

---

## 🚀 Features
- Basic evaluation (material, piece-square tables, king safety).
- Alpha-beta search.
- Configurable search depth.
- UCI support.
- Optional **Cython compilation** for performance boost (~2-5x faster).

---

## 📦 Requirements
- Python 3.8+  
- [python-chess](https://python-chess.readthedocs.io/)  
- Cython  

Install with:
```bash
pip install python-chess cython
