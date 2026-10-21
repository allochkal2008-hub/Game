## ----------------------------------------------------------------------------
##  НАСТРОЙКИ
## ----------------------------------------------------------------------------

define SPRITE_ZOOM = 0.8      # общий масштаб спрайтов (1.0 = исходный размер)
define MUSIC_ON = True        # фоновая музыка: True — включена, False — выключена


## --- Персонажи --------------------------------------------------------------
define m  = Character("Марина", color="#B22222")
define a  = Character("Аля", color="#B22222")
define v  = Character("Вика", color="#B22222")
define yu = Character("Юля", color="#B22222")
define s  = Character("Серёга", color="#B22222")
define t  = Character("Тамара Ивановна", color="#B22222")

## --- Переходы ---------------------------------------------------------------
define flash = Fade(0.1, 0.0, 0.8, color="#ffffff")
define slow_fade = Fade(1.0, 0.5, 1.0)
define quick = Dissolve(0.2)       # смена говорящего

## --- Позиция спрайта ---------------------------------------------------------
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


## ----------------------------------------------------------------------------
##  АКТ 2. Утро в 1985-м. Инженерный быт
## ----------------------------------------------------------------------------

label act2:

    centered "{size=+30}АКТ 2{/size}\n\nУтро в 1985-м. Инженерный быт"

    scene bg dorm_1985 at retro with fade
    $ bgm("dorm_1985", fadein=2.0)

    "Комната советского общежития. На стенах — плакаты рок-групп и календарь за 1985 год."
    "На столе нет ноутбуков — только деревянные линейки и огромные листы бумаги."


    show marina u_surprised at pos_speaker
    with quick
    m "{i}(Резко вскакивает){/i} Ай! Кто выключил мой будильник на смартфоне?!"

    hide marina
    show alya u_surprised at pos_speaker
    with quick
    a "{i}(Трёт глаза){/i} Какой смартфон? Марина, ты где взяла это жуткое колючее одеяло?"

    hide alya
    show yulya u_surprised at pos_speaker
    with quick
    yu "Девочки... А где наши обои со звёздами? И почему нас четверо на двухъярусных железных кроватях?"

    hide yulya
    show vika u_surprised at pos_speaker
    with quick
    v "{i}(Подбегает к столу){/i} Так. Тише. Смотрите на календарь. «Октябрь 1985 года». Это шутка?"

    hide vika
    show marina u_thinking at pos_speaker
    with quick
    m "Посмотрите на этот стол! Что это за гигантские пластиковые трубы?"

    hide marina
    with quick
    "В комнату заглядывает парень в клетчатой рубашке с весёлой улыбкой. Это Серёга."

    show serega happy at pos_speaker
    with quick
    s "О, девчонки, проснулись! А чего тубусы на пол побросали? Архитектуру к первой паре не дочертили?"

    ## --- добавлено: Серёга ведёт себя так, будто знает их сто лет ---
    hide serega
    with quick
    "Серёга говорит так, будто они знакомы сто лет. Девочки переглядываются."

    show alya u_thinking at pos_speaker
    with quick
    a "Ту... тубусы? Это вот эти трубы?"

    hide alya
    show serega normal at pos_speaker
    with quick
    s "Ну да. Чертежи ватманские внутри. И не забудьте свои готовальни, без циркуля на начерталке делать нечего. Да, и логарифмические линейки захватите, калькуляторы на весь поток — дефицит."

    hide serega
    show vika u_surprised at pos_speaker
    with quick
    v "{i}(Шёпотом Але){/i} Готовальни? Логарифмические линейки? Они чертят руками без AutoCAD?!"

    hide vika
    show marina u_normal at pos_speaker
    with quick
    m "{i}(Шёпотом){/i} Похоже на то. Девчата, подыграем. Нам же нужны были факты."

    hide marina
    show yulya u_thinking at pos_speaker
    with quick
    yu "Серёж, а... чем тут обычно завтракают? Мы спросонья ничего не соображаем."

    hide yulya
    show serega happy at pos_speaker
    with quick
    s "Да как всегда! Либо по-быстрому в комнате, либо в буфет бежать. На плите чайник закипел, там девчонки делятся запасами."

    hide serega
    with quick
    "Что взять на завтрак?"

    menu:
        "Докторская колбаса с батоном (быстро, сытно, классика общаги)":
            $ breakfast = "kolbasa"

            "Девочки режут батон прямо на чертёжных листах и делают бутерброды с докторской колбасой."
            show marina u_happy at pos_speaker
            with quick
            m "Колбаса с батоном — и это завтрак? Вкусно, между прочим!"
            hide marina
            show serega happy at pos_speaker
            with quick
            s "Настоящий общажный завтрак! Быстро, сытно — и бегом на пару."

        "Плавленый сырок «Дружба» и чай (экономно, традиционно)":
            $ breakfast = "syrok"

            hide serega
            with quick
            "Серёга приносит с плиты чайник. Девочки разворачивают плавленые сырки и разливают чай по гранёным стаканам."
            show vika u_thinking at pos_speaker
            with quick
            v "Сырок «Дружба» и чай... Экономно."
            hide vika
            show serega happy at pos_speaker
            with quick
            s "По-студенчески: дёшево и привычно. Пей, пока горячий!"


    hide serega
    with quick
    "Аля торопливо шарит по карманам и по столу."
    show alya u_thinking at pos_speaker
    with quick
    a "Мой карандаш... Куда он делся?"
    hide alya
    show serega normal at pos_speaker
    with quick
    s "Опять потеряла? Держи, у меня запасной — простой, деревянный. Механических у нас не водится."
    hide serega
    show alya u_surprised at pos_speaker
    with quick
    a "{i}(Вертит карандаш в руках){/i} Спасибо... Он же даже не выдвигается!"
    hide alya
    show serega normal at pos_speaker
    with quick
    s "Так его перочинным ножом точат! Всё, хватит копаться, побежали!"

    hide serega
    with quick
    "Девочки выбегают на улицу вслед за Серёгой. На улице прохладно, туман."

    scene bg street_1985 at retro with fade

    show yulya u_surprised at pos_speaker
    with quick
    yu "Ого... Ни одной иномарки. Одни круглые автобусы и «Жигули»."

    hide yulya
    show vika u_thinking at pos_speaker
    with quick
    v "Глядите, люди стоят у киоска и читают бумажные газеты «Правда» и «Труд». Никто не залипает в экраны."

    hide vika
    show serega happy at pos_speaker
    with quick
    s "Наш ЛиАЗ подъехал! Шевелитесь, а то штурмом брать придётся!"

    ## --- Автобус ---
    hide serega
    with quick
    "Они затискиваются в жёлтый ЛиАЗ-677. Автобус громко звенит бутылками на ухабах."

    scene bg bus_1985 at retro with fade
    $ sfx("bus_bells", loop=True)
    with hpunch

    show marina u_surprised at pos_speaker
    with quick
    m "{i}(Держится за поручень){/i} Ого, как его трясёт! А где тут валидатор? Как платить?"

    hide marina
    show serega normal at pos_speaker
    with quick
    s "Какой валидатор? Вон касса механическая. Бросаешь 5 копеек в щель и сама крутишь ручку, чтобы оторвать билет. Всё на честности, девчонки."

    hide serega
    show alya u_surprised at pos_speaker
    with quick
    a "Пять копеек... Проезд стоит пять копеек?!"

    with vpunch
    hide alya
    show serega happy at pos_speaker
    with quick
    s "Ну да. А сколько, по-вашему? Рубль, что ли? Ладно, выходим, вон наш политех!"

    $ sfx_stop(0.5)
    jump act3


## ----------------------------------------------------------------------------
##  АКТ 3. День в ВУЗе. Идеология и обед за копейки
## ----------------------------------------------------------------------------

label act3:

    centered "{size=+30}АКТ 3{/size}\n\nДень в ВУЗе. Идеология и обед за копейки"

    scene bg polytech_hall at retro with fade

    "Коридоры политехнического института. На стенах — лозунги «Учиться, учиться и учиться!»."
    "Вокруг полно студентов в строгих костюмах и скромных платьях."

    ## --- Лекция ---
    scene bg lecture_hall at retro with fade
    "Они заходят в огромную лекционную аудиторию. На доске написано: «История КПСС. Тема: Развитой социализм»."


    show vika u_thinking at pos_speaker
    with quick
    v "{i}(Тихо){/i} История КПСС... Это как наши «Основы государственности», только с уклоном в партию?"

    hide vika
    show alya u_normal at pos_speaker
    with quick
    a "Точно. Смотри, профессор за каждый прогул грозится деканские выговоры выписать. Никакого свободного посещения."

    hide alya
    show yulya u_sleepy at pos_speaker
    with quick
    yu "И никаких презентаций в PowerPoint. Только мел, огромная доска и монотонный голос преподавателя. Где же мой DeepSeek..?"

    ## --- добавлено: Вика начинает записывать ---
    hide yulya
    with quick
    "Вика достаёт блокнот и украдкой записывает: «посещаемость — строго, доска и мел, обязательная История КПСС»."

    ## --- Столовая ---
    "После двух пар лекций девочки вместе с Серёгой идут в студенческую столовую. Шум, звон тарелок, запах выпечки."

    scene bg canteen at retro with fade
    $ sfx("canteen_noise", loop=True)

    show marina u_surprised at pos_speaker
    with quick
    m "Так, у меня в кармане куртки нашлась советская монета — ровно 50 копеек. На что хватит?"

    hide marina
    with quick
    "Что выбрать на обед?"

    menu:
        "Гороховый суп, котлета с пюре и компот (35 копеек — сытный студенческий обед)":
            $ lunch = "soup"
            $ coins_left = 15

            "Девочки берут подносы и садятся за липкий деревянный стол."
            show marina u_happy at pos_speaker
            with quick
            m "Сдача — 15 копеек. Это же целых три поездки на автобусе!"

        "Борщ, отварные сосиски и пирожок с капустой (48 копеек — роскошно, впритык)":
            $ lunch = "borsch"
            $ coins_left = 2

            hide marina
            with quick
            "Девочки берут подносы и садятся за липкий деревянный стол."
            show marina u_happy at pos_speaker
            with quick
            m "Сдачи — две копейки. Впритык! Зато какой обед!"

    hide marina
    show vika u_thinking at pos_speaker
    with quick
    v "Слушай, Серёга, а если стипендия всего 40 рублей, то на столовую уходит приличная часть?"

    hide vika
    show serega normal at pos_speaker
    with quick
    s "Ну, если каждый день шиковать, то да. Но у нас многие повышенную получают — 50 рублей. А отличники — Ленинскую, целых 100 рублей! Это вообще бешеные деньги."

    hide serega
    show marina u_thinking2 at pos_speaker
    with quick
    m "А если не хватает?"

    hide marina
    show serega happy at pos_speaker
    with quick
    s "Тогда летом все в ССО — Студенческие строительные отряды. Мы в прошлом году коровники в Сибири строили. За два месяца — 600 рублей чистыми! Я себе магнитофон купил и джинсы у фарцовщиков."

    hide serega
    show alya u_surprised at pos_speaker
    with quick
    a "Шестьсот рублей за лето?! Это же несколько инженерных зарплат!"

    hide alya
    show serega normal at pos_speaker
    with quick
    s "Ну так в ССО пахать надо от зари до зари. Зато романтика: форма с нашивками, песни у костра. Это вам не осенняя картошка."

    hide serega
    show yulya u_thinking2 at pos_speaker
    with quick
    yu "А что не так с картошкой?"

    hide yulya
    show serega normal at pos_speaker
    with quick
    s "Да ну, в сентябре вместо учёбы весь институт на три недели в колхоз отправляют. Грязь, дождь, собираешь вёдрами эту картошку. Хотя весело, конечно, пары-то отменяют!"

    hide serega
    show vika u_happy at pos_speaker
    with quick
    v "{i}(Записывает в блокнот){/i} Так, отмена пар ради уборки урожая... Записала."

    hide vika
    show serega serious at pos_speaker
    with quick
    s "Главное — институт окончить нормально. А то распределение пугает. Куда Родина пошлёт на 3 года отрабатывать — туда и поедешь. Хоть на Сахалин."

    hide serega
    show marina u_surprised at pos_speaker
    with quick
    m "{i}(Шёпотом Але){/i} Распределение? То есть они не сами ищут работу на HeadHunter?"

    hide marina
    show alya u_thinking at pos_speaker
    with quick
    a "{i}(Шёпотом){/i} Кажется, государство гарантирует работу, но отнимает право выбора."

    ## --- добавлено: мостик к вечеру ---
    hide alya
    show serega happy at pos_speaker
    with quick
    s "Ладно, хватит о грустном! Вечером в общаге все собираются — пошли с нами, расскажете, откуда вы такие странные."

    $ sfx_stop(1.0)
    jump act4


## ----------------------------------------------------------------------------
##  АКТ 4. Вечер в общаге. Перестройка и финал
## ----------------------------------------------------------------------------

label act4:

    centered "{size=+30}АКТ 4{/size}\n\nВечер в общаге. Перестройка и финал"

    scene bg dorm_corridor_evening at retro with fade
    $ bgm("tape_music", fadein=2.0)

    "Общежитие, вечер. В коридоре пахнет жареной картошкой."
    "Из чьей-то комнаты тихо играет кассетный магнитофон: «Перемен требуют наши сердца...»."


    show yulya u_happy at pos_speaker
    with quick
    yu "Ребята в соседней комнате чертят, а девчонки на кухне одну сковородку картошки на весь этаж делят. Коллективизм!"

    ## --- добавлено: callback на выбор обеда ---
    if lunch == "soup":
        show yulya u_happy at pos_speaker
        yu "А я всё ещё вспоминаю тот гороховый суп за 35 копеек. Вот это я понимаю — обед!"
    else:
        show yulya u_happy at pos_speaker
        yu "А я всё ещё вспоминаю тот борщ с пирожком за 48 копеек. Роскошь — но оно того стоило!"

    hide yulya
    show marina u_thinking at pos_speaker
    with quick
    m "Смотрите, тут из развлечений — только гитара и настольный теннис в фойе. И никаких чатов в телеграме."

    hide marina
    show alya u_happy at pos_speaker
    with quick
    a "Зато люди общаются вживую, а не сидят по углам в наушниках. А мне бы сейчас и хотелось музыку послушать…"

    hide alya
    show vika u_happy at pos_speaker
    with quick
    v "Я собрала идеальный материал для проекта. Смотрите, какая контрастная таблица получается!"

    hide vika
    with quick
    "Вдруг в коридоре раздаётся грозный голос коменданта."

    t "Десять минут до одиннадцати! Гости, на выход! Закрываю общежитие!"

    show marina u_surprised at pos_speaker
    with quick
    m "Ой, Серёга, нам пора! А то запрёт, и кукуй на улице."

    hide marina
    show serega happy at pos_speaker
    with quick
    s "Да ладно вам, Тамара Ивановна строгая, но отходчивая. Ладно, девчонки, удачи с вашей начерталкой!"

    ## --- добавлено: тёплое прощание ---
    hide serega
    show alya u_happy at pos_speaker
    with quick
    a "Серёж, спасибо за всё. Правда."
    hide alya
    show serega happy at pos_speaker
    with quick
    s "Да пустяки! Заходите ещё — у нас тут всегда весело."

    ## --- Возвращение ---
    scene bg dorm_1985 at retro with fade
    "Девочки забегают в свою комнату."

    $ sfx("clock_chime")
    "Часы бьют 23:00."
    $ sfx("door_lock")
    "Дверь общаги закрывается с тяжёлым металлическим щелчком."
    "Комната начинает кружиться."

    $ bgm(None, fadeout=0.5)
    scene black with flash
    $ sfx("alarm", loop=True)
    pause 1.0

    jump ending


## ----------------------------------------------------------------------------
##  ФИНАЛ
## ----------------------------------------------------------------------------

label ending:

    scene bg room_modern_morning with flash

    "Современная комната Марины. Солнечное утро. На экране ноутбука открыта пустая презентация."


    show marina surprised at pos_speaker
    with quick
    m "{i}(Просыпается на клавиатуре){/i} А-а-а! Комендантский час закончился?!"

    $ sfx_stop(0.5)

    hide marina
    show alya surprised at pos_speaker
    with quick
    a "{i}(Смотрит на часы){/i} Девочки, девять утра!"

    ## --- добавлено: карандаш из 1985 ---
    show alya thinking at pos_speaker
    a "Подождите... У меня в руке карандаш. Простой, деревянный. Серёгин."

    hide alya
    show yulya surprised at pos_speaker
    with quick
    yu "Погодите... Это был сон? Но посмотрите на экран моего ноутбука!"

    hide yulya
    with quick
    "Все смотрят на экран. Там набрана структурированная таблица сравнения."

    $ bgm("final_theme", fadein=2.0)
    show screen comparison_table

    show marina happy at pos_speaker
    with quick
    m "Она реальная! Вика, ты гений, ты успела всё записать во сне!"

    hide marina
    show vika happy at pos_speaker
    with quick
    v "Я не знаю как, но у нас есть идеальный проект. Мы не просто покажем цифры, мы расскажем историю!"

    hide vika
    show alya happy at pos_speaker
    with quick
    a "Собираемся, девочки. Пора получить наш заслуженный зачёт по Основам государственности!"

    hide alya
    show yulya happy at pos_speaker
    with quick
    yu "Должны получить не меньше десятки!"

    hide yulya
    with quick

    hide screen comparison_table
    scene black with slow_fade
    centered "{size=+30}КОНЕЦ{/size}"

    $ bgm(None, fadeout=3.0)
    return
