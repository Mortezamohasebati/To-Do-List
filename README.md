<div align="center">

<br/>

# ✅ To-Do List — Advanced Task Manager

<br/>

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/PyQt5-GUI_Framework-41CD52?style=for-the-badge&logo=qt&logoColor=white"/>
<img src="https://img.shields.io/badge/Calendar-Jalali_|_Shamsi-F59E0B?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Theme-Dark_%26_Light-7C3AED?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Storage-JSON-10B981?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-EF4444?style=for-the-badge"/>

<br/><br/>

**A sleek Persian-first desktop task manager — 1,085 lines of pure PyQt5 with Jalali calendar, live dark/light theme, and zero database required.**

<br/>

🇮🇷 [فارسی / Persian README](./README.fa.md)

</div>

---

## 🖥️ What Is This?

A feature-rich **Persian task manager desktop app** built entirely in Python. No web browser, no Electron, no database — just pure Python, PyQt5, and a single `tasks.json` file. It speaks Persian natively, understands the Shamsi (Jalali) calendar, and looks great in both dark and light modes.

The codebase is a single well-structured `main.py` — 1,085 lines with proper data models, PyQt5 signal/slot architecture, custom reusable widgets, and a full two-palette theme engine.

---

## ✨ Features

| | Feature | Details |
|:---:|---|---|
| 🌙 | **Dark / Light Theme** | One-click full theme switch — every widget, card, and dialog repaints instantly |
| 📅 | **Jalali (Shamsi) Calendar** | Native Persian date/time picker with spinboxes for year · month · day · hour · minute |
| 🏷️ | **4 Smart Categories** | شخصی (Personal) · فوری (Urgent) · کار (Work) · ایده (Idea) — each fully color-coded |
| 🎨 | **Custom Card Colors** | Per-task color picker via Qt's native `QColorDialog` with auto-contrast text |
| ⚡ | **Quick Add Sidebar** | Type a title and click a category button — task added instantly |
| ✨ | **Advanced Add Dialog** | Full modal: title, description, Shamsi deadline, category, and card color |
| 📊 | **Live Stats Panel** | Real-time counters for Total · Done · Pending · Urgent tasks |
| 📈 | **Gradient Progress Bar** | Visual completion percentage with purple → green gradient |
| 🔍 | **Real-time Search** | Instant filtering across all tasks as you type |
| ⇅ | **Sort Tasks** | Sort by due date or category with a single click |
| 💾 | **JSON Persistence** | All data stored in `tasks.json` — no setup, no migrations, no server |
| 🖥️ | **Windows Launcher** | `RUN_TO.bat` for double-click launch on Windows |

---

## 🏗️ Architecture

```
📦 To-Do-List/
 ├── 🧠 main.py        1,085 lines · PyQt5 + jdatetime
 │    ├── THEMES {}         Dark & light color palettes
 │    ├── Task              Data model (to_dict / from_dict)
 │    ├── ShamsiDatePicker  Custom Jalali date/time widget
 │    ├── TaskWidget        Individual task card (QFrame + signals)
 │    ├── TaskDialog        Add / Edit modal dialog
 │    ├── StatsWidget       Live 4-counter stats panel
 │    ├── SidebarWidget     Left navigation panel
 │    └── TodoApp           QMainWindow — orchestrates everything
 ├── 💾 tasks.json     Auto-generated local storage
 └── 🚀 RUN_TO.bat     Windows one-click launcher
```

---

## 🚀 Quick Start

### 1 — Install

```bash
pip install PyQt5 jdatetime
```

### 2 — Run

```bash
# Windows — double-click
RUN_TO.bat

# Any OS — terminal
python main.py
```

> ✅ No config, no `.env`, no database. Just run.

---

## 🎮 Usage Guide

| Action | How to do it |
|---|---|
| ➕ Quick add | Type title in sidebar → click 👤 / 🔥 / 💼 category button |
| ➕ Advanced add | Click **✨ افزودن پیشرفته** → fill the dialog |
| ✅ Mark complete | Click the circle on the left of any task card |
| ✏️ Edit task | Click **✏️** on any card |
| 🗑️ Delete task | Click **🗑️** on any card |
| 🔍 Search | Type in the search box — filters live |
| ⇅ Sort | Click **📅 تاریخ** or **🏷️ دسته** in the sidebar |
| 🌙 Switch theme | Click **☀️ / 🌙** in the sidebar header |
| 💾 Save | Click **💾 ذخیره همه** — also auto-saves on every change |

---

## 🏷️ Task Categories

| Category | Persian | Icon | Color |
|---|---|:---:|---|
| Personal | شخصی | 👤 | 🟢 Green |
| Urgent | فوری | 🔥 | 🔴 Red |
| Work | کار | 💼 | 🔵 Blue |
| Idea | ایده | 💡 | 🟠 Orange |

---

## 🛠️ Tech Stack

| Tool | Version | Role |
|---|---|---|
| **Python** | 3.8+ | Core language |
| **PyQt5** | latest | Desktop GUI — widgets, signals, layouts |
| **jdatetime** | latest | Jalali ↔ Gregorian conversion |
| **json** | stdlib | Lightweight local storage |

---

## 🤝 Contributing

```bash
# Fork → Clone
git clone https://github.com/Mortezamohasebati/To-Do-List.git
cd To-Do-List

# Create a feature branch
git checkout -b feature/your-feature

# Commit & push
git commit -m "feat: describe your change"
git push origin feature/your-feature

# Open a Pull Request on GitHub
```

All PRs and issues are welcome!

---

## 📄 License

[MIT](LICENSE) — use it, fork it, build on it. Just give credit. 🙏

---

<div align="center">

Made with ❤️ by **[Morteza Mohasebati](https://github.com/Mortezamohasebati)**

<br/>

⭐ If this helped you, drop a star — it means a lot!

<br/>

<img src="https://img.shields.io/github/stars/Mortezamohasebati/To-Do-List?style=social"/> &nbsp;
<img src="https://img.shields.io/github/forks/Mortezamohasebati/To-Do-List?style=social"/>

</div>
