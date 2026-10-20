## ----------------------------------------------------------------------------
##  НАСТРОЙКИ
## ----------------------------------------------------------------------------

define SPRITE_ZOOM = 1.0      # общий масштаб спрайтов
define MUSIC_ON = False       # фоновая музыка: False — выключена, True — включить


## --- Персонажи --------------------------------------------------------------
define m  = Character("Марина", color="#ff8fa8")
define a  = Character("Аля", color="#8fd3ff")
define v  = Character("Вика", color="#b6f08f")
define yu = Character("Юля", color="#ffd98f")
define s  = Character("Серёга", color="#f4a261")
define t  = Character("Тамара Ивановна", color="#ff6b6b")

## --- Переходы ---------------------------------------------------------------
define flash = Fade(0.1, 0.0, 0.8, color="#ffffff")
define slow_fade = Fade(1.0, 0.5, 1.0)
define quick = Dissolve(0.2)       # смена говорящего

## --- Позиция спрайта ---------------------------------------------------------
## На экране виден только тот, кто сейчас говорит: он стоит по центру.
transform pos_speaker:
    xalign 0.5 yalign 1.0
    zoom SPRITE_ZOOM

transform retro:
    matrixcolor TintMatrix("#f4e4c8") * SaturationMatrix(0.75)


## ----------------------------------------------------------------------------
##  АВТОПОДКЛЮЧЕНИЕ КАРТИНОК И ЗВУКОВ
## ----------------------------------------------------------------------------

init -2 python:

    SPRITE_DIR = "images/sprites/"

    BACKGROUNDS = [
        "room_modern_night", "room_modern_morning", "dorm_1985", "street_1985",
        "bus_1985", "polytech_hall", "lecture_hall", "canteen",
        "dorm_corridor_evening",
    ]


    ## Обычный мир
    MODERN = {
        "marina": {
            "normal":    "marina_surprised.PNG",
            "happy":     "marina_happy.png",
            "surprised": "marina_surprised.PNG",
            "thinking":  "marina_surprised.PNG",
            "sleepy":    "marina_surprised.PNG",
            "shout":     "marina_shoked.PNG",
            "shocked":   "marina_shoked.PNG",
            "one":       "marina_one.PNG",
        },
        "alya": {
            "normal":    "alya_thinking.PNG",
            "happy":     "alya_happy.png",
            "surprised": "Alya_surprised.png",
            "thinking":  "alya_thinking.PNG",
            "sleepy":    "alya_thinking.PNG",
            "shout":     "Alya_surprised.png",
            "one":       "alya_one.PNG",
        },
        "vika": {
            "normal":    "vika_thinking.png",
            "happy":     "vika_thinking.png",
            "surprised": "vika_thinking.png",
            "thinking":  "vika_thinking.png",
            "sleepy":    "vika_thinking.png",
            "shout":     "vika_thinking.png",
            "one":       "vika_one.PNG",
        },
        "yulya": {
            "normal":    "yulya_happy.png",
            "happy":     "yulya_happy.png",
            "surprised": "yulya_surprised.png",
            "thinking":  "yulya_surprised.png",
            "sleepy":    "yulya_happy.png",
            "shout":     "yulya_shoked.png",
            "shocked":   "yulya_shoked.png",
            "one":       "yulya_one.PNG",
        },
        "serega": {
            "normal":    "serega_normal.png",
            "happy":     "serega_normal.png",
            "serious":   "serega_normal.png",
        },
    }

    ## Советская одежда
    SOVIET = {
        "marina": {
            "normal":    "marina_Unormal.png",
            "happy":     "marina_Unormal.png",
            "surprised": "marina_Uthinking2.png",
            "thinking":  "marina_Uthinking.png",
            "thinking2": "marina_Uthinking2.png",
            "sleepy":    "marina_Unormal.png",
            "shout":     "marina_Uthinking2.png",
        },
        "alya": {
            "normal":    "alya_Unormal.png",
            "happy":     "alya_Unormal.png",
            "surprised": "alya_Usurprised.png",
            "thinking":  "alya_Uthinking.png",
            "sleepy":    "alya_Unormal.png",
            "shout":     "alya_Usurprised.png",
        },
        "vika": {
            "normal":    "vika_Unormal.png",
            "happy":     "vika_Uhappy.png",
            "surprised": "vika_Unormal.png",
            "thinking":  "vika_Uthinking.png",
            "sleepy":    "vika_Unormal.png",
            "shout":     "vika_Unormal.png",
        },
        "yulya": {
            "normal":    "yulya_Uthinking.png",
            "happy":     "yulya_Uthinking.png",
            "surprised": "yulya_Uthinking2.png",
            "thinking":  "yulya_Uthinking.png",
            "thinking2": "yulya_Uthinking2.png",
            "sleepy":    "yulya_Uthinking2.png",
            "shout":     "yulya_Uthinking2.png",
        },
    }

    def _find_image(folder, fname):
        for ext in ("png", "webp", "jpg", "jpeg"):
            p = "images/{}/{}.{}".format(folder, fname, ext)
            if renpy.loadable(p):
                return p
        return None

    def reg_bg(name):
        p = _find_image("bg", name)
        renpy.image(("bg", name), p if p else Placeholder("bg", text=name))

    def reg_sprite(char, emo, fname, prefix=""):
        path = SPRITE_DIR + fname
        shown = prefix + emo
        if renpy.loadable(path):
            renpy.image((char, shown), path)
        else:
            renpy.image((char, shown), Placeholder("boy" if char == "serega" else "girl", text="{} {}".format(char, shown)))

    for _bg in BACKGROUNDS:
        reg_bg(_bg)
    for _char, _d in MODERN.items():
        for _emo, _f in _d.items():
            reg_sprite(_char, _emo, _f)
    for _char, _d in SOVIET.items():
        for _emo, _f in _d.items():
            reg_sprite(_char, _emo, _f, prefix="u_")

    ## --- Звук
    def _audio_path(name):
        for ext in ("ogg", "mp3", "opus", "wav"):
            p = "audio/{}.{}".format(name, ext)
            if renpy.loadable(p):
                return p
        return None

    def bgm(name=None, fadein=1.0, fadeout=1.0):
        """bgm("dorm_1985") — включить музыку, bgm() — выключить."""
        if not store.MUSIC_ON:
            return
        if name is None:
            renpy.music.stop(channel="music", fadeout=fadeout)
            return
        p = _audio_path(name)
        if p:
            renpy.music.play(p, channel="music", loop=True, fadein=fadein, fadeout=fadeout)

    def sfx(name, loop=False):
        """sfx("alarm") — проиграть звук."""
        p = _audio_path(name)
        if p:
            renpy.sound.play(p, loop=loop)

    def sfx_stop(fadeout=0.5):
        renpy.sound.stop(fadeout=fadeout)


## ----------------------------------------------------------------------------
##  ПЕРЕМЕННЫЕ ВЫБОРОВ
## ----------------------------------------------------------------------------

default breakfast = ""    
default lunch = ""        
default coins_left = 50   
