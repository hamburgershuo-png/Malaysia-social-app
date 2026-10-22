#!/usr/bin/env python3
"""Rebuild the 2026-2027-1 Art & Technology timetable as a readable PDF."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
pdfmetrics.registerFont(TTFont("WQ", FONT, subfontIndex=0))

INK = Color(0.11, 0.10, 0.09)
MUTED = Color(0.35, 0.33, 0.31)
RULE = Color(0.82, 0.80, 0.77)
PAPER = Color(0.98, 0.97, 0.95)
SOFT = Color(0.94, 0.92, 0.89)
WHITE = white

SAGE = Color(0.25, 0.36, 0.29)
SAGE_BG = Color(0.90, 0.93, 0.90)
TEAL = Color(0.14, 0.30, 0.35)
TEAL_BG = Color(0.86, 0.91, 0.93)
AMBER = Color(0.48, 0.35, 0.10)
AMBER_BG = Color(0.96, 0.91, 0.80)
CLAY = Color(0.45, 0.25, 0.18)
CLAY_BG = Color(0.95, 0.89, 0.86)
SLATE = Color(0.27, 0.25, 0.24)
SLATE_BG = Color(0.91, 0.90, 0.89)
NAVY = Color(0.22, 0.29, 0.40)
NAVY_BG = Color(0.90, 0.92, 0.95)
GOLD = Color(0.55, 0.38, 0.14)

PAGE_W, PAGE_H = A4
MARGIN = 14 * mm

CLASSES = [
    ("A", "25人", "朱旭", "国交楼 4002"),
    ("B", "24人", "周筠", "国交楼 4004"),
    ("C", "24人", "张恒旺", "国交楼 4006"),
    ("D", "24人", "戴清材", "国交楼 4008"),
]

WEEKS = [
    (1, "9.7–9.13", "9.7 / 9.10", "报到", "新生报到（原表写在 B 班第 1 周）"),
    (2, "9.14–9.20", "9.14 / 9.17", "造型", "视觉设计与造型设计基础"),
    (3, "9.21–9.27", "9.21 / 9.24", "造型", "视觉设计与造型设计基础"),
    (4, "9.28–10.4", "9.28 / 10.1", "造型", "视觉设计与造型设计基础（含国庆，以学校通知为准）"),
    (5, "10.5–10.11", "10.5 / 10.8", "造型", "视觉设计与造型设计基础"),
    (6, "10.12–10.18", "10.12 / 10.15", "军训", "军训"),
    (7, "10.19–10.25", "10.19 / 10.22", "军训", "军训"),
    (8, "10.26–11.1", "10.26 / 10.29", "几何", "IAAD 几何学"),
    (9, "11.2–11.8", "11.2 / 11.5", "几何", "IAAD 几何学"),
    (10, "11.9–11.15", "11.9 / 11.12", "几何", "IAAD 几何学"),
    (11, "11.16–11.22", "11.16 / 11.19", "几何", "IAAD 几何学"),
    (12, "11.23–11.29", "11.23 / 11.26", "色彩", "IAAD 色彩与装饰；中外设计史加课周三 5–8 节"),
    (13, "11.30–12.6", "11.30 / 12.3", "色彩", "IAAD 色彩与装饰"),
    (14, "12.7–12.13", "12.7 / 12.10", "色彩", "IAAD 色彩与装饰"),
    (15, "12.14–12.20", "12.14 / 12.17", "色彩", "IAAD 色彩与装饰"),
    (16, "12.21–12.27", "12.21 / 12.24", "造型", "视觉设计与造型设计基础（下半段）"),
    (17, "12.28–1.3", "12.28 / 12.31", "造型", "视觉设计与造型设计基础（下半段）"),
    (18, "1.4–1.10", "1.4 / 1.7", "造型", "视觉设计与造型设计基础（仅周一下午+周四上午）"),
    (19, "1.11–1.17", "1.11 / 1.14", "复习", "复习考试"),
    (20, "1.18–1.24", "1.18 / 1.21", "复习", "复习考试"),
]

PHASE_COLOR = {
    "报到": (SLATE, SLATE_BG),
    "造型": (SAGE, SAGE_BG),
    "军训": (TEAL, TEAL_BG),
    "几何": (AMBER, AMBER_BG),
    "色彩": (CLAY, CLAY_BG),
    "复习": (NAVY, NAVY_BG),
}


def wrap_text(c, text, font, size, max_w):
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines or [""]


def draw_header(c, page_no, total, subtitle=""):
    c.setFillColor(INK)
    c.rect(0, PAGE_H - 18 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 18 * mm, 3.2 * mm, 18 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("WQ", 8.5)
    c.drawString(10 * mm, PAGE_H - 7.2 * mm, "山东艺术学院 · 国际艺术交流学院（国际艺术设计学院）")
    c.setFont("WQ", 11)
    c.drawString(10 * mm, PAGE_H - 13.4 * mm, "2026–2027 学年第一学期  ·  艺术与科技 2026 级专业课程表")
    if subtitle:
        c.setFont("WQ", 8)
        c.setFillColor(Color(0.85, 0.82, 0.76))
        c.drawRightString(PAGE_W - 10 * mm, PAGE_H - 10.4 * mm, subtitle)
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H - 18 * mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, 9 * mm, fill=1, stroke=0)
    c.setFillColor(Color(0.78, 0.75, 0.70))
    c.setFont("WQ", 7.5)
    c.drawString(10 * mm, 3.6 * mm, "按原课表重新排版，便于阅读。课表如有变动，以学院正式通知为准。")
    c.drawRightString(PAGE_W - 10 * mm, 3.6 * mm, f"{page_no} / {total}")


def section_title(c, x, y, text, w=None):
    c.setFillColor(INK)
    c.setFont("WQ", 12)
    c.drawString(x, y, text)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    c.line(x, y - 2.2 * mm, x + (w or 42 * mm), y - 2.2 * mm)
    return y - 8 * mm


def rounded(c, x, y, w, h, color, radius=3):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)


def page_cover(c, total):
    draw_header(c, 1, total, "学期总览")
    y = PAGE_H - 26 * mm

    c.setFillColor(INK)
    c.setFont("WQ", 9)
    c.drawString(MARGIN, y, "原表字体损坏、格子太密，所以按同一份课表重排成「先看阶段，再看每周，再看星期」。")
    y -= 8 * mm

    y = section_title(c, MARGIN, y, "四个班怎么分")
    col_w = (PAGE_W - 2 * MARGIN - 6 * mm) / 4
    for i, (cls, num, teacher, room) in enumerate(CLASSES):
        x = MARGIN + i * (col_w + 2 * mm)
        rounded(c, x, y - 28 * mm, col_w, 30 * mm, WHITE, 3)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.roundRect(x, y - 28 * mm, col_w, 30 * mm, 3, fill=0, stroke=1)
        c.setFillColor(GOLD)
        c.roundRect(x, y - 2.2 * mm, 18 * mm, 6.4 * mm, 2, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("WQ", 9)
        c.drawCentredString(x + 9 * mm, y - 0.4 * mm, f"{cls} 班")
        c.setFillColor(INK)
        c.setFont("WQ", 9)
        c.drawString(x + 3 * mm, y - 10 * mm, f"人数  {num}")
        c.drawString(x + 3 * mm, y - 16.5 * mm, f"教师  {teacher}")
        c.drawString(x + 3 * mm, y - 23 * mm, f"教室  {room}")
    y -= 38 * mm

    y = section_title(c, MARGIN, y, "专业课一条线看完", 48 * mm)
    phases = [
        ("第 1 周", "报到", "新生报到", SLATE, SLATE_BG),
        ("第 2–5 周", "造型上", "视觉设计与造型设计基础", SAGE, SAGE_BG),
        ("第 6–7 周", "军训", "集中军训，专业课暂停", TEAL, TEAL_BG),
        ("第 8–11 周", "几何", "IAAD 几何学  2 学分 / 32 学时", AMBER, AMBER_BG),
        ("第 12–15 周", "色彩", "IAAD 色彩与装饰  2 学分 / 32 学时", CLAY, CLAY_BG),
        ("第 16–18 周", "造型下", "造型基础后半段", SAGE, SAGE_BG),
        ("第 19–20 周", "考试", "复习考试", NAVY, NAVY_BG),
    ]
    card_h = 16 * mm
    for title, tag, desc, fg, bg in phases:
        rounded(c, MARGIN, y - card_h + 3 * mm, PAGE_W - 2 * MARGIN, card_h, bg, 2.5)
        c.setFillColor(fg)
        c.roundRect(MARGIN, y - card_h + 3 * mm, 3 * mm, card_h, 0, fill=1, stroke=0)
        c.setFont("WQ", 9.5)
        c.drawString(MARGIN + 7 * mm, y - 3.2 * mm, title)
        c.setFont("WQ", 8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 36 * mm, y - 3.2 * mm, tag)
        c.setFillColor(INK)
        c.setFont("WQ", 9)
        c.drawString(MARGIN + 52 * mm, y - 3.2 * mm, desc)
        y -= card_h + 1.6 * mm

    y -= 3 * mm
    y = section_title(c, MARGIN, y, "专业课默认时间", 42 * mm)
    c.setFillColor(INK)
    c.setFont("WQ", 9.5)
    lines = [
        "学院在表头写明：专业必修课上课时间 = 周一下午 5、6、7、8 节  +  周四上午 1、2、3、4 节。",
        "视觉设计与造型设计基础（5 学分 / 80 学时）多数周还加周五下午，用来凑满 80 学时。",
        "C 班第 2–5 周例外：周一仍是下午，周四改上 7–8 节，周五改上 3–4 节；第 16 周起与其他班相同。",
        "IAAD 几何学、IAAD 色彩与装饰按默认专业课时上课，教室与本班造型课相同。",
    ]
    for line in lines:
        c.drawString(MARGIN, y, line)
        y -= 5.4 * mm

    y -= 2 * mm
    rounded(c, MARGIN, 14 * mm, PAGE_W - 2 * MARGIN, 22 * mm, NAVY_BG, 3)
    c.setFillColor(NAVY)
    c.setFont("WQ", 8.5)
    c.drawString(MARGIN + 4 * mm, 30 * mm, "怎么用")
    c.setFillColor(INK)
    c.setFont("WQ", 8.5)
    c.drawString(MARGIN + 4 * mm, 24.2 * mm, "1. 先看第 2 页：第几周上哪门专业课。")
    c.drawString(MARGIN + 4 * mm, 19.2 * mm, "2. 再看第 3 页：这一周星期几、第几节、在哪间教室。")
    c.drawString(MARGIN + 4 * mm, 14.2 * mm, "3. 公共课（设计史、思政、英语、体育等）所有班一样，见第 4 页。")


def page_weeks(c, total):
    draw_header(c, 2, total, "二十周日历")
    y = PAGE_H - 26 * mm
    y = section_title(c, MARGIN, y, "按周对照  ·  周一 / 周四日期来自原表")
    bar_x = MARGIN
    bar_w = (PAGE_W - 2 * MARGIN) / 20
    bar_y = y + 1 * mm
    for week, span, md, tag, note in WEEKS:
        fg, bg = PHASE_COLOR[tag]
        c.setFillColor(bg)
        c.rect(bar_x, bar_y - 7.2 * mm, bar_w - 0.4 * mm, 8.4 * mm, fill=1, stroke=0)
        c.setFillColor(fg)
        c.rect(bar_x, bar_y - 7.2 * mm, 1.1 * mm, 8.4 * mm, fill=1, stroke=0)
        c.setFont("WQ", 6.2)
        c.drawCentredString(bar_x + bar_w / 2, bar_y - 2.4 * mm, str(week))
        c.setFont("WQ", 5.4)
        c.drawCentredString(bar_x + bar_w / 2, bar_y - 5.8 * mm, tag)
        bar_x += bar_w
    y -= 11 * mm

    headers = ["周次", "日期（约）", "周一 / 周四", "阶段", "这一周上什么"]
    widths = [14 * mm, 28 * mm, 28 * mm, 16 * mm, PAGE_W - 2 * MARGIN - 86 * mm]
    row_h = 8.15 * mm
    x0 = MARGIN

    def draw_row(vals, yy, fg=None, bg=None, header=False):
        x = x0
        if header:
            c.setFillColor(INK)
            c.rect(x0, yy, sum(widths), row_h, fill=1, stroke=0)
        elif bg:
            c.setFillColor(bg)
            c.rect(x0, yy, sum(widths), row_h, fill=1, stroke=0)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.3)
        c.rect(x0, yy, sum(widths), row_h, fill=0, stroke=1)
        for i, (val, w) in enumerate(zip(vals, widths)):
            if header:
                c.setFillColor(WHITE)
                c.setFont("WQ", 8)
            elif i == 3 and fg:
                c.setFillColor(fg)
                c.setFont("WQ", 8)
            else:
                c.setFillColor(INK)
                c.setFont("WQ", 8)
            c.drawString(x + 1.6 * mm, yy + 2.6 * mm, val)
            x += w

    draw_row(headers, y, header=True)
    y -= row_h
    for week, span, md, tag, note in WEEKS:
        fg, bg = PHASE_COLOR[tag]
        draw_row([f"第 {week} 周", span, md, tag, note], y, fg, bg)
        y -= row_h

    y -= 5 * mm
    y = section_title(c, MARGIN, y, "四个班的教室（专业课都在国交楼）", 62 * mm)
    c.setFont("WQ", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, "A 班 朱旭 · 4002　　B 班 周筠 · 4004　　C 班 张恒旺 · 4006　　D 班 戴清材 · 4008")
    y -= 7 * mm
    c.setFillColor(MUTED)
    c.setFont("WQ", 8)
    c.drawString(MARGIN, y, "第 1 周原表只在 B 班格子写了「新生报到」。2026 级是新生，第 1 周一般全年级报到，专业课从第 2 周开始。")


def page_weekly(c, total):
    draw_header(c, 3, total, "一周课表")
    y = PAGE_H - 26 * mm
    y = section_title(c, MARGIN, y, "先看自己在哪一段，再对号入座")

    periods = [
        ("上午 1–2 节", "约 8:30–10:20"),
        ("上午 3–4 节", "约 10:30–12:20"),
        ("下午 5–6 节", "约 13:30–15:20"),
        ("下午 7–8 节", "约 15:30–17:20"),
        ("晚上 9–10 节", "约 18:40–20:30"),
    ]

    # period reference
    box_w = (PAGE_W - 2 * MARGIN - 8 * mm) / 5
    for i, (name, t) in enumerate(periods):
        x = MARGIN + i * (box_w + 2 * mm)
        rounded(c, x, y - 12 * mm, box_w, 14 * mm, WHITE, 2)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.roundRect(x, y - 12 * mm, box_w, 14 * mm, 2, fill=0, stroke=1)
        c.setFillColor(INK)
        c.setFont("WQ", 8)
        c.drawString(x + 2 * mm, y - 2.8 * mm, name)
        c.setFillColor(MUTED)
        c.setFont("WQ", 7.5)
        c.drawString(x + 2 * mm, y - 8.2 * mm, t)
    y -= 20 * mm
    c.setFillColor(MUTED)
    c.setFont("WQ", 7.5)
    c.drawString(MARGIN, y, "钟点按长清校区秋季作息整理，当年以教务处通知为准。")
    y -= 8 * mm

    def grid(title, rows, top):
        nonlocal y
        y = section_title(c, MARGIN, top, title, 78 * mm)
        days = ["节次", "周一", "周二", "周三", "周四", "周五"]
        widths = [18 * mm] + [(PAGE_W - 2 * MARGIN - 18 * mm) / 5] * 5
        rh = 12.4 * mm
        c.setFillColor(INK)
        c.rect(MARGIN, y, sum(widths), 7 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("WQ", 8)
        xx = MARGIN
        for d, w in zip(days, widths):
            c.drawCentredString(xx + w / 2, y + 2.2 * mm, d)
            xx += w
        y -= rh
        slots = ["1–2 节", "3–4 节", "5–6 节", "7–8 节", "9–10 节"]
        for r, slot in enumerate(slots):
            xx = MARGIN
            c.setFillColor(SOFT if r % 2 == 0 else WHITE)
            c.rect(MARGIN, y, sum(widths), rh, fill=1, stroke=0)
            c.setStrokeColor(RULE)
            c.setLineWidth(0.35)
            c.rect(MARGIN, y, sum(widths), rh, fill=0, stroke=1)
            for col, w in enumerate(widths):
                if col == 0:
                    c.setFillColor(MUTED)
                    c.setFont("WQ", 8)
                    c.drawCentredString(xx + w / 2, y + 4.8 * mm, slot)
                else:
                    line1, line2, kind = rows[r][col - 1]
                    if kind:
                        fg, bg = {
                            "sage": (SAGE, SAGE_BG),
                            "amber": (AMBER, AMBER_BG),
                            "clay": (CLAY, CLAY_BG),
                            "navy": (NAVY, NAVY_BG),
                            "teal": (TEAL, TEAL_BG),
                        }[kind]
                        c.setFillColor(bg)
                        c.rect(xx + 0.5 * mm, y + 0.5 * mm, w - 1.0 * mm, rh - 1.0 * mm, fill=1, stroke=0)
                        c.setFillColor(fg)
                    else:
                        c.setFillColor(INK)
                    if line1:
                        c.setFont("WQ", 7.4)
                        c.drawCentredString(xx + w / 2, y + 6.6 * mm, line1)
                    if line2:
                        c.setFont("WQ", 6.6)
                        c.setFillColor(MUTED if not kind else fg)
                        c.drawCentredString(xx + w / 2, y + 2.6 * mm, line2)
                xx += w
            y -= rh
        y -= 4 * mm

    empty = ("", "", None)
    normal_shape = [
        [empty, ("艺术学概论", "报告厅 1 · 王淑君", "navy"), ("英语", "11–12 教室", "navy"), ("专业课", "本班国交楼", "sage"), ("近现代史纲要", "2 教室 · 韩锡玲", "navy")],
        [("军事理论", "", "navy"), empty, ("英语", "11–12 教室", "navy"), ("专业课", "本班国交楼", "sage"), empty],
        [("专业课", "本班国交楼", "sage"), empty, empty, ("英语", "11–12 教室", "navy"), ("造型加课", "本班国交楼", "sage")],
        [("专业课", "本班国交楼", "sage"), ("体育", "", "navy"), ("中外设计史", "实验中心楼 3014", "navy"), empty, ("造型加课", "本班国交楼", "sage")],
        [empty, empty, empty, empty, empty],
    ]
    grid("A / B / D 班 · 第 2–5 周、第 16–17 周（造型课加周五下午）", normal_shape, y)

    c_shape = [
        [empty, ("艺术学概论", "报告厅 1 · 王淑君", "navy"), ("英语", "11–12 教室", "navy"), empty, ("近现代史纲要", "2 教室 · 韩锡玲", "navy")],
        [("军事理论", "", "navy"), empty, ("英语", "11–12 教室", "navy"), empty, ("造型课", "国交楼 4006", "sage")],
        [("专业课", "国交楼 4006", "sage"), empty, empty, ("英语", "11–12 教室", "navy"), empty],
        [("专业课", "国交楼 4006", "sage"), ("体育", "", "navy"), ("中外设计史", "实验中心楼 3014", "navy"), ("造型课", "国交楼 4006", "sage"), empty],
        [empty, empty, empty, empty, empty],
    ]
    grid("C 班特例 · 仅第 2–5 周（周四改 7–8 节，周五改 3–4 节）", c_shape, y)

    c.setFillColor(MUTED)
    c.setFont("WQ", 7.8)
    notes = [
        "第 8–15 周：把表里的「专业课 / 造型课」换成 IAAD 几何学或色彩与装饰；时间回到周一 5–8 节 + 周四 1–4 节，不再加周五下午。",
        "第 18 周造型课只上周一 5–8 节和周四 1–4 节。第 6–7 周军训。第 19–20 周复习考试。第 12 周中外设计史加到周三 5–8 节。",
        "形势与政策只在第 7–8 周周四 9–10 节，韩锡玲，2 教室。C 班第 16 周起的一周课表与 A/B/D 班相同。",
    ]
    for n in notes:
        for line in wrap_text(c, n, "WQ", 7.8, PAGE_W - 2 * MARGIN):
            c.drawString(MARGIN, y, line)
            y -= 4.2 * mm
        y -= 0.6 * mm


def page_public(c, total):
    draw_header(c, 4, total, "公共课与说明")
    y = PAGE_H - 26 * mm
    y = section_title(c, MARGIN, y, "四个班一起上的课")

    pubs = [
        ("中外设计史", "米华（2–5、8–15 周）\n荆雷（16–18 周）", "周三下午 7–8 节\n第 12 周改为周三 5–8 节", "实验中心楼 3014", "第 6–7 周军训停课"),
        ("军事理论", "原表未写教师", "周一 3–4 节", "未单独写教室", "全学期按学校安排"),
        ("艺术学概论", "王淑君", "周二 3–4 节", "报告厅 1", ""),
        ("体育", "原表未写教师", "周二 7–8 节", "以体育部安排为准", ""),
        ("英语", "原表未写教师", "周三 1–4 节\n周四 5–6 节", "11–12 教室", ""),
        ("形势与政策", "韩锡玲", "周四 9–10 节", "2 教室", "只上第 7–8 周"),
        ("中国近现代史纲要", "韩锡玲", "周五 1–2 节", "2 教室", ""),
    ]
    headers = ["课程", "教师", "时间", "地点", "备注"]
    widths = [32 * mm, 38 * mm, 40 * mm, 32 * mm, PAGE_W - 2 * MARGIN - 142 * mm]
    rh = 13.2 * mm
    x0 = MARGIN
    c.setFillColor(INK)
    c.rect(x0, y, sum(widths), 7.2 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("WQ", 8)
    xx = x0
    for h, w in zip(headers, widths):
        c.drawString(xx + 1.8 * mm, y + 2.3 * mm, h)
        xx += w
    y -= rh
    for i, row in enumerate(pubs):
        bg = WHITE if i % 2 else SOFT
        c.setFillColor(bg)
        c.rect(x0, y, sum(widths), rh, fill=1, stroke=0)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.35)
        c.rect(x0, y, sum(widths), rh, fill=0, stroke=1)
        xx = x0
        for j, (val, w) in enumerate(zip(row, widths)):
            c.setFillColor(INK if j == 0 else MUTED)
            c.setFont("WQ", 8 if j == 0 else 7.4)
            lines = val.split("\n")
            ty = y + rh - 4.6 * mm
            for line in lines:
                c.drawString(xx + 1.8 * mm, ty, line)
                ty -= 3.6 * mm
            xx += w
        y -= rh

    y -= 6 * mm
    y = section_title(c, MARGIN, y, "专业课学分与教室")
    pro = [
        ("视觉设计与造型设计基础", "5 学分 / 80 学时", "2–5 周、16–18 周", "各班自己的国交楼教室"),
        ("IAAD 几何学", "2 学分 / 32 学时", "8–11 周", "各班自己的国交楼教室"),
        ("IAAD 色彩与装饰", "2 学分 / 32 学时", "12–15 周", "各班自己的国交楼教室"),
        ("军训", "按学校军事课安排", "6–7 周", "按武装部 / 学工通知"),
    ]
    headers = ["课程", "学分 / 学时", "周次", "地点"]
    widths = [52 * mm, 38 * mm, 40 * mm, PAGE_W - 2 * MARGIN - 130 * mm]
    rh = 8.2 * mm
    c.setFillColor(INK)
    c.rect(MARGIN, y, sum(widths), 7.2 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("WQ", 8)
    xx = MARGIN
    for h, w in zip(headers, widths):
        c.drawString(xx + 1.8 * mm, y + 2.3 * mm, h)
        xx += w
    y -= rh
    for i, row in enumerate(pro):
        c.setFillColor(WHITE if i % 2 else SOFT)
        c.rect(MARGIN, y, sum(widths), rh, fill=1, stroke=0)
        c.setStrokeColor(RULE)
        c.rect(MARGIN, y, sum(widths), rh, fill=0, stroke=1)
        xx = MARGIN
        for j, (val, w) in enumerate(zip(row, widths)):
            c.setFillColor(INK)
            c.setFont("WQ", 8)
            c.drawString(xx + 1.8 * mm, y + 2.8 * mm, val)
            xx += w
        y -= rh

    y -= 6 * mm
    y = section_title(c, MARGIN, y, "还原说明（原表看不清的地方）", 58 * mm)
    c.setFillColor(INK)
    c.setFont("WQ", 8.3)
    notes = [
        "原图是一份 excel/pdf 课表截图，中文字体映射坏了，格子里挤着课程、周次、教师、教室。本 PDF 按像素切格做了中文 OCR，并用山东艺术学院公开师资名录校对了能对上的姓名。",
        "已核对：朱旭、周筠、张恒旺、戴清材、米华、荆雷、韩锡玲、王淑君；教室国交楼 4002/4004/4006/4008、实验中心楼 3014、报告厅 1、11–12 教室、2 教室。",
        "IAAD 为意大利应用艺术与设计学院（Istituto d'Arte Applicata e Design）导入课程，原表黄格里只写了课名和教室，没有中方教师姓名，故不臆造。",
        "第 1 周日期原表写作 9.10，从第 2 周起表头上一行是周一、下一行是周四。本表把第 1 周按 9.7（周一）–9.13 补全，方便对照校历。",
        "军事理论、体育、英语的教师原表未写清；作息钟点来自学校长清校区秋季作息的历史公布，若 2026 年有调整，以教务处为准。",
    ]
    for n in notes:
        for line in wrap_text(c, "·  " + n, "WQ", 8.3, PAGE_W - 2 * MARGIN):
            c.drawString(MARGIN, y, line)
            y -= 4.3 * mm
        y -= 1.4 * mm


def main():
    out_repo = "/workspace/schedule/2026-2027-1-艺术与科技-课程表.pdf"
    out_art = "/opt/cursor/artifacts/2026-2027-1-艺术与科技-课程表.pdf"
    c = canvas.Canvas(out_repo, pagesize=A4)
    c.setTitle("2026-2027学年第一学期 艺术与科技专业课程表")
    c.setAuthor("国际艺术交流学院（国际艺术设计学院）课表重排")
    total = 4
    page_cover(c, total)
    c.showPage()
    page_weeks(c, total)
    c.showPage()
    page_weekly(c, total)
    c.showPage()
    page_public(c, total)
    c.save()
    import shutil
    shutil.copy2(out_repo, out_art)
    print("wrote", out_repo)
    print("wrote", out_art)


if __name__ == "__main__":
    main()
