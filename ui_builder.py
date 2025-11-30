"""
Bot Mesh v23.0 ULTRA PRO - Premium 3D UI System
Created by: Abeer Aldosari © 2025

✨ تصميم ثري دي فائق الاحترافية
🎨 نظام ألوان متطور ومريح للعين
🎯 تسجيل ذكي وتلقائي
👁️ واجهة أنيقة وسهلة الاستخدام
⚡ تأثيرات بصرية متقدمة
🔄 تحديث تلقائي للأسماء
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS, FIXED_GAME_QR
from typing import Optional, List, Dict


def _colors(theme=None):
    """الحصول على ألوان الثيم مع تحسينات"""
    return THEMES.get(theme or DEFAULT_THEME, THEMES[DEFAULT_THEME])


# ============================================================================
# نظام البطاقات الثري دي المتطور
# ============================================================================

def _ultra_card(contents, theme=None, shadow_depth="8px", glow=False):
    """بطاقة ثري دي فائقة مع ظل عميق وتوهج اختياري"""
    c = _colors(theme)
    
    card = {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": c["card"],
        "cornerRadius": "24px",
        "paddingAll": "24px",
        "margin": "md",
        "borderWidth": "1px",
        "borderColor": c["primary"] if glow else c["border"],
        "offsetBottom": shadow_depth,
        "offsetStart": "0px",
        "offsetEnd": "0px"
    }
    
    return card


def _glass_card(contents, theme=None):
    """بطاقة زجاجية شفافة (Glassmorphism)"""
    c = _colors(theme)
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": c["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "margin": "md",
        "borderWidth": "2px",
        "borderColor": c["border"],
        "offsetBottom": "5px"
    }


def _gradient_header(title, subtitle=None, icon=None, theme=None):
    """ترويسة متدرجة فاخرة مع أيقونة"""
    c = _colors(theme)
    
    contents = []
    
    if icon:
        contents.append({
            "type": "text",
            "text": icon,
            "size": "3xl",
            "align": "center",
            "margin": "none"
        })
    
    contents.append({
        "type": "text",
        "text": title,
        "size": "xxl",
        "weight": "bold",
        "color": c["button_text"],
        "align": "center",
        "margin": "sm" if icon else "none"
    })
    
    if subtitle:
        contents.append({
            "type": "text",
            "text": subtitle,
            "size": "sm",
            "color": c["button_text"],
            "align": "center",
            "margin": "sm",
            "weight": "bold"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "background": {
            "type": "linearGradient",
            "angle": "135deg",
            "startColor": c["gradient_start"],
            "endColor": c["gradient_end"]
        },
        "cornerRadius": "24px",
        "paddingAll": "28px",
        "margin": "none",
        "offsetBottom": "8px"
    }


def _floating_button(label, text, icon="", style="primary", theme=None):
    """زر عائم ثري دي مع أيقونة"""
    c = _colors(theme)
    
    colors_map = {
        "primary": {"bg": c["primary"], "text": c["button_text"], "border": c["primary"]},
        "secondary": {"bg": c["secondary"], "text": c["button_text"], "border": c["secondary"]},
        "success": {"bg": c["success"], "text": c["button_text"], "border": c["success"]},
        "accent": {"bg": c["accent"], "text": c["button_text"], "border": c["accent"]},
        "outline": {"bg": c["card"], "text": c["text"], "border": c["border"]}
    }
    
    btn_colors = colors_map.get(style, colors_map["primary"])
    display_text = f"{icon} {label}" if icon else label
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": display_text,
                "size": "md",
                "weight": "bold",
                "color": btn_colors["text"],
                "align": "center",
                "gravity": "center"
            }
        ],
        "backgroundColor": btn_colors["bg"],
        "cornerRadius": "16px",
        "paddingAll": "16px",
        "action": {"type": "message", "text": text},
        "height": "56px",
        "borderWidth": "2px",
        "borderColor": btn_colors["border"],
        "offsetBottom": "5px",
        "flex": 1
    }


def _metric_display(value, label, icon, color_key="primary", theme=None):
    """عرض مقياس احترافي مع أيقونة"""
    c = _colors(theme)
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": icon,
                "size": "3xl",
                "align": "center",
                "gravity": "center"
            },
            {
                "type": "text",
                "text": str(value),
                "size": "3xl",
                "weight": "bold",
                "color": c[color_key],
                "align": "center",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": label,
                "size": "sm",
                "color": c["text3"],
                "align": "center",
                "weight": "bold",
                "margin": "sm"
            }
        ],
        "backgroundColor": c["card"],
        "cornerRadius": "20px",
        "paddingAll": "24px",
        "borderWidth": "2px",
        "borderColor": c[color_key],
        "flex": 1,
        "offsetBottom": "6px"
    }


def _progress_bar(current, total, label, theme=None):
    """شريط تقدم أنيق مع نسبة مئوية"""
    c = _colors(theme)
    percentage = min(int((current / total) * 100), 100) if total > 0 else 0
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": label,
                        "size": "sm",
                        "color": c["text2"],
                        "weight": "bold",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{percentage}%",
                        "size": "sm",
                        "color": c["primary"],
                        "weight": "bold",
                        "align": "end",
                        "flex": 0
                    }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": f"{percentage}%",
                        "height": "10px",
                        "backgroundColor": c["primary"],
                        "cornerRadius": "5px"
                    }
                ],
                "backgroundColor": c["border"],
                "height": "10px",
                "cornerRadius": "5px",
                "margin": "md"
            }
        ],
        "margin": "lg"
    }


def _divider(style="line", theme=None):
    """فاصل أنيق بأنماط متعددة"""
    c = _colors(theme)
    
    if style == "diamond":
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "box", "layout": "vertical", "contents": [], "flex": 1, "height": "2px", "backgroundColor": c["border"]},
                {"type": "text", "text": "◆", "size": "xs", "color": c["primary"], "align": "center", "flex": 0, "margin": "none"},
                {"type": "box", "layout": "vertical", "contents": [], "flex": 1, "height": "2px", "backgroundColor": c["border"]}
            ],
            "margin": "xl",
            "alignItems": "center"
        }
    elif style == "dots":
        return {
            "type": "text",
            "text": "• • •",
            "size": "sm",
            "color": c["border"],
            "align": "center",
            "margin": "xl"
        }
    else:
        return {
            "type": "separator",
            "margin": "xl",
            "color": c["border"]
        }


def _badge(text, style="info", theme=None):
    """شارة معلومات أنيقة"""
    c = _colors(theme)
    
    styles = {
        "info": {"bg": c["info_bg"], "border": c["info"], "text": c["text"]},
        "success": {"bg": c["success_bg"], "border": c["success"], "text": c["text"]},
        "warning": {"bg": c["error_bg"], "border": c["warning"], "text": c["text"]},
        "primary": {"bg": c["primary"], "border": c["primary"], "text": c["button_text"]}
    }
    
    badge_style = styles.get(style, styles["info"])
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": text,
                "size": "sm",
                "weight": "bold",
                "color": badge_style["text"],
                "align": "center"
            }
        ],
        "backgroundColor": badge_style["bg"],
        "cornerRadius": "14px",
        "paddingAll": "14px",
        "borderWidth": "2px",
        "borderColor": badge_style["border"],
        "margin": "md",
        "offsetBottom": "3px"
    }


def _game_tile(game_name, theme=None, is_popular=False):
    """بلاطة لعبة ثري دي احترافية"""
    c = _colors(theme)
    
    game_info = {
        "ذكاء": {"icon": "🧠", "color": "primary"},
        "رياضيات": {"icon": "🔢", "color": "info"},
        "لون": {"icon": "🎨", "color": "accent"},
        "ترتيب": {"icon": "🔤", "color": "secondary"},
        "أسرع": {"icon": "⚡", "color": "warning"},
        "ضد": {"icon": "↔️", "color": "success"},
        "تكوين": {"icon": "📝", "color": "primary"},
        "أغنيه": {"icon": "🎵", "color": "accent"},
        "لعبة": {"icon": "🎮", "color": "info"},
        "سلسلة": {"icon": "⛓️", "color": "secondary"},
        "خمن": {"icon": "🤔", "color": "warning"},
        "توافق": {"icon": "💕", "color": "success"}
    }
    
    info = game_info.get(game_name, {"icon": "🎯", "color": "primary"})
    
    contents = [
        {
            "type": "text",
            "text": info["icon"],
            "size": "3xl",
            "align": "center"
        },
        {
            "type": "text",
            "text": game_name,
            "size": "lg",
            "weight": "bold",
            "color": c["text"],
            "align": "center",
            "margin": "md"
        }
    ]
    
    if is_popular:
        contents.insert(0, {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "⭐",
                    "size": "xs",
                    "align": "center"
                }
            ],
            "position": "absolute",
            "offsetTop": "8px",
            "offsetEnd": "8px",
            "backgroundColor": c["warning"],
            "cornerRadius": "12px",
            "paddingAll": "4px",
            "width": "28px",
            "height": "28px"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": c["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "action": {"type": "message", "text": game_name},
        "borderWidth": "2px",
        "borderColor": c[info["color"]],
        "flex": 1,
        "offsetBottom": "5px"
    }


# ============================================================================
# الصفحة الرئيسية الفائقة
# ============================================================================

def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME, mode_label="فردي"):
    """الصفحة الرئيسية بتصميم فائق الاحترافية"""
    c = _colors(theme)
    
    # حساب المستوى
    if points < 50:
        level, badge, progress_max, next_level = "مبتدئ", "🌱", 50, "متوسط"
    elif points < 150:
        level, badge, progress_max, next_level = "متوسط", "⭐", 150, "متقدم"
    elif points < 300:
        level, badge, progress_max, next_level = "متقدم", "🔥", 300, "محترف"
    else:
        level, badge, progress_max, next_level = "محترف", "👑", points + 100, "أسطورة"
    
    status_icon = "✅" if is_registered else "⚠️"
    status_text = "نشط" if is_registered else "غير مسجل"
    status_color = "success" if is_registered else "warning"
    
    body = {
        "type": "carousel",
        "contents": [
            # البطاقة الأولى: الملف الشخصي
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        _gradient_header("مرحباً", username, "👋", theme),
                        
                        _ultra_card([
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "spacing": "md",
                                "contents": [
                                    _metric_display(points, "النقاط", "🏆", "primary", theme),
                                    _metric_display(level, "المستوى", badge, status_color, theme)
                                ]
                            }
                        ], theme, "8px", True),
                        
                        _progress_bar(points, progress_max, f"التقدم نحو {next_level}", theme),
                        
                        _badge(f"{status_icon} {status_text} • وضع {mode_label}", "primary", theme),
                        
                        _divider("diamond", theme),
                        
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        _floating_button("الألعاب", "ألعاب", "🎮", "primary", theme),
                                        _floating_button("نقاطي", "نقاطي", "📊", "secondary", theme)
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        _floating_button("الصدارة", "صدارة", "🏆", "accent", theme),
                                        _floating_button("المساعدة", "مساعدة", "❓", "outline", theme)
                                    ]
                                }
                            ]
                        },
                        
                        _divider("dots", theme),
                        
                        {
                            "type": "text",
                            "text": BOT_RIGHTS,
                            "size": "xxs",
                            "color": c["text3"],
                            "align": "center",
                            "wrap": True
                        }
                    ],
                    "paddingAll": "0px",
                    "backgroundColor": c["bg"]
                }
            },
            
            # البطاقة الثانية: المظهر
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        _gradient_header("المظهر", "اختر الثيم المفضل", "🎨", theme),
                        
                        _badge("✨ تخصيص الألوان", "primary", theme),
                        
                        *_generate_theme_grid(theme),
                        
                        _glass_card([
                            {
                                "type": "text",
                                "text": "💡 نصيحة",
                                "size": "md",
                                "weight": "bold",
                                "color": c["primary"],
                                "margin": "none"
                            },
                            {
                                "type": "text",
                                "text": "اختر الثيم الذي يريح عينك ويناسب ذوقك الشخصي",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            }
                        ], theme),
                        
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "margin": "lg",
                            "contents": [
                                _floating_button("رجوع", "بداية", "🏠", "secondary", theme),
                                _floating_button("الألعاب", "ألعاب", "🎮", "primary", theme)
                            ]
                        }
                    ],
                    "paddingAll": "0px",
                    "backgroundColor": c["bg"]
                }
            }
        ]
    }
    
    msg = FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(body))
    msg.quick_reply = _build_quick_reply()
    return msg


def _generate_theme_grid(current_theme):
    """توليد شبكة الثيمات"""
    themes_list = list(THEMES.keys())
    theme_icons = {
        "أبيض": "☀️", "أسود": "🌙", "أزرق": "💙", "بنفسجي": "💜",
        "وردي": "💗", "أخضر": "💚", "برتقالي": "🧡", "أحمر": "❤️", "بني": "🤎"
    }
    
    rows = []
    for i in range(0, len(themes_list), 3):
        row_themes = themes_list[i:i+3]
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                _floating_button(
                    theme_icons.get(t, "🎨"),
                    f"ثيم {t}",
                    t,
                    "primary" if t == current_theme else "outline",
                    current_theme
                )
                for t in row_themes
            ]
        })
    
    return rows


# ============================================================================
# قائمة الألعاب الفائقة
# ============================================================================

def build_games_menu(theme=DEFAULT_THEME, top_games=None):
    """قائمة ألعاب فائقة الاحترافية"""
    c = _colors(theme)
    
    default_order = ["أسرع", "ذكاء", "لعبة", "خمن", "أغنيه", "سلسلة",
                     "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"]
    
    games = (top_games[:6] + [g for g in default_order if g not in (top_games or [])])[:12]
    popular_games = games[:3]
    
    game_rows = []
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
        game_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                _game_tile(g, theme, g in popular_games)
                for g in row_games
            ]
        })
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                _gradient_header("الألعاب", "اختر لعبتك المفضلة", "🎮", theme),
                
                _badge("⭐ الأكثر شعبية", "success", theme),
                
                *game_rows,
                
                _divider("diamond", theme),
                
                _glass_card([
                    {
                        "type": "text",
                        "text": "ℹ️ كيف تلعب",
                        "size": "md",
                        "weight": "bold",
                        "color": c["primary"]
                    },
                    {
                        "type": "text",
                        "text": "• اضغط على اللعبة للبدء\n• 'لمح' للمساعدة\n• 'جاوب' لكشف الإجابة\n• 'إيقاف' للإنهاء",
                        "size": "sm",
                        "color": c["text2"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ], theme),
                
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        _floating_button("رجوع", "بداية", "🏠", "secondary", theme),
                        _floating_button("إيقاف", "إيقاف", "🛑", "outline", theme)
                    ]
                },
                
                _divider("line", theme),
                
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": c["text3"],
                    "align": "center"
                }
            ],
            "paddingAll": "0px",
            "backgroundColor": c["bg"]
        }
    }
    
    msg = FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(body))
    msg.quick_reply = _build_quick_reply()
    return msg


# ============================================================================
# صفحة النقاط الفائقة
# ============================================================================

def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    """صفحة إحصائيات فائقة الاحترافية"""
    c = _colors(theme)
    
    # تحديد المستوى
    if points < 50:
        level, badge, color, progress_current, progress_max, next_level = "مبتدئ", "🌱", "text2", points, 50, "متوسط"
    elif points < 150:
        level, badge, color, progress_current, progress_max, next_level = "متوسط", "⭐", "info", points - 50, 100, "متقدم"
    elif points < 300:
        level, badge, color, progress_current, progress_max, next_level = "متقدم", "🔥", "warning", points - 150, 150, "محترف"
    else:
        level, badge, color, progress_current, progress_max, next_level = "محترف", "👑", "success", 100, 100, "أسطورة"
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                _gradient_header(username, f"مستوى {level}", badge, theme),
                
                _ultra_card([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "contents": [
                            _metric_display(points, "النقاط", "🏆", "primary", theme),
                            _metric_display(level, "المستوى", badge, color, theme)
                        ]
                    }
                ], theme, "8px", True),
                
                _progress_bar(progress_current, progress_max, f"التقدم نحو {next_level}", theme),
                
                _glass_card([
                    {
                        "type": "text",
                        "text": "💡 نصيحة",
                        "size": "md",
                        "weight": "bold",
                        "color": c["primary"]
                    },
                    {
                        "type": "text",
                        "text": "العب المزيد من الألعاب لزيادة نقاطك والوصول للمستوى التالي!",
                        "size": "sm",
                        "color": c["text2"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ], theme),
                
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        _floating_button("رجوع", "ب
