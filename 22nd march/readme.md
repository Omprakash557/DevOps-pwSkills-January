# readme

# Python Fundamentals – Lecture Notes

A beginner-friendly guide covering Python's **OS module**, **File Handling**, **Math library**, **Virtual Environments**, and **NumPy basics**.

---

## 1. OS Module

The `os` module provides functions to interact with the operating system — listing files, creating/deleting folders, and working with paths.

```python
import os

# Get current working directory
cwd = os.getcwd()
print(cwd)
```

### Listing Files

```python
files = os.listdir()
print("Files in current directory:", files)
```

### Creating Folders

```python
# Single folder
os.mkdir("test_folder1")

# Nested folders
os.makedirs("test/test123")
```

### Removing Folders

```python
os.rmdir("test_folder")
os.removedirs("test/test123")
```

### Path Types

| Type | Description | Example |
|------|-------------|---------|
| **Absolute** | Full path from root | `/home/user/project/file.txt` |
| **Relative** | Path from current location | `./data/file.txt` |

---

## 2. File Handling

Files are opened with a **mode** that defines what you can do with them:

| Mode | Description |
|------|-------------|
| `w` | Write (creates or overwrites) |
| `r` | Read (view contents) |
| `x` | Execute |
| `a` | Append (add to end) |

### Creating and Writing to a File

```python
with open("sample.txt", "w") as f:
    f.write("Hello Students")
    f.writelines(" ")
    f.writelines("Hello Students")
f.close()
```

### Writing Without `with` Block

```python
f = open("sample123.txt", "w")
f.write("Hello")
f.close()
```

### Append vs Add

- **Append** → adds content to the **end** of the file
- **Add** → inserts content at a specific **offset/position**

### Common End-of-File Markers

| Format | EOF Indicator |
|--------|---------------|
| `.txt` | New line |
| `.html` | `</html>` |
| `.xml` | `</xml>` |
| `.yaml` | New line |

---

## 3. Math Library

The `math` module provides mathematical functions and constants.

```python
import math as m

print(m.pi)          # 3.141592653589793

print(m.ceil(2.4))   # 3   → rounds UP
print(m.floor(2.4))  # 2   → rounds DOWN

print(m.fabs(-9.11)) # 9.11 → absolute value

print(m.sqrt(25))    # 5.0
print(m.pow(2, 3))   # 8.0  → 2^3
```

---

## 4. Practice Tasks

### Task 1 – File & Folder Operations

> Write a Python script that:
> 1. Creates a folder named `student_data`
> 2. Inside it, creates a file `info.txt`
> 3. Writes your name into the file
> 4. Prints all files inside the folder
> 5. Deletes the file

### Task 2 – Math Operations

> Write a Python program that:
> 1. Takes a number from the user
> 2. Prints its **square root**
> 3. Prints its **factorial**
> 4. Prints its **log value**
> 5. Converts **45°** to radians and prints the **sin** value

---

## 5. Virtual Environments

Virtual environments isolate project dependencies so packages don't conflict across projects.

### Windows (VS Code Terminal)

```bash
python -m venv myenv
myenv\Scripts\activate
pip list
```

### Mac / Linux

```bash
python -m venv myenv
source myenv/bin/activate
pip list
```

> `pip list` shows all installed packages inside the active environment.

---

## 6. NumPy Basics

[NumPy](https://numpy.org/) is a library for numerical computing with powerful array operations.

### Installation

```bash
pip install numpy
```

### Example

```python
import numpy as np

# Create an array of ones
arr_ones = np.ones((1, 4))
print(f"Array of ones: {arr_ones}")
# Output: [[1. 1. 1. 1.]]
```

---

## Quick Reference

| Topic | Key Import | Purpose |
|-------|-----------|---------|
| OS operations | `import os` | File system interaction |
| Math functions | `import math` | Mathematical computations |
| NumPy arrays | `import numpy as np` | Numerical computing |

---

> **Note:** These are classroom lecture notes. Practice both tasks to solidify your understanding!
