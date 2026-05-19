import sys
import json
import jdatetime
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QDialog, QLabel, QCheckBox, QColorDialog,
    QScrollArea, QTextEdit, QFrame, QSizePolicy, QProgressBar,
    QComboBox, QMessageBox, QSpinBox, QGridLayout
)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QColor, QFont, QCursor

TASKS_FILE = "tasks.json"

# ══════════════════════════════════════════════════════════════════════════════
#  تم‌ها
# ══════════════════════════════════════════════════════════════════════════════
THEMES = {
    "dark": {
        "sidebar_bg":       "#1E1B2E",
        "sidebar_hover":    "#2D2647",
        "sidebar_sub":      "#9CA3AF",
        "sidebar_input_bg": "#2D2647",
        "sidebar_input_br": "#3D3659",
        "main_bg":          "#13111C",
        "card_bg":          "#1E1B2E",
        "card_border":      "#2D2647",
        "card_hover_br":    "#7C3AED",
        "header_from":      "#4C1D95",
        "header_to":        "#312E81",
        "text_primary":     "#F3F4F6",
        "text_secondary":   "#9CA3AF",
        "text_done":        "#4B5563",
        "accent":           "#7C3AED",
        "accent_light":     "#2D1B69",
        "accent_hover":     "#6D28D9",
        "green":            "#10B981",
        "green_light":      "#064E3B",
        "red":              "#EF4444",
        "red_light":        "#7F1D1D",
        "orange":           "#F59E0B",
        "orange_light":     "#78350F",
        "blue":             "#3B82F6",
        "blue_light":       "#1E3A5F",
        "progress_bg":      "#2D2647",
        "scroll_bg":        "#2D2647",
        "dialog_bg":        "#1E1B2E",
        "input_bg":         "#13111C",
        "input_br":         "#3D3659",
        "sep":              "#2D2647",
        "stat_alpha":       "33",
        "toggle_icon":      "☀️",
        "toggle_tip":       "حالت روشن",
    },
    "light": {
        "sidebar_bg":       "#1E1B2E",
        "sidebar_hover":    "#2D2647",
        "sidebar_sub":      "#9CA3AF",
        "sidebar_input_bg": "#2D2647",
        "sidebar_input_br": "#3D3659",
        "main_bg":          "#F5F4FA",
        "card_bg":          "#FFFFFF",
        "card_border":      "#E8E4F4",
        "card_hover_br":    "#7C3AED",
        "header_from":      "#7C3AED",
        "header_to":        "#4F46E5",
        "text_primary":     "#1A1A2E",
        "text_secondary":   "#6B7280",
        "text_done":        "#9CA3AF",
        "accent":           "#7C3AED",
        "accent_light":     "#EDE9FE",
        "accent_hover":     "#6D28D9",
        "green":            "#10B981",
        "green_light":      "#D1FAE5",
        "red":              "#EF4444",
        "red_light":        "#FEE2E2",
        "orange":           "#F59E0B",
        "orange_light":     "#FEF3C7",
        "blue":             "#3B82F6",
        "blue_light":       "#DBEAFE",
        "progress_bg":      "#E8E4F4",
        "scroll_bg":        "#E8E4F4",
        "dialog_bg":        "#F5F4FA",
        "input_bg":         "#FFFFFF",
        "input_br":         "#E8E4F4",
        "sep":              "#E8E4F4",
        "stat_alpha":       "22",
        "toggle_icon":      "🌙",
        "toggle_tip":       "حالت تاریک",
    },
}

CAT_COLORS = {
    "شخصی": ("green", "green_light"),
    "فوری": ("red",   "red_light"),
    "کار":  ("blue",  "blue_light"),
    "ایده": ("orange","orange_light"),
}


def cat_colors(category, T):
    k = CAT_COLORS.get(category, ("text_secondary", "card_border"))
    return T[k[0]], T[k[1]]


# ══════════════════════════════════════════════════════════════════════════════
#  ابزارهای تاریخ شمسی
# ══════════════════════════════════════════════════════════════════════════════
MONTHS_FA = [
    "فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور",
    "مهر","آبان","آذر","دی","بهمن","اسفند",
]


def qdatetime_to_jalali(qdt):
    if not qdt or qdt.isNull():
        return jdatetime.datetime.now()
    py = qdt.toPyDateTime()
    return jdatetime.datetime.fromgregorian(datetime=py)


def jalali_to_qdatetime(jdt):
    gr = jdt.togregorian()
    return QDateTime(QDate(gr.year, gr.month, gr.day),
                     QTime(gr.hour, gr.minute))


def format_shamsi(qdt):
    if not qdt or qdt.isNull():
        return ""
    j = qdatetime_to_jalali(qdt)
    return f"{j.year}/{j.month:02d}/{j.day:02d}  {j.hour:02d}:{j.minute:02d}"


def today_shamsi_str():
    j = jdatetime.date.today()
    return f"{j.day} {MONTHS_FA[j.month - 1]} {j.year}"


# ══════════════════════════════════════════════════════════════════════════════
#  مدل
# ══════════════════════════════════════════════════════════════════════════════
class Task:
    def __init__(self, id=0, title="", description="", due_date=None,
                 category="None", color=None, is_done=False):
        self.id          = id
        self.title       = title
        self.description = description
        self.due_date    = due_date if due_date else QDateTime()
        self.category    = category
        self.color       = color if color else QColor("#FFFFFF")
        self.is_done     = is_done

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.toString(Qt.ISODate) if not self.due_date.isNull() else None,
            "category": self.category,
            "color": self.color.name(),
            "is_done": self.is_done,
        }

    @staticmethod
    def from_dict(d):
        return Task(
            id=d.get("id", 0),
            title=d.get("title", ""),
            description=d.get("description", ""),
            due_date=QDateTime.fromString(d["due_date"], Qt.ISODate) if d.get("due_date") else QDateTime(),
            category=d.get("category", "None"),
            color=QColor(d.get("color", "#FFFFFF")),
            is_done=d.get("is_done", False),
        )


# ══════════════════════════════════════════════════════════════════════════════
#  انتخاب‌گر تاریخ شمسی
# ══════════════════════════════════════════════════════════════════════════════
class ShamsiDatePicker(QWidget):
    def __init__(self, T, parent=None):
        super().__init__(parent)
        self.T = T
        now = jdatetime.datetime.now()
        lay = QGridLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        lbl_s = f"color:{T['text_secondary']}; font-size:8pt; background:transparent;"
        spin_s = f"""
            QSpinBox {{
                background:{T['input_bg']}; color:{T['text_primary']};
                border:1.5px solid {T['input_br']}; border-radius:8px;
                padding:4px 6px; font-size:10pt; font-family:'Segoe UI';
            }}
            QSpinBox:focus {{ border:1.5px solid {T['accent']}; }}
            QSpinBox::up-button, QSpinBox::down-button {{ width:18px; }}
        """

        def lbl(text):
            l = QLabel(text)
            l.setStyleSheet(lbl_s)
            l.setAlignment(Qt.AlignCenter)
            return l

        def spin(mn, mx, val, w=80):
            s = QSpinBox()
            s.setRange(mn, mx)
            s.setValue(val)
            s.setFixedWidth(w)
            s.setFixedHeight(36)
            s.setStyleSheet(spin_s)
            s.setAlignment(Qt.AlignCenter)
            return s

        for col, text in enumerate(["سال","ماه","روز","ساعت","دقیقه"]):
            lay.addWidget(lbl(text), 0, col)

        self.year_sp  = spin(1300, 1500, now.year,   90)
        self.month_sp = spin(1,    12,   now.month,  68)
        self.day_sp   = spin(1,    31,   now.day,    68)
        self.hour_sp  = spin(0,    23,   now.hour,   68)
        self.min_sp   = spin(0,    59,   now.minute, 68)

        for col, sp in enumerate([self.year_sp, self.month_sp,
                                   self.day_sp, self.hour_sp, self.min_sp]):
            lay.addWidget(sp, 1, col)

    def get_qdatetime(self):
        try:
            jdt = jdatetime.datetime(
                self.year_sp.value(), self.month_sp.value(), self.day_sp.value(),
                self.hour_sp.value(), self.min_sp.value()
            )
            return jalali_to_qdatetime(jdt)
        except Exception:
            return QDateTime.currentDateTime()

    def set_qdatetime(self, qdt):
        if not qdt or qdt.isNull():
            return
        j = qdatetime_to_jalali(qdt)
        self.year_sp.setValue(j.year)
        self.month_sp.setValue(j.month)
        self.day_sp.setValue(j.day)
        self.hour_sp.setValue(j.hour)
        self.min_sp.setValue(j.minute)


# ══════════════════════════════════════════════════════════════════════════════
#  کارت وظیفه
# ══════════════════════════════════════════════════════════════════════════════
class TaskWidget(QFrame):
    edit_task   = pyqtSignal(int)
    delete_task = pyqtSignal(int)
    toggle_done = pyqtSignal(int)

    def __init__(self, task, T, parent=None):
        super().__init__(parent)
        self.task = task
        self.T    = T
        self.setObjectName("taskCard")
        self._build()

    def _build(self):
        T = self.T
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(f"""
            QFrame#taskCard {{
                background:{T['card_bg']};
                border:1px solid {T['card_border']};
                border-radius:14px;
            }}
            QFrame#taskCard:hover {{
                border:1px solid {T['card_hover_br']};
            }}
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        fg, bg = cat_colors(self.task.category, T)

        # نوار رنگی بالای کارت
        bar = QFrame()
        bar.setFixedHeight(4)
        bar.setStyleSheet(f"background:{fg}; border-radius:0px;")
        outer.addWidget(bar)

        # محتوا
        body = QWidget()
        body.setStyleSheet("background:transparent;")
        row = QHBoxLayout(body)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(12)

        # چک‌باکس
        self.chk = QCheckBox()
        self.chk.setChecked(self.task.is_done)
        self.chk.setFixedSize(22, 22)
        self.chk.setStyleSheet(f"""
            QCheckBox::indicator {{
                width:20px; height:20px; border-radius:10px;
                border:2px solid {fg}; background:{T['card_bg']};
            }}
            QCheckBox::indicator:checked {{
                background:{fg}; border:2px solid {fg};
            }}
        """)
        self.chk.stateChanged.connect(lambda s: self.toggle_done.emit(self.task.id))
        row.addWidget(self.chk, 0, Qt.AlignTop)

        # اطلاعات
        info = QVBoxLayout()
        info.setSpacing(4)
        info.setContentsMargins(0, 0, 0, 0)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)
        title_row.setContentsMargins(0, 0, 0, 0)

        self.title_lbl = QLabel(self.task.title)
        self.title_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.title_lbl.setLayoutDirection(Qt.RightToLeft)
        title_row.addWidget(self.title_lbl, 1)

        if self.task.category not in ("None", ""):
            badge = QLabel(f"  {self.task.category}  ")
            badge.setFont(QFont("Segoe UI", 8, QFont.Bold))
            badge.setStyleSheet(f"background:{bg}; color:{fg}; border-radius:8px; padding:2px 6px;")
            badge.setFixedHeight(20)
            title_row.addWidget(badge)

        info.addLayout(title_row)

        if self.task.description:
            dl = QLabel(self.task.description)
            dl.setWordWrap(True)
            dl.setFont(QFont("Segoe UI", 9))
            dl.setLayoutDirection(Qt.RightToLeft)
            dl.setStyleSheet(f"color:{T['text_secondary']}; background:transparent;")
            info.addWidget(dl)

        if not self.task.due_date.isNull():
            dr = QHBoxLayout()
            dr.setSpacing(4)
            di = QLabel("📅")
            di.setFont(QFont("Segoe UI", 8))
            di.setStyleSheet("background:transparent;")
            dv = QLabel(format_shamsi(self.task.due_date))
            dv.setFont(QFont("Segoe UI", 8))
            dv.setStyleSheet(f"color:{T['text_secondary']}; background:transparent;")
            dr.addStretch()
            dr.addWidget(dv)
            dr.addWidget(di)
            info.addLayout(dr)

        row.addLayout(info, 1)

        # دکمه‌های عملیات
        bc = QVBoxLayout()
        bc.setSpacing(6)
        bc.setContentsMargins(0, 0, 0, 0)

        eb = self._icon_btn("✏️", T["accent"], T["accent_light"], "ویرایش")
        db = self._icon_btn("🗑️", T["red"],   T["red_light"],    "حذف")
        eb.clicked.connect(lambda: self.edit_task.emit(self.task.id))
        db.clicked.connect(lambda: self.delete_task.emit(self.task.id))
        bc.addWidget(eb)
        bc.addWidget(db)
        row.addLayout(bc)

        outer.addWidget(body)
        self._update_done()

    def _icon_btn(self, icon, fg, bg, tip):
        b = QPushButton(icon)
        b.setFixedSize(34, 34)
        b.setToolTip(tip)
        b.setCursor(QCursor(Qt.PointingHandCursor))
        b.setStyleSheet(f"""
            QPushButton {{ background:{bg}; border:none; border-radius:8px; font-size:14px; }}
            QPushButton:hover {{ background:{fg}; }}
        """)
        return b

    def _update_done(self):
        T = self.T
        if self.task.is_done:
            self.title_lbl.setStyleSheet(
                f"text-decoration:line-through; color:{T['text_done']}; background:transparent;")
        else:
            self.title_lbl.setStyleSheet(
                f"color:{T['text_primary']}; background:transparent;")


# ══════════════════════════════════════════════════════════════════════════════
#  دیالوگ افزودن / ویرایش
# ══════════════════════════════════════════════════════════════════════════════
class TaskDialog(QDialog):
    save_task = pyqtSignal(object)

    def __init__(self, T, task=None, parent=None):
        super().__init__(parent)
        self.T    = T
        self.task = task
        self.current_color = task.color if task else QColor(T["card_bg"])
        self.setWindowTitle("وظیفه جدید" if not task else "ویرایش وظیفه")
        self.setFixedSize(590, 520)
        self.setLayoutDirection(Qt.RightToLeft)
        T = self.T
        self.setStyleSheet(f"""
            QDialog {{ background:{T['dialog_bg']}; }}
            QLabel  {{ color:{T['text_primary']}; font-family:'Segoe UI'; background:transparent; }}
            QLineEdit, QTextEdit, QComboBox {{
                background:{T['input_bg']}; color:{T['text_primary']};
                border:1.5px solid {T['input_br']}; border-radius:10px;
                padding:8px 12px; font-size:10pt; font-family:'Segoe UI';
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border:1.5px solid {T['accent']};
            }}
            QComboBox::drop-down {{ border:none; width:28px; }}
            QComboBox QAbstractItemView {{
                background:{T['input_bg']}; color:{T['text_primary']};
                border:1px solid {T['input_br']}; border-radius:8px;
                selection-background-color:{T['accent_light']};
            }}
        """)
        self._build()

    def _build(self):
        T = self.T
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)

        # هدر
        ico = "✨" if not self.task else "✏️"
        h = QLabel(f"{ico}  {'افزودن وظیفه جدید' if not self.task else 'ویرایش وظیفه'}")
        h.setFont(QFont("Segoe UI", 13, QFont.Bold))
        h.setStyleSheet(f"color:{T['accent']}; background:transparent;")
        lay.addWidget(h)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color:{T['sep']};")
        lay.addWidget(sep)

        # عنوان
        self.title_in = QLineEdit()
        self.title_in.setPlaceholderText("عنوان وظیفه را بنویسید...")
        self.title_in.setFixedHeight(42)
        self.title_in.setFont(QFont("Segoe UI", 11))
        lay.addWidget(self.title_in)

        # توضیحات
        self.desc_in = QTextEdit()
        self.desc_in.setPlaceholderText("توضیحات (اختیاری)...")
        self.desc_in.setFixedHeight(76)
        self.desc_in.setFont(QFont("Segoe UI", 10))
        lay.addWidget(self.desc_in)

        # تاریخ شمسی
        dl = QLabel("📅  تاریخ سررسید (شمسی):")
        dl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        dl.setStyleSheet(f"color:{T['text_secondary']}; background:transparent;")
        lay.addWidget(dl)

        self.date_picker = ShamsiDatePicker(T)
        lay.addWidget(self.date_picker)

        # دسته‌بندی + رنگ
        cr = QHBoxLayout()
        cr.setSpacing(8)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["None", "شخصی", "فوری", "کار", "ایده"])
        self.cat_combo.setFixedHeight(42)
        self.cat_combo.setFont(QFont("Segoe UI", 10))
        cr.addWidget(self.cat_combo, 1)

        self.color_btn = QPushButton("🎨  رنگ کارت")
        self.color_btn.setFixedHeight(42)
        self.color_btn.setFixedWidth(130)
        self.color_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.color_btn.clicked.connect(self._pick_color)
        self._refresh_color_btn()
        cr.addWidget(self.color_btn)
        lay.addLayout(cr)

        lay.addStretch(1)

        # دکمه‌ها
        br = QHBoxLayout()
        br.setSpacing(10)

        cancel = QPushButton("لغو")
        cancel.setFixedHeight(44)
        cancel.setCursor(QCursor(Qt.PointingHandCursor))
        cancel.clicked.connect(self.reject)
        cancel.setStyleSheet(f"""
            QPushButton {{ background:{T['sep']}; color:{T['text_secondary']};
                border:none; border-radius:10px; font-size:10pt; font-family:'Segoe UI'; }}
            QPushButton:hover {{ background:{T['input_br']}; }}
        """)
        br.addWidget(cancel)

        save = QPushButton("💾  ذخیره")
        save.setFixedHeight(44)
        save.setCursor(QCursor(Qt.PointingHandCursor))
        save.clicked.connect(self._save)
        save.setStyleSheet(f"""
            QPushButton {{ background:{T['accent']}; color:white;
                border:none; border-radius:10px; font-size:10pt;
                font-family:'Segoe UI'; font-weight:bold; }}
            QPushButton:hover {{ background:{T['accent_hover']}; }}
        """)
        br.addWidget(save)
        lay.addLayout(br)

        if self.task:
            self._load()

    def _load(self):
        self.title_in.setText(self.task.title)
        self.desc_in.setText(self.task.description)
        self.date_picker.set_qdatetime(self.task.due_date)
        idx = self.cat_combo.findText(self.task.category)
        if idx >= 0:
            self.cat_combo.setCurrentIndex(idx)
        self.current_color = self.task.color
        self._refresh_color_btn()

    def _pick_color(self):
        c = QColorDialog.getColor(self.current_color, self, "انتخاب رنگ کارت")
        if c.isValid():
            self.current_color = c
            self._refresh_color_btn()

    def _refresh_color_btn(self):
        T = self.T
        r, g, b = self.current_color.red(), self.current_color.green(), self.current_color.blue()
        tc = "#111" if (0.299*r + 0.587*g + 0.114*b) > 140 else "#fff"
        self.color_btn.setStyleSheet(f"""
            QPushButton {{ background:{self.current_color.name()}; color:{tc};
                border:1.5px solid {T['input_br']}; border-radius:10px;
                font-size:10pt; font-family:'Segoe UI'; }}
        """)

    def _save(self):
        T = self.T
        title = self.title_in.text().strip()
        if not title:
            QMessageBox.warning(self, "خطا", "عنوان وظیفه نمی‌تواند خالی باشد.")
            return

        cat   = self.cat_combo.currentText()
        qdt   = self.date_picker.get_qdatetime()
        color = self.current_color

        if color.name().lower() == T["card_bg"].lower() and cat in CAT_COLORS:
            fk, bk = CAT_COLORS[cat]
            color = QColor(T[bk])

        if self.task:
            self.task.title       = title
            self.task.description = self.desc_in.toPlainText()
            self.task.due_date    = qdt
            self.task.category    = cat
            self.task.color       = color
            self.save_task.emit(self.task)
        else:
            nid = self._next_id()
            self.save_task.emit(Task(
                id=nid, title=title,
                description=self.desc_in.toPlainText(),
                due_date=qdt, category=cat, color=color,
            ))
        self.accept()

    def _next_id(self):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return max((d.get("id", 0) for d in data), default=0) + 1
        except Exception:
            return 1


# ══════════════════════════════════════════════════════════════════════════════
#  ویجت آمار
# ══════════════════════════════════════════════════════════════════════════════
class StatsWidget(QWidget):
    def __init__(self, T, parent=None):
        super().__init__(parent)
        self.T        = T
        self._counters = []
        self._build()

    def _build(self):
        T   = self.T
        lay = QHBoxLayout(self)
        lay.setSpacing(12)
        lay.setContentsMargins(0, 0, 0, 0)

        defs = [
            ("📋", "کل وظایف",  "accent", "accent_light"),
            ("✅", "انجام‌شده", "green",  "green_light"),
            ("⏳", "در انتظار", "orange", "orange_light"),
            ("🔥", "فوری",      "red",    "red_light"),
        ]
        for icon, label, fk, bk in defs:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background:{T[bk]}; border-radius:12px;
                    border:1px solid {T[fk]}{T['stat_alpha']};
                }}
            """)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            card.setFixedHeight(72)

            v = QVBoxLayout(card)
            v.setContentsMargins(14, 8, 14, 8)
            v.setSpacing(2)
            v.setAlignment(Qt.AlignCenter)

            cnt = QLabel("0")
            cnt.setFont(QFont("Segoe UI", 18, QFont.Bold))
            cnt.setStyleSheet(f"color:{T[fk]}; background:transparent;")
            cnt.setAlignment(Qt.AlignCenter)

            lbl = QLabel(f"{icon} {label}")
            lbl.setFont(QFont("Segoe UI", 8))
            lbl.setStyleSheet(f"color:{T[fk]}; background:transparent;")
            lbl.setAlignment(Qt.AlignCenter)

            v.addWidget(cnt)
            v.addWidget(lbl)
            lay.addWidget(card)
            self._counters.append(cnt)

    def update_stats(self, tasks):
        vals = [
            len(tasks),
            sum(1 for t in tasks if t.is_done),
            sum(1 for t in tasks if not t.is_done),
            sum(1 for t in tasks if t.category == "فوری" and not t.is_done),
        ]
        for cnt, val in zip(self._counters, vals):
            cnt.setText(str(val))


# ══════════════════════════════════════════════════════════════════════════════
#  سایدبار
# ══════════════════════════════════════════════════════════════════════════════
class SidebarWidget(QWidget):
    add_quick      = pyqtSignal(str)
    open_dialog    = pyqtSignal()
    filter_changed = pyqtSignal(str)
    sort_changed   = pyqtSignal(str)
    save_all       = pyqtSignal()
    toggle_theme   = pyqtSignal()

    def __init__(self, T, parent=None):
        super().__init__(parent)
        self.T = T
        self.setFixedWidth(260)
        self.setStyleSheet(f"background:{T['sidebar_bg']};")
        self._build()

    def _build(self):
        T   = self.T
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 20, 16, 20)
        lay.setSpacing(12)

        # هدر سایدبار
        hdr = QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        logo = QLabel("✅  وظایف")
        logo.setFont(QFont("Segoe UI", 13, QFont.Bold))
        logo.setStyleSheet("color:white; background:transparent;")
        hdr.addWidget(logo, 1)

        self.theme_btn = QPushButton(T["toggle_icon"])
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.setToolTip(T["toggle_tip"])
        self.theme_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background:{T['sidebar_hover']}; color:white;
                border:none; border-radius:8px; font-size:16px;
            }}
            QPushButton:hover {{ background:{T['accent']}; }}
        """)
        self.theme_btn.clicked.connect(self.toggle_theme.emit)
        hdr.addWidget(self.theme_btn)
        lay.addLayout(hdr)

        lay.addWidget(self._sep())

        # تاریخ امروز شمسی
        today_lbl = QLabel(f"📆  {today_shamsi_str()}")
        today_lbl.setFont(QFont("Segoe UI", 9))
        today_lbl.setStyleSheet(f"color:{T['sidebar_sub']}; background:transparent;")
        today_lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(today_lbl)

        # ورودی سریع
        self.task_in = self._inp("عنوان وظیفه...")
        self.desc_in = self._inp("توضیحات (اختیاری)...")
        lay.addWidget(self.task_in)
        lay.addWidget(self.desc_in)

        # دکمه‌های سریع
        grid = QHBoxLayout()
        grid.setSpacing(6)
        for cat, icon, ck in [("شخصی","👤","green"),
                               ("فوری","🔥","red"),
                               ("کار", "💼","blue")]:
            clr = T[ck]
            b   = QPushButton(f"{icon}\n{cat}")
            b.setFixedHeight(52)
            b.setCursor(QCursor(Qt.PointingHandCursor))
            b.setFont(QFont("Segoe UI", 8, QFont.Bold))
            b.setStyleSheet(f"""
                QPushButton {{ background:{clr}22; color:{clr};
                    border:1.5px solid {clr}55; border-radius:10px; }}
                QPushButton:hover {{ background:{clr}44; }}
                QPushButton:pressed {{ background:{clr}; color:white; }}
            """)
            b.clicked.connect(lambda chk, c=cat: self.add_quick.emit(c))
            grid.addWidget(b)
        lay.addLayout(grid)

        adv = self._btn("✨  افزودن پیشرفته", T["accent"], T["accent_hover"])
        adv.clicked.connect(self.open_dialog.emit)
        lay.addWidget(adv)

        lay.addWidget(self._sep())

        sl = QLabel("🔍  جستجو")
        sl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        sl.setStyleSheet(f"color:{T['sidebar_sub']}; background:transparent;")
        lay.addWidget(sl)

        self.filter_in = self._inp("جستجو در وظایف...")
        self.filter_in.textChanged.connect(self.filter_changed.emit)
        lay.addWidget(self.filter_in)

        sl2 = QLabel("⇅  مرتب‌سازی")
        sl2.setFont(QFont("Segoe UI", 9, QFont.Bold))
        sl2.setStyleSheet(f"color:{T['sidebar_sub']}; background:transparent;")
        lay.addWidget(sl2)

        sr = QHBoxLayout()
        sr.setSpacing(6)
        sd = self._btn("📅 تاریخ", "#374151", "#4B5563", small=True)
        sc = self._btn("🏷️ دسته",  "#374151", "#4B5563", small=True)
        sd.clicked.connect(lambda: self.sort_changed.emit("date"))
        sc.clicked.connect(lambda: self.sort_changed.emit("category"))
        sr.addWidget(sd)
        sr.addWidget(sc)
        lay.addLayout(sr)

        lay.addStretch(1)
        lay.addWidget(self._sep())

        save = self._btn("💾  ذخیره همه وظایف", T["green"], "#059669")
        save.clicked.connect(self.save_all.emit)
        lay.addWidget(save)

    def _sep(self):
        f = QFrame()
        f.setFrameShape(QFrame.HLine)
        f.setStyleSheet(f"color:{self.T['sidebar_hover']};")
        return f

    def _inp(self, placeholder):
        T = self.T
        w = QLineEdit()
        w.setPlaceholderText(placeholder)
        w.setFixedHeight(38)
        w.setLayoutDirection(Qt.RightToLeft)
        w.setStyleSheet(f"""
            QLineEdit {{
                background:{T['sidebar_input_bg']}; color:white;
                border:1.5px solid {T['sidebar_input_br']}; border-radius:10px;
                padding:6px 12px; font-size:10pt; font-family:'Segoe UI';
            }}
            QLineEdit:focus {{ border:1.5px solid {T['accent']}; }}
        """)
        return w

    def _btn(self, text, bg, hover, small=False):
        b = QPushButton(text)
        b.setCursor(QCursor(Qt.PointingHandCursor))
        b.setFixedHeight(36 if small else 42)
        b.setFont(QFont("Segoe UI", 9 if small else 10, QFont.Bold))
        b.setStyleSheet(f"""
            QPushButton {{ background:{bg}; color:white;
                border:none; border-radius:10px; }}
            QPushButton:hover {{ background:{hover}; }}
        """)
        return b


# ══════════════════════════════════════════════════════════════════════════════
#  پنجره اصلی
# ══════════════════════════════════════════════════════════════════════════════
class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مدیریت وظایف پیشرفته")
        self.setMinimumSize(980, 660)
        self.resize(1100, 700)
        self._theme_name = "light"
        self.T     = THEMES[self._theme_name]
        self.tasks = []
        self.load_tasks()
        self._build_ui()
        self.refresh_all()

    # ─── ساخت UI ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        T = self.T
        self.setStyleSheet(f"QMainWindow {{ background:{T['main_bg']}; }}")

        self._central = QWidget()
        self.setCentralWidget(self._central)
        self._root = QHBoxLayout(self._central)
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.setSpacing(0)

        # سایدبار
        self.sidebar = SidebarWidget(T)
        self.sidebar.add_quick.connect(self._quick_add)
        self.sidebar.open_dialog.connect(lambda: self._open_dialog())
        self.sidebar.filter_changed.connect(self._filter)
        self.sidebar.sort_changed.connect(self.sort_tasks)
        self.sidebar.save_all.connect(self.save_tasks)
        self.sidebar.toggle_theme.connect(self._switch_theme)
        self._root.addWidget(self.sidebar)

        # ناحیه اصلی
        self._right_w = QWidget()
        self._right_w.setStyleSheet(f"background:{T['main_bg']};")
        right = QVBoxLayout(self._right_w)
        right.setContentsMargins(24, 20, 24, 20)
        right.setSpacing(16)

        # هدر
        hw = QWidget()
        hw.setFixedHeight(80)
        hw.setStyleSheet(f"""
            QWidget {{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {T['header_from']}, stop:1 {T['header_to']});
                border-radius:16px;
            }}
        """)
        hi = QHBoxLayout(hw)
        hi.setContentsMargins(20, 0, 20, 0)
        ht = QLabel("📋  لیست وظایف من")
        ht.setFont(QFont("Segoe UI", 15, QFont.Bold))
        ht.setStyleSheet("color:white; background:transparent;")
        hi.addWidget(ht)
        hi.addStretch()
        dl = QLabel(today_shamsi_str())
        dl.setFont(QFont("Segoe UI", 10))
        dl.setStyleSheet("color:rgba(255,255,255,0.85); background:transparent;")
        hi.addWidget(dl)
        right.addWidget(hw)

        # آمار
        self.stats_w = StatsWidget(T)
        right.addWidget(self.stats_w)

        # پیشرفت
        pr = QHBoxLayout()
        pl = QLabel("پیشرفت کلی:")
        pl.setFont(QFont("Segoe UI", 9))
        pl.setStyleSheet(f"color:{T['text_secondary']}; background:transparent;")
        pr.addWidget(pl)

        self.prog = QProgressBar()
        self.prog.setFixedHeight(10)
        self.prog.setTextVisible(False)
        self.prog.setStyleSheet(f"""
            QProgressBar {{ background:{T['progress_bg']}; border-radius:5px; border:none; }}
            QProgressBar::chunk {{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {T['accent']}, stop:1 {T['green']});
                border-radius:5px;
            }}
        """)
        pr.addWidget(self.prog, 1)

        self.pct_lbl = QLabel("0%")
        self.pct_lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.pct_lbl.setStyleSheet(f"color:{T['accent']}; background:transparent;")
        pr.addWidget(self.pct_lbl)
        right.addLayout(pr)

        # لیست
        self._task_cont = QWidget()
        self._task_cont.setStyleSheet("background:transparent;")
        self._task_lay  = QVBoxLayout(self._task_cont)
        self._task_lay.setContentsMargins(0, 0, 4, 0)
        self._task_lay.setSpacing(10)
        self._task_lay.setAlignment(Qt.AlignTop)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(self._task_cont)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(f"""
            QScrollArea {{ border:none; background:transparent; }}
            QScrollBar:vertical {{
                background:{T['scroll_bg']}; width:6px; border-radius:3px;
            }}
            QScrollBar::handle:vertical {{
                background:{T['accent']}88; border-radius:3px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border:none; background:none;
            }}
        """)
        right.addWidget(self._scroll, 1)

        self._empty_lbl = QLabel("🎉  هیچ وظیفه‌ای وجود ندارد!\nاز سایدبار وظیفه اضافه کنید.")
        self._empty_lbl.setAlignment(Qt.AlignCenter)
        self._empty_lbl.setFont(QFont("Segoe UI", 12))
        self._empty_lbl.setStyleSheet(f"color:{T['text_secondary']}; background:transparent;")
        self._empty_lbl.setVisible(False)
        right.addWidget(self._empty_lbl)

        self._root.addWidget(self._right_w, 1)

    # ─── تغییر تم ────────────────────────────────────────────────────────────
    def _switch_theme(self):
        self._theme_name = "dark" if self._theme_name == "light" else "light"
        self.T = THEMES[self._theme_name]
        # حذف ویجت‌های قدیمی و بازسازی
        self._root.removeWidget(self.sidebar)
        self.sidebar.deleteLater()
        self._root.removeWidget(self._right_w)
        self._right_w.deleteLater()
        self._build_ui()
        self.refresh_all()

    # ─── منطق ────────────────────────────────────────────────────────────────
    def refresh_all(self):
        self._rebuild_list(self.tasks)
        self.stats_w.update_stats(self.tasks)
        done  = sum(1 for t in self.tasks if t.is_done)
        total = len(self.tasks)
        pct   = int(done / total * 100) if total else 0
        self.prog.setValue(pct)
        self.pct_lbl.setText(f"{pct}%")
        self._empty_lbl.setVisible(total == 0)

    def _rebuild_list(self, tasks):
        while self._task_lay.count():
            item = self._task_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for task in tasks:
            w = TaskWidget(task, self.T)
            w.edit_task.connect(self._edit_task)
            w.delete_task.connect(self._delete_task)
            w.toggle_done.connect(self._toggle_done)
            self._task_lay.addWidget(w)

    def _quick_add(self, category):
        title = self.sidebar.task_in.text().strip()
        if not title:
            QMessageBox.warning(self, "خطا", "لطفاً عنوان وظیفه را وارد کنید.")
            return
        desc = self.sidebar.desc_in.text().strip()
        nid  = max((t.id for t in self.tasks), default=0) + 1
        fk, bk = CAT_COLORS.get(category, ("accent", "accent_light"))
        new_task = Task(
            id=nid, title=title, description=desc,
            due_date=QDateTime.currentDateTime(),
            category=category, color=QColor(self.T[bk]),
        )
        self.tasks.append(new_task)
        self.sidebar.task_in.clear()
        self.sidebar.desc_in.clear()
        self.save_tasks()
        self.refresh_all()

    def _open_dialog(self, task=None):
        dlg = TaskDialog(self.T, task=task, parent=self)
        dlg.save_task.connect(self._handle_save)
        dlg.exec_()

    def _edit_task(self, tid):
        task = next((t for t in self.tasks if t.id == tid), None)
        if task:
            self._open_dialog(task)

    def _handle_save(self, task):
        for i, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[i] = task
                break
        else:
            self.tasks.append(task)
        self.save_tasks()
        self.refresh_all()

    def _delete_task(self, tid):
        self.tasks = [t for t in self.tasks if t.id != tid]
        self.save_tasks()
        self.refresh_all()

    def _toggle_done(self, tid):
        for t in self.tasks:
            if t.id == tid:
                t.is_done = not t.is_done
                break
        self.save_tasks()
        self.stats_w.update_stats(self.tasks)
        done  = sum(1 for t in self.tasks if t.is_done)
        total = len(self.tasks)
        pct   = int(done / total * 100) if total else 0
        self.prog.setValue(pct)
        self.pct_lbl.setText(f"{pct}%")

    def _filter(self, text):
        term = text.lower()
        for i in range(self._task_lay.count()):
            w = self._task_lay.itemAt(i).widget()
            if isinstance(w, TaskWidget):
                m = (term in w.task.title.lower() or
                     term in w.task.description.lower() or
                     term in w.task.category.lower())
                w.setVisible(m or not term)

    def sort_tasks(self, by):
        if by == "date":
            self.tasks.sort(key=lambda t: (
                t.due_date.isNull(),
                t.due_date.toSecsSinceEpoch() if not t.due_date.isNull() else float("inf")
            ))
        elif by == "category":
            self.tasks.sort(key=lambda t: t.category)
        self.refresh_all()

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                self.tasks = [Task.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            print(f"خطا: {e}")
            self.tasks = []

    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.tasks],
                          f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"خطا در ذخیره: {e}")


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setLayoutDirection(Qt.RightToLeft)
    app.setFont(QFont("Segoe UI", 10))
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
