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


## ----------------------------------------------------------------------------
##  ТАБЛИЦА СРАВНЕНИЯ (финал)
## ----------------------------------------------------------------------------

init python:
    TABLE_ROWS = [
        ("Критерий сравнения",
         "Студенчество в СССР (1980-е)",
         "Современное студенчество"),
        ("Образование и идеология",
         "Бесплатное. Жёсткий контроль посещаемости. Обязательные дисциплины: История КПСС, Марксизм-ленинизм.",
         "Платное/бюджет. Больше свободы выбора дисциплин. Новый курс: «Основы российской государственности»."),
        ("Финансы и подработки",
         "Стипендия 40-50 руб. (хватало на жизнь). Летом — огромные заработки в ССО (строительные отряды). Осенняя «картошка».",
         "Стипендия часто символическая. Подработки в гибком графике (курьеры, фриланс, IT), ССО носят более добровольный характер."),
        ("Быт и технологии",
         "Отсутствие гаджетов, черчение вручную (тубусы, готовальни). Общежития с коллективным бытом и строгим комендантским часом до 23:00.",
         "Цифровизация, онлайн-платформы, AutoCAD, ноутбуки. Больше автономии в быту, свободный доступ."),
        ("Трудоустройство",
         "Обязательное государственное распределение на 3 года после выпуска по всей стране.",
         "Самостоятельный поиск работы на рынке труда, стажировки, свободный выбор локации."),
    ]

screen comparison_table():
    zorder 10
    frame:
        xalign 0.5
        ypos 15
        padding (20, 12)
        background Solid("#000000dd")
        vbox:
            spacing 8
            for i, row in enumerate(TABLE_ROWS):
                hbox:
                    spacing 8
                    frame:
                        xsize 260
                        background Solid("#ffffff30" if i == 0 else "#ffffff1a")
                        padding (12, 8)
                        text row[0] size 22 bold True color "#ffd54f"
                    frame:
                        xsize 740
                        background Solid("#ffffff30" if i == 0 else "#ffffff1a")
                        padding (12, 8)
                        text row[1] size 21 bold (i == 0)
                    frame:
                        xsize 740
                        background Solid("#ffffff30" if i == 0 else "#ffffff1a")
                        padding (12, 8)
                        text row[2] size 21 bold (i == 0)


## ============================================================================
##  ИГРА
## ============================================================================

label start:

    $ breakfast = ""
    $ lunch = ""
    $ coins_left = 50
    jump act1


## ----------------------------------------------------------------------------
##  АКТ 1. Ночной дедлайн и великий тупик
## ----------------------------------------------------------------------------

label act1:

    scene black
    centered "{size=+30}АКТ 1{/size}\n\nНочной дедлайн и великий тупик"

    scene bg room_modern_night with fade
    $ bgm("calm_night", fadein=2.0)

    "Современная комната Марины. 02:40 ночи."
    "Стол завален распечатками, на ноутбуке светится пустая презентация."


    show marina one at pos_speaker
    with quick
    m "Завтра в десять утра защита проекта по «Основам российской государственности», а у нас конь не валялся!"

    hide marina
    show alya one at pos_speaker
    with quick
    a "Не ори. Мы собрали кучу фактов. Вот, смотри: ВУЗы, ССО, картошка, Ленинская стипендия..."

    hide alya
    show vika one at pos_speaker
    with quick
    v "И что с этим делать? Это просто список цифр и дат. Как их связать? Что из этого реально важно, а что миф?"

    hide vika
    show yulya one at pos_speaker
    with quick
    yu "Я вообще запуталась. Моя бабушка твердит, что они только и делали, что учились, а дедушка — что они на картошке все выходные пили чай у костра и пели песни под гитару."

    hide yulya
    show marina one at pos_speaker
    with quick
    m "Мы обзвонили всех мам, пап, бабушек, осталось только Ленину телеграмму отправить. Никакой конкретики, одни эмоции! Гугл выдаёт сухие статьи. Как показать живую систему?"

    hide marina
    show vika one at pos_speaker
    with quick
    v "Нам нужен сквозной сюжет. Сравнение с нашей жизнью. Но откуда взять детали быта?"

    hide vika
    with quick
    "Все замолкают. Часы на ноутбуке показывают 02:58."

    show yulya one at pos_speaker
    with quick
    yu "Девочки, у меня глаза закрываются... Давайте пять минут перерыв..."

    hide yulya
    show alya one at pos_speaker
    with quick
    a "Карандаш... Где мой механический карандаш?.."

    hide alya
    with quick
    "Голова Али опускается на конспекты. Одна за другой девочки роняют головы на стол."

    $ bgm(None, fadeout=2.0)
    $ sfx("radio_static", loop=True)
    scene black with Dissolve(2.5)
    pause 1.5
    $ sfx_stop(1.0)

    jump act2
