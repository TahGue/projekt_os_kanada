# Code Sources and Citations

This document lists all external sources, libraries, code examples, and references used in this project. All sources must be properly cited to avoid plagiarism.

---

## 📚 Primary Dataset

**Dataset**: 120 years of Olympic history: athletes and results  
**Source**: Kaggle  
**URL**: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results  
**Author**: rrius  
**License**: CC0: Public Domain  
**Citation**:
```
Dataset: "120 years of Olympic history: athletes and results"
Source: Kaggle (https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
Author: rrius
License: CC0: Public Domain
```

---

## 📖 Libraries and Documentation

### 1. Pandas
**Library**: pandas  
**Version**: 2.1.4  
**Documentation**: https://pandas.pydata.org/docs/  
**Usage**: Data loading, manipulation, filtering, and aggregation  
**Citation**:
```python
# Pandas library for data manipulation
# Documentation: https://pandas.pydata.org/docs/
# Version: 2.1.4
```

### 2. Plotly Dash
**Library**: dash  
**Version**: 2.14.2  
**Documentation**: https://dash.plotly.com/  
**Usage**: Interactive web dashboard creation  
**Citation**:
```python
# Plotly Dash for interactive web dashboards
# Documentation: https://dash.plotly.com/
# Version: 2.14.2
```

### 3. Plotly Express
**Library**: plotly  
**Version**: 5.17.0  
**Documentation**: https://plotly.com/python/plotly-express/  
**Usage**: Data visualization and interactive charts  
**Citation**:
```python
# Plotly Express for data visualization
# Documentation: https://plotly.com/python/plotly-express/
# Version: 5.17.0
```

### 4. NumPy
**Library**: numpy  
**Version**: 1.26.2  
**Documentation**: https://numpy.org/doc/  
**Usage**: Numerical operations and array handling  
**Citation**:
```python
# NumPy for numerical operations
# Documentation: https://numpy.org/doc/
# Version: 1.26.2
```

### 5. Matplotlib
**Library**: matplotlib  
**Version**: 3.8.2  
**Documentation**: https://matplotlib.org/stable/  
**Usage**: Static visualizations in EDA notebook  
**Citation**:
```python
# Matplotlib for static visualizations
# Documentation: https://matplotlib.org/stable/
# Version: 3.8.2
```

### 6. Seaborn
**Library**: seaborn  
**Version**: 0.13.0  
**Documentation**: https://seaborn.pydata.org/  
**Usage**: Statistical visualizations and styling  
**Citation**:
```python
# Seaborn for statistical visualizations
# Documentation: https://seaborn.pydata.org/
# Version: 0.13.0
```

### 7. Hashlib (Python Standard Library)
**Library**: hashlib  
**Documentation**: https://docs.python.org/3/library/hashlib.html  
**Usage**: SHA-256 hashing for name anonymization  
**Citation**:
```python
# Python standard library hashlib for SHA-256 hashing
# Documentation: https://docs.python.org/3/library/hashlib.html
```

---

## 💻 Code Examples and Tutorials

### 1. SHA-256 Hashing for Data Anonymization
**Source**: Python hashlib documentation and common GDPR practices  
**URL**: https://docs.python.org/3/library/hashlib.html  
**Usage**: Name anonymization in `src/data_loader.py`  
**Citation in code**:
```python
# SHA-256 hashing for GDPR-compliant anonymization
# Reference: Python hashlib documentation
# https://docs.python.org/3/library/hashlib.html
```

### 2. Plotly Dash Callback Pattern
**Source**: Plotly Dash documentation  
**URL**: https://dash.plotly.com/basic-callbacks  
**Usage**: Interactive callbacks in `src/dashboard.py`  
**Citation in code**:
```python
# Dash callback pattern for interactive updates
# Reference: Plotly Dash documentation
# https://dash.plotly.com/basic-callbacks
```

### 3. Pandas Boolean Indexing
**Source**: Pandas documentation  
**URL**: https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing  
**Usage**: Data filtering in `src/data_processor.py`  
**Citation in code**:
```python
# Boolean indexing for efficient data filtering
# Reference: Pandas documentation
# https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing
```

### 4. Plotly Express Color Palettes
**Source**: Plotly Express documentation  
**URL**: https://plotly.com/python/builtin-colorscales/  
**Usage**: Color scales (Viridis, Plasma) in `src/dashboard.py`  
**Citation in code**:
```python
# Color-blind friendly palettes (Viridis, Plasma)
# Reference: Plotly Express built-in colorscales
# https://plotly.com/python/builtin-colorscales/
```

### 5. Olympics Data Analysis Tutorial
**Source**: GeeksforGeeks  
**URL**: https://www.geeksforgeeks.org/olympics-data-analysis-using-python/  
**Usage**: General approach to Olympic data analysis (conceptual reference)  
**Citation**:
```
General approach to Olympic data analysis inspired by:
GeeksforGeeks - Olympics Data Analysis Using Python
https://www.geeksforgeeks.org/olympics-data-analysis-using-python/
```

---

## 🎨 Design and Visualization References

### 1. Color-Blind Friendly Palettes
**Source**: Scientific visualization best practices  
**Reference**:
- Viridis color scale: https://matplotlib.org/stable/tutorials/colors/colormaps.html
- Plasma color scale: https://matplotlib.org/stable/tutorials/colors/colormaps.html
**Usage**: Dashboard color schemes  
**Citation in code**:
```python
# Color-blind friendly palettes (Viridis, Plasma)
# Reference: Matplotlib colormap documentation
# https://matplotlib.org/stable/tutorials/colors/colormaps.html
```

### 2. Dashboard Design Principles
**Source**: Plotly Dash documentation and best practices  
**URL**: https://dash.plotly.com/  
**Usage**: Dashboard layout and structure  
**Citation**:
```
Dashboard design principles based on:
Plotly Dash documentation and best practices
https://dash.plotly.com/
```

---

## 📝 Academic and Research References

### 1. GDPR Compliance for Data Anonymization
**Source**: General GDPR principles and Python hashlib documentation  
**Reference**:
- GDPR: https://gdpr.eu/
- Python hashlib: https://docs.python.org/3/library/hashlib.html
**Usage**: Name anonymization approach  
**Citation**:
```
GDPR-compliant anonymization approach based on:
- GDPR principles (https://gdpr.eu/)
- Python hashlib SHA-256 implementation
```

### 2. Object-Oriented Programming Principles
**Source**: Python OOP best practices  
**Reference**: Python documentation and general OOP principles  
**Usage**: OlympicAnalyzer class design  
**Citation**:
```
OOP design principles based on:
- Python documentation (https://docs.python.org/3/)
- General object-oriented programming best practices
```

---

## 🔗 Additional Resources Consulted

1. **Kaggle Dataset Discussion**:  
   - https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results/discussion

2. **Plotly Dash Community Examples**:  
   - https://dash.plotly.com/gallery

3. **Pandas User Guide**:  
   - https://pandas.pydata.org/docs/user_guide/

4. **Python Best Practices**:  
   - PEP 8 Style Guide: https://pep8.org/

---

## 📋 How to Cite in Code

Add comments next to code that uses external sources:

```python
# Example 1: Library usage
import pandas as pd  # Pandas 2.1.4 - https://pandas.pydata.org/docs/

# Example 2: Code pattern from documentation
@app.callback(...)  # Dash callback pattern - https://dash.plotly.com/basic-callbacks

# Example 3: Algorithm or approach
df['Name_hash'] = df['Name'].apply(
    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
)  # SHA-256 hashing for GDPR anonymization - Python hashlib documentation

# Example 4: Color palette
color_continuous_scale='viridis'  # Color-blind friendly palette - Plotly Express
```

---

## ✅ Citation Checklist

- [x] Primary dataset (Kaggle) cited
- [x] All libraries documented with versions
- [x] Code patterns from documentation cited
- [x] Design principles referenced
- [x] Tutorials and examples acknowledged
- [x] Comments added in code where appropriate

---

## 📝 Notes

1. **Standard Libraries**: Python standard library modules (hashlib, os) do not require citation but are noted for completeness.

2. **Original Code**: All code in this project is original implementation, though patterns and approaches may be inspired by documentation and best practices.

3. **Dataset**: The dataset is publicly available under CC0: Public Domain license, allowing free use.

4. **Libraries**: All libraries used are open-source and properly licensed for academic use.

---

**Last Updated**: 2024  
**Project**: Olympic Games Data Analysis - Kanada  
**Course**: Projekt_OS
