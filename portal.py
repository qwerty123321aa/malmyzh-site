"""Редакционные страницы и общие компоненты статического портала."""
import html
import json
from html.parser import HTMLParser

BASE = 'https://qwerty123321aa.github.io/malmyzh-site/'
UPDATED = '6 ноября 2026'
SECTIONS = [
 ('about','Геология','Тип месторождения, минералы и строение руд.','malmyzh-excavator.jpg'),
 ('location','Карта','Малмыж и географические ориентиры Приамурья.','malmyzh-fleet.jpg'),
 ('resources','Запасы и ресурсы','Как читать оценки меди, золота и серебра.','malmyzh-rock.jpg'),
 ('production','Добыча и переработка','Путь руды от карьера до концентрата.','malmyzh-loading.jpg'),
 ('importance','Экономика','Рабочие места и производственные связи.','malmyzh-drilling.jpg'),
 ('ecology','Экология','Вода, воздух, земли и вопросы контроля.','malmyzh-fleet.jpg'),
 ('history','История проекта','Документированные этапы освоения.','malmyzh-winter.jpg'),
 ('gallery','Фотогалерея','Документальные кадры с площадки.','malmyzh-night.jpg'),
 ('sources','Источники','Документы, публикации и происхождение фотографий.','malmyzh-excavator.jpg')]
EVENTS = [
 ('2018','Исходная оценка','В публикации Роснедр приведена база сравнения: 5,156 млн тонн меди и 278 тонн золота.',1),
 ('22 сентября 2021','Новая оценка ГКЗ','Утверждены 8,3 млн тонн меди, 347,4 тонны золота и 1 676 тонн серебра. Протокол № 6749.',1),
 ('2024','Первая очередь фабрики','Год запуска первой очереди указан на официальном сайте оператора. Это корпоративное сообщение.',2),
 ('2025','Обсуждение документации','В уведомлении Росприроднадзора названы фабрика, хвостовое хозяйство и оборотное водоснабжение.',3)]


def install(g):
    cite, heading, section, note, photo = (g[k] for k in ('cite','heading','section','note','photo'))
    old = dict(g['PAGES'])

    def cards():
        return '<div class="topic-grid portal-topics">'+''.join(f'<article class="topic"><a href="{slug}.html"><img src="assets/{image.removesuffix(".jpg")}.webp" width="640" height="480" loading="lazy" alt="{g["PHOTO_INFO"][image][1]}"><h3>{title} ↗</h3></a><p>{desc}</p><small>Фото: <a href="sources.html#source-9">АО «Тех Взрыв Инвест»</a></small></article>' for slug,title,desc,image in SECTIONS)+'</div>'

    def home():
        return f'''<section class="portal-hero"><img class="hero-image" src="assets/malmyzh-loading.webp" width="1024" height="768" alt="Экскаватор и самосвал на площадке Малмыжского проекта" fetchpriority="high"><div class="portal-hero-copy"><span class="eyebrow">Независимый информационно-образовательный проект</span><h1>Малмыжское<br>месторождение</h1><p>Медь. Золото. Приамурье.</p><p class="hero-description">Геология, промышленное освоение и природа Хабаровского края — в документах, фотографиях и данных.</p><div class="hero-actions">{g['link']('about.html','Исследовать месторождение')}{g['link']('location.html','Изучить карту','quiet-link')}</div></div><div class="hero-credit">Фото: <a href="sources.html#source-9">АО «Тех Взрыв Инвест»</a> · Дата съёмки не указана</div></section>
        <section class="facts-strip dark-facts" aria-label="Оценка запасов ГКЗ 2021 года">{g['stat']('8,3 <i>млн т</i>','медь', 'Запасы · 2021 · Роснедра')}{g['stat']('347,4 <i>т</i>','золото','Запасы · 2021 · Роснедра')}{g['stat']('1 676 <i>т</i>','серебро','Запасы · 2021 · Роснедра')}<div class="stat-note">Государственная оценка от 22.09.2021.<br>Масса металла в недрах, не годовая добыча.{cite(1)}</div></section>
        <section class="intro-row"><h2>Большая геология<br>Дальнего Востока</h2><p>Малмыж — золото-медно-порфировое месторождение в Нанайском и Амурском районах. Здесь добывают руду и получают медный концентрат.{cite(1,2)}</p></section>
        {cards()}{g['reserves_chart']()}
        <section class="editorial-links"><article><span class="eyebrow">Природа и промышленность</span><h2>Что важно знать об экологии</h2><p>Возможные риски, предусмотренные меры и данные, которых не хватает для выводов.</p>{g['link']('ecology.html','Разобраться в вопросе','text-link')}</article><article><span class="eyebrow">Обновлено 6 ноября 2026</span><h2>Новая версия проекта</h2><p>Добавлены история, поиск, галерея и отдельная страница технологии.</p>{g['link']('updates.html','Обновления материалов','text-link')}</article></section>'''

    def geology():
        diagram='''<figure class="geo-figure"><svg viewBox="0 0 1000 430" role="img" aria-label="Учебная схема: вмещающие породы, интрузия, зона изменения и рудные прожилки"><rect width="1000" height="430" fill="#e4e3db"/><path d="M0 75Q200 30 400 80T1000 60V430H0Z" fill="#c8ccc2"/><path d="M180 430L310 200Q500 80 680 210L840 430Z" fill="#a5b19e"/><path d="M320 430L390 255Q500 170 610 260L680 430Z" fill="#526c58"/><path d="M370 400L450 270L520 315L590 230M415 410L520 335L610 380M480 425L510 300" fill="none" stroke="#d7a35c" stroke-width="9"/><path d="M85 100L180 430M870 100L760 420" stroke="#777d78" stroke-width="3" stroke-dasharray="8 8"/><g fill="#172321" font-family="Arial" font-size="21"><text x="40" y="45">Вмещающие породы</text><text x="40" y="190">Геологические структуры</text><text x="650" y="160">Зона изменения пород</text><text x="680" y="320">Рудные прожилки</text><text x="420" y="395" fill="white">Интрузия</text></g><path d="M700 165L650 220M740 315L570 300" stroke="#172321" fill="none"/></svg><figcaption>Концептуальная модель медно-порфирового месторождения по USGS [7]. Не фактический разрез Малмыжа; масштаб, глубины и границы условные.</figcaption></figure>'''
        minerals='<section class="prose"><h2>Минералы руды</h2><p>Роснедра указывают пирит и халькопирит в составе руд Малмыжа.'+cite(1)+'</p></section><div class="mineral-grid"><article><span class="formula">CuFeS₂</span><h3>Халькопирит</h3><p>Сульфид меди и железа. Один из основных медных минералов порфировых руд.</p></article><article><span class="formula">FeS₂</span><h3>Пирит</h3><p>Сульфид железа. Его присутствие важно при изучении поведения сульфидных пород в воде и воздухе.</p></article></div><p class="muted">Формулы — общие минералогические сведения. На фотографиях горной массы отдельные минералы не идентифицированы; снимки образцов без подтверждённого происхождения не представлены.</p>'
        return old['about'][1]()+section('Как устроена порфировая система', '<p>Порфировые системы связаны с магматическими интрузиями и движением горячих растворов. Они формируют прожилки, вкрапления и зоны изменения пород. Ниже показана общая учебная модель.'+cite(7)+'</p>')+diagram+minerals

    def production():
        stages=[('Карьер','Разработка и извлечение руды открытым способом.','malmyzh-excavator.jpg'),('Перевозка','Горную массу доставляют к пунктам подготовки.','malmyzh-fleet.jpg'),('Дробление','Крупные куски руды уменьшают до размера, пригодного для измельчения.',None),('Измельчение','Освобождают полезные минералы от срастаний с породой.',None),('Обогащение','Разделяют минеральные компоненты и повышают содержание полезных металлов.',None),('Концентрат','Продукт направляют на дальнейшую переработку; остатки образуют хвосты.',None)]
        return heading('Производство','От руды к концентрату','Добыча и обогащение — последовательные этапы работы с минеральным сырьём.')+note('Схема ниже объясняет общий процесс по модели USGS. Это не технологический регламент Малмыжского ГОКа. Открытый способ и медный концентрат подтверждены отдельными источниками.'+cite(1,2,7))+'<div class="stage-grid">'+''.join('<article class="stage">'+(f'<img src="assets/{im.removesuffix(".jpg")}.webp" alt="{g["PHOTO_INFO"][im][1]}" loading="lazy"><small>Фото: АО «Тех Взрыв Инвест» '+cite(9)+'</small>' if im else f'<div class="stage-symbol" aria-hidden="true">{symbol}</div>')+f'<h2>{title}</h2><p>{desc}</p></article>' for (title,desc,im),symbol in zip(stages,['','', '◆ → ◇','◇ → ⋅','⋅ → Cu','Cu ↗']))+'</div>'+section('Где заканчивается работа ГОКа','<p>Оператор специализируется на выпуске медного концентрата. Концентрат — промежуточный продукт, который требует дальнейшей металлургической переработки.'+cite(2)+'</p>')+g['photo_gallery'](['malmyzh-loading.jpg','malmyzh-rock.jpg'],'Реальные кадры горных работ')

    def resources():
        glossary=[('Запасы','Учтённая по установленным правилам часть минерального сырья с изученными условиями залегания.'),('Ресурсы','Более широкое представление о минеральном потенциале; степень изученности и методика оценки должны быть названы.'),('Прогнозные ресурсы','Оценка возможного минерального потенциала, требующая дальнейшего изучения.'),('Добыча','Количество извлечённой руды или металла за определённый период.'),('Мощность','Расчётная способность производства. Не равна подтверждённому выпуску.')]
        return old['resources'][1]()+section('Как читать цифры','<p>Единицы, период и метод оценки важны так же, как само значение.</p>')+g['reserves_chart']()+'<section class="prose"><h2>Термины без путаницы</h2>'+''.join(f'<details><summary>{t}</summary><p>{d}</p></details>' for t,d in glossary)+'</section><p><a href="assets/statistics.csv" download>Скачать данные графиков CSV ↓</a></p>'

    def history():
        return heading('Хронология','История проекта','Выберите событие, чтобы прочитать его контекст и открыть документ.')+'<section class="timeline">'+''.join(f'<details {"open" if i==0 else ""}><summary><time>{date}</time><span>{title}</span></summary><p>{desc}{cite(src)}</p></details>' for i,(date,title,desc,src) in enumerate(EVENTS))+'</section>'+note('В шкалу включены только этапы с источниками в подборке. Дата открытия и полный календарь строительства не восстановлены предположениями.')+g['photo_gallery'](['malmyzh-winter.jpg','malmyzh-night.jpg'],'Фотохроника без вымышленных дат')

    def gallery():
        groups={'malmyzh-loading.jpg':'Карьер','malmyzh-excavator.jpg':'Карьер','malmyzh-rock.jpg':'Карьер','malmyzh-fleet.jpg':'Техника','malmyzh-drilling.jpg':'Техника','malmyzh-winter.jpg':'Зима','malmyzh-night.jpg':'Ночные работы'}
        return heading('Документальная съёмка','Малмыж в фотографиях','Семь кадров из галереи подрядчика. Даты съёмки и индивидуальный фотограф не указаны.')+'<label class="filter-label">Показать <select id="gallery-filter"><option value="">Все фотографии</option>'+''.join(f'<option>{s}</option>' for s in ['Карьер','Техника','Зима','Ночные работы'])+'</select></label><div class="photo-grid gallery-grid">'+''.join(f'<div data-gallery-category="{cat}">'+photo(f,g['PHOTO_INFO'][f][1],g['PHOTO_INFO'][f][0])+'</div>' for f,cat in groups.items())+'</div>'+section('Источники и права','<p>Источник всех семи снимков — галерея Малмыжского проекта АО «Тех Взрыв Инвест».'+cite(9)+'</p><p>Водяные знаки сохранены. Права остаются у правообладателей; свободная лицензия не заявляется. Изображения не доказывают экологическую безопасность или состояние предприятия на конкретную дату. Аэрофотографии, образцы минералов и независимые снимки природы с подтверждёнными условиями использования в подборке отсутствуют.</p>')

    def updates():
        return heading('Редакция','Обновления материалов','Здесь опубликованы изменения самого информационного проекта. Подтверждённые события предприятия собраны в истории.')+'<article class="update-entry"><span class="eyebrow">6 ноября 2026 · Обновление сайта</span><h2>Расширены материалы и навигация</h2><p>Добавлены страницы добычи, истории и фотогалереи, поиск по текстам, фильтрация источников и выгрузка данных. Сохранены исходные ссылки и подписи фотографий.</p><p>Геологические оценки остаются датированными 2021 годом. Проектные экологические меры обозначены отдельно от результатов измерений.</p><a href="sources.html">Проверить источники ↗</a></article><article class="update-entry"><span class="eyebrow">5 ноября 2026 · Фотоматериалы</span><h2>Добавлены документальные фотографии</h2><p>Включены семь кадров из первичной галереи подрядчика с подписями и ссылкой на происхождение.'+cite(9)+'</p><a href="gallery.html">Открыть галерею ↗</a></article>'

    def sources():
        text=old['sources'][1]()
        filters='<div class="filter-bar"><label>Поиск в источниках<input type="search" id="source-query" placeholder="Организация, документ, тема"></label><label>Категория<select id="source-filter"><option value="">Все категории</option><option value="state">Государственные документы</option><option value="science">Научные публикации</option><option value="company">Корпоративные материалы</option><option value="geology">Геологические сведения</option><option value="map">Картографические данные</option></select></label></div><p id="source-status" role="status"></p>'
        for s in g['SOURCES']:
            cat='state' if s['id'] in [1,3] else 'science' if s['id'] in [5,6,7,8] else 'company' if s['id'] in [2,4,9] else 'geology' if s['id']==10 else 'map'
            text=text.replace(f'class="source" id="source-{s["id"]}"',f'class="source" data-category="{cat}" id="source-{s["id"]}"')
        text=text.replace('<div class="sources-list">',filters+'<div class="sources-list">')
        text=text.replace('Шрифт <a href="https://fonts.google.com/specimen/Golos+Text">Golos Text</a> используется по <a href="assets/Golos-OFL.txt">SIL Open Font License</a> и хранится в проекте.','Шрифты Manrope и Inter хранятся в проекте и используются по SIL Open Font License. <a href="assets/font-licenses.txt">Лицензии шрифтов</a>. Карта — Leaflet, графики — Plotly; <a href="assets/vendor-licenses.txt">лицензии библиотек</a>.')
        return text

    def location():
        text=old['location'][1]()
        return text.replace('<section class="map-section">','<section class="map-section"><div id="leaflet-map" aria-label="Карта Приамурья" role="region"></div><p class="map-legend"><span>●</span> Приблизительная отметка месторождения · Границы лицензии не показаны</p><p class="muted">Масштабируйте карту и нажмите на отметку. Подложка и названия рек и населённых пунктов: OpenStreetMap. Альтернативная карта ниже доступна независимо от Leaflet.</p>')

    def search():
        return heading('Навигация','Поиск по сайту','Ищите минералы, географические названия, числовые показатели и документы.')+'<form id="search-form" role="search"><label for="search-input">Что найти</label><div class="search-row"><input id="search-input" type="search" name="q" placeholder="Например, медь, вода, 2021" autocomplete="off"><button class="button">Найти</button></div></form><p id="search-status" role="status">Введите запрос для поиска.</p><div id="search-results"></div><noscript><p>Для поиска нужен JavaScript. Все материалы доступны через меню разделов.</p></noscript>'

    def economy():
        return old['importance'][1]()+section('Инвестиции в историческом контексте', '<p>В сообщении Роснедр от 29 октября 2021 года бюджет проекта вместе с геологоразведкой оценивался в 248 млрд рублей. На 1 октября 2021 года сообщалось о вложении около 62 млрд рублей. Это исторические сведения из той публикации, а не текущая стоимость проекта или размер инвестиций за 2026 год.'+cite(1)+'</p>')+section('Мощность и фактический выпуск','<p>Официальный сайт оператора указывает производительность 104 млн тонн руды в год. Показатель приведён как заявленная мощность; фактический выпуск за календарный год требует отдельной производственной отчётности.'+cite(2)+'</p><p>Экспортные возможности и поступления в бюджет зависят от выпуска, условий реализации и налогообложения. В подборке нет проверенной годовой серии налогов и экспорта, поэтому количественная оценка этих эффектов не строится.</p>')

    def ecology():
        text=old['ecology'][1]()
        visuals=[('Вода','malmyzh-winter.jpg'),('Воздух','malmyzh-loading.jpg'),('Земли и растительность','malmyzh-fleet.jpg'),('Хвостохранилище','malmyzh-rock.jpg')]
        for title,file in visuals:
            text=text.replace('<article class="risk"><h3>'+title, '<article class="risk"><img src="assets/'+file.removesuffix('.jpg')+'.webp" alt="'+g['PHOTO_INFO'][file][1]+'" loading="lazy"><small>Контекст горных работ, не измерение воздействия. Фото: АО «Тех Взрыв Инвест» '+cite(9)+'</small><h3>'+title)
        return text

    pages={'index':('Главная',home),'about':('Геология Малмыжа',geology),'location':('Карта месторождения',location),'resources':('Запасы и ресурсы',resources),'production':('Добыча и переработка',production),'importance':('Значение для региона',economy),'ecology':('Экология Хабаровского края',ecology),'history':('История проекта',history),'gallery':('Фотогалерея',gallery),'updates':('Обновления материалов',updates),'sources':('Источники и достоверность',sources),'search':('Поиск по сайту',search)}
    descriptions={s:d for s,_,d,_ in SECTIONS}|{'index':'Геология, добыча, природа и экономика Малмыжского месторождения. Документальные фотографии, карта и проверяемые данные.','search':'Поиск по текстам, статистике и источникам Малмыжского проекта.','updates':'Редакционные обновления материалов о Малмыжском месторождении.'}

    def render(slug):
        title,body=pages[slug] if slug in pages else ('Страница не найдена',lambda:heading('404','Страница не найдена','Проверьте адрес или выберите раздел сайта.')+cards())
        nav=''.join(f'<a href="{s}.html"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in [('index','Главная'),('about','Геология'),('location','Карта'),('resources','Запасы'),('production','Добыча'),('ecology','Экология'),('sources','Источники')])
        more=''.join(f'<a href="{s}.html">{t}</a>' for s,t in [('importance','Экономика'),('history','История'),('gallery','Галерея'),('updates','Обновления')])
        desc=descriptions.get(slug,title+' — Малмыжское месторождение, Хабаровский край.')
        canonical=BASE+('' if slug=='index' else slug+'.html')
        content=body()
        # Современные копии фотографий сохраняют оригиналы и их водяные знаки.
        for filename in g['PHOTO_INFO']:
            content=content.replace('assets/'+filename,'assets/'+filename.removesuffix('.jpg')+'.webp')
        return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#172321"><title>{title} — Малмыж</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{title} — Малмыж"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}assets/malmyzh-loading.jpg"><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/editorial.css?v=portal-1"><link rel="stylesheet" href="assets/portal.css?v=portal-1"><script type="module" src="assets/portal.js?v=portal-1"></script><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'WebSite','name':'Малмыжское месторождение','url':BASE,'inLanguage':'ru','description':desc},ensure_ascii=False)}</script></head><body><a class="skip-link" href="#main">К содержанию</a><header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><span>Малмыж<small>МЕДЬ · ЗОЛОТО · ПРИАМУРЬЕ</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" type="button">Меню ☰</button><nav id="site-nav" aria-label="Основная навигация">{nav}<details class="more-nav"><summary>Ещё</summary><div>{more}</div></details></nav><a class="header-sources" href="search.html" aria-label="Поиск по сайту">Поиск ⌕</a></div></header><main id="main" class="container {'home' if slug=='index' else ''}">{'' if slug=='index' else '<nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span>/</span><span>'+title+'</span></nav>'}{content}</main><dialog id="photo-dialog" aria-label="Просмотр фотографий"><div class="dialog-toolbar"><button type="button" data-prev aria-label="Предыдущее фото">←</button><button type="button" data-next aria-label="Следующее фото">→</button><button type="button" data-fullscreen>На весь экран</button><button class="dialog-close" type="button">Закрыть ×</button></div><img alt="Фотография месторождения"><p></p></dialog><footer class="site-footer"><div class="container footer-inner"><div><a class="footer-brand" href="index.html">Малмыж</a><p>Независимый информационно-образовательный проект.<br>Геология, производство и природа Хабаровского края.</p></div><div class="footer-links">{more}<a href="sources.html">Источники</a></div><div><p>Обновление сайта: {UPDATED}<br>Фактические материалы: проверка 5 ноября 2026<br>Неофициальный сайт</p></div></div></footer></body></html>'''

    g['PAGES']=pages
    g['render']=render


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(); self.text=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']:self.skip+=1
    def handle_endtag(self,tag):
        if tag in ['script','style']:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.text.append(data)


def build_extra(destination,pages,render):
    records=[]
    for slug,(title,body) in pages.items():
        parser=TextExtractor();parser.feed(body())
        records.append({'title':title,'url':slug+'.html','category':title,'text':' '.join(' '.join(parser.text).split())})
    (destination/'assets/search-index.json').write_text(json.dumps(records,ensure_ascii=False),encoding='utf-8')
    (destination/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{"" if s=="index" else s+".html"}</loc><lastmod>2026-11-06</lastmod></url>' for s in pages)+'</urlset>',encoding='utf-8')
    (destination/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    (destination/'404.html').write_text(render('404'),encoding='utf-8')
