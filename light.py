"""Светлая редакционная версия. Надстройка сохраняет прежние URL и материалы."""
import html
import re
import json
from pathlib import Path
MEDIA = json.loads((Path(__file__).parent / "assets/media-catalog.json").read_text())
from light_content import HISTORY, ARTICLES


def install(g):
    pages=g['PAGES'];previous=dict(pages);base_render=g['render']
    cite,heading,section,photo=(g[k] for k in ('cite','heading','section','photo'))

    def figure(file,title=None,source=9):
        if file in MEDIA:
            m=MEDIA[file]
            return f'<figure class="photo"><button class="photo-open" type="button" data-photo="assets/{file}" aria-label="Увеличить: {html.escape(m["alt"])}"><img src="assets/{file}" alt="{html.escape(m["alt"])}" loading="lazy"><span class="zoom-hint" aria-hidden="true">Увеличить</span></button><figcaption><strong>{m["title"]}</strong><span>Фото: <a href="{m["page"]}" target="_blank" rel="noopener">{m["credit"]}</a>. {m["note"]}{cite(m["source"])}</span></figcaption></figure>'
        if file=='operator-specialist.webp':
            return '<figure class="photo"><button class="photo-open" data-photo="assets/operator-specialist.webp" aria-label="Увеличить иллюстрацию с сайта оператора"><img src="assets/operator-specialist.webp" alt="Специалист с рацией в производственном помещении, изображение с сайта оператора" loading="lazy"></button><figcaption><strong>'+title+'</strong>Источник: <a href="https://amurminerals.ru/">«Амур Минералс»</a>. Автор и дата не указаны. Место съёмки отдельно не подтверждено.'+cite(2)+'</figcaption></figure>'
        original=file.replace('.webp','.jpg')
        return photo(original,g['PHOTO_INFO'].get(original,('',title))[1],title,source=source)

    def statistic(number,unit,label,explanation,src=1):
        return f'<article class="big-stat"><strong><span data-count="{number}" data-final="{number.replace(".",",")}">{number.replace(".",",")}</span><small>{unit}</small></strong><h3>{label}</h3><p>{explanation}{cite(src)}</p></article>'

    def home():
        return f'''<section class="museum-hero"><div class="museum-copy"><h1>История,<br>скрытая в камне</h1><p>Исследуйте Малмыжское месторождение — от геологии до производства.</p>{g['link']('about.html','Начать исследование')}</div><div class="mineral-stage"><div class="mineral-space"><img id="museum-mineral" src="assets/mineral-museum.png" alt="Художественная иллюстрация минерализованной породы" fetchpriority="high"><span class="mineral-label">Порода и минерализация</span></div><label class="mineral-control">Поверните иллюстрацию<input id="mineral-turn" type="range" min="-25" max="25" value="0" aria-label="Поворот иллюстрации минерала"></label></div></section><section class="museum-landscape"><div><h2>От поверхности —<br>к недрам</h2><p>Геология · Люди · Природа</p></div><img src="assets/museum-landscape.png" alt="Художественная иллюстрация ландшафта и горных пород"></section>
        <nav class="chapter-links" aria-label="Темы проекта"><a href="location.html">На карте <span>↗</span></a><a href="resources.html">В недрах <span>↗</span></a><a href="production.html">В производстве <span>↗</span></a><a href="ecology.html">В природе <span>↗</span></a></nav>
        <section class="light-stats" aria-label="Запасы по государственной оценке 2021 года">{statistic('8.3','млн т','Медь','Запасы · ГКЗ, 22.09.2021')}{statistic('347.4','т','Золото','Запасы · ГКЗ, 22.09.2021')}{statistic('1676','т','Серебро','Запасы · ГКЗ, 22.09.2021')}</section><p class="stat-footnote">Масса металла, учтённого в недрах. Не ежегодная добыча и не объём готовой продукции.</p>
        <section class="editorial-intro"><span class="eyebrow">О месторождении</span><h2>Большой объём породы.<br>Ценные минералы внутри.</h2><div><p>Малмыж относится к золото-медно-порфировым месторождениям. Полезные минералы распределены в породе: их нужно найти, изучить и отделить при переработке.{cite(1,7)}</p><p>Месторождение находится в Амурском и Нанайском районах. За геологическими цифрами стоят инженерные решения, труд специалистов и ответственность перед природой Приамурья.{cite(1)}</p>{g['link']('location.html','Найти на карте','text-link')}</div></section>
        <section class="feature-pair"><article class="feature-main"><a href="about.html"><img src="assets/malmyzh-rock.webp" alt="Горная порода на рабочей площадке" loading="lazy"><h2>Понять геологию ↗</h2></a><p>Порфировая система, минералы и методы исследования.</p><small>Фото: <a href="sources.html#source-9">АО «Тех Взрыв Инвест»</a></small></article><article class="feature-side"><span class="eyebrow">Запасы и ресурсы</span><div class="metal-art"><span class="metal-orbit copper">Cu<small>Медь</small></span><span class="metal-orbit gold">Au<small>Золото</small></span><span class="metal-orbit silver">Ag<small>Серебро</small></span></div><h2>Что говорят цифры</h2><p>Как различаются содержание металла, запасы, извлечение и производственная мощность.</p>{g['link']('resources.html','Читать данные','text-link')}</article></section>
        <section class="wide-feature"><div>{figure('malmyzh-loading-winter.webp')}</div><article><span class="eyebrow">Добыча и переработка</span><h2>От рудного тела<br>до концентрата</h2><p>Открытый карьер, транспорт, дробление, измельчение и обогащение. Разбираем производственную цепочку по этапам.</p>{g['link']('production.html','Как это работает','text-link')}</article></section>
        <section class="history-preview"><span class="eyebrow">Интерактивная история</span><h2>Два десятилетия<br>изучения и освоения</h2><div class="history-dates"><span>2005–2007</span><span aria-hidden="true">→</span><span>2025</span></div><p>От ранних геологических работ к запуску первой очереди фабрики. Даты и события, которые можно проверить.</p>{g['link']('history.html','Пройти по истории','button')}</section>
        <section class="feature-pair reverse"><article><span class="eyebrow">Компания и люди</span><img class="company-inline-logo" src="assets/amur-minerals-logo.svg" alt="Логотип Амур Минералс"><h2>Амур Минералс</h2><p>Оператор разработки Малмыжа: деятельность, рабочие места, социальные инициативы и официальные документы.</p>{g['link']('company.html','Познакомиться с компанией','text-link')}</article><div>{figure('amur-culture.webp')}</div></section>
        <section class="reading-links"><article><span>Регион</span><h2><a href="importance.html">Экономическое значение ↗</a></h2><p>Инвестиции в историческом контексте, занятость и производственные связи.</p></article><article><span>Окружающая среда</span><h2><a href="ecology.html">Добыча и природа ↗</a></h2><p>Вода, воздух, земли и вопросы экологического контроля.</p></article></section>
        <section class="reading-links"><article><span>Фотографии</span><h2><a href="gallery.html">Документальные кадры ↗</a></h2><p>Галерея с подписями, происхождением снимков и увеличением.</p></article><article><span>Редакция</span><h2><a href="sources.html">Как мы проверяем материалы ↗</a></h2><p>Государственные документы, научные публикации и корпоративные источники.</p></article></section>
        '''

    def company():
        return '<div class="company-masthead">'+heading('Компания и регион','Амур Минералс','Оператор Малмыжского проекта. Производство медного концентрата, инженерная инфраструктура и работа с регионом.')+'<figure class="company-logo"><img src="assets/amur-minerals-logo.svg" alt="Официальный логотип Амур Минералс"><figcaption>Логотип: <a href="https://amurminerals.ru/">официальный сайт компании</a></figcaption></figure></div>'+f'''<div class="company-intro"><div>{section('О компании',f'<p>ООО «Амур Минералс» — оператор Малмыжского проекта и резидент ТОР «Хабаровск», по сведениям официального сайта.{cite(2)}</p><p>В сообщении Роснедр 2021 года компания названа владельцем лицензии и участником группы РМК. В нём 2018-й указан как год приобретения оператора Русской медной компанией. Это датированное описание, а не отдельная проверка структуры собственности на сегодня.{cite(1)}</p>')}</div>{figure('malmyzh-hall.webp')}</div>
        <section class="company-numbers"><h2>Компания в цифрах</h2><p>Показатели официального ресурса без даты публикации. Проверено 6 ноября 2026 года. Это сведения оператора, не независимая статистика.</p><div class="light-stats">{statistic('104','млн т/год','Заявленная мощность','Руды в год · не фактический годовой выпуск',2)}{statistic('2500','+','Рабочие места','На предприятии · сведения компании',2)}{statistic('1400','+','Подрядные организации','Рабочие места · сведения компании',2)}</div></section>
        {section('Малмыжский производственный комплекс',f'<p>Связка карьера, переработки и инженерного обеспечения позволяет превратить руду в продукт для дальнейшей металлургии. Сайт оператора указывает 2024 год как запуск первой очереди фабрики. В этой работе нет актуального годового отчёта, позволяющего сопоставить мощность с фактическим выпуском.{cite(2)}</p>')}
        <div class="company-photo-pair">{figure('malmyzh-hangar.webp')}{figure('malmyzh-lighting.webp')}</div>
        {section('Люди и регион',f'<p>Оператор описывает профессиональное развитие и профориентацию, а в социальной политике — поддержку инфраструктуры, образования, культуры и спорта. Эти направления изложены как позиция компании; результат каждой инициативы требует отдельной датированной информации.{cite(14,15)}</p><p>Для знакомства с работой отрасли подготовлен материал о взаимодействии геологов, производственных специалистов и лабораторий: <a href="professions.html">профессии горной промышленности</a>.</p>')}
        <div class="company-culture">{figure('amur-culture.webp')}</div>
        {section('Экология и ответственность',f'<p>В атласе компании перечислены водооборот, пылеподавление, наблюдения и восстановление земель. Их наличие в проекте нужно отличать от подтверждённой эффективности. Для оценки результата необходимы измерения, точки отбора проб и сопоставимые периоды.{cite(4)}</p><p>В <a href="ecology.html">экологическом разделе</a> отдельно изложены возможные риски и ограничения доступных данных.</p>')}
        <section class="official-links"><h2>Официальные ресурсы</h2><a href="https://amurminerals.ru/" target="_blank" rel="noopener">Сайт компании ↗</a><a href="https://amurminerals.ru/career" target="_blank" rel="noopener">Карьера и вакансии ↗</a><a href="https://amurminerals.ru/socialinvestment" target="_blank" rel="noopener">Социальные инвестиции ↗</a></section><p class="editor-note">Страница подготовлена независимым учебным проектом. Поддержка или согласование со стороны компании не заявляются.</p>'''

    def history():
        options=''.join(f'<option value="{i}">{date} — {title}</option>' for i,(date,title,*_) in enumerate(HISTORY))
        entries=''.join(f'<article class="history-event" id="event-{i}" data-event="{i}" data-image="assets/{im}" data-source="{MEDIA.get(im,{}).get('source',9)}" data-caption="{html.escape(title)}"><time>{date}</time><h2>{title}</h2><p>{text}{cite(src)}</p><figure class="mobile-event-photo"><img src="assets/{im}" alt="Иллюстрация темы: {html.escape(title)}" loading="lazy"><figcaption>Иллюстрация темы, не датированный снимок события. Источник фотографии: <a href="sources.html#source-{MEDIA.get(im,{}).get('source',9)}">{MEDIA.get(im,{}).get('credit','АО «Тех Взрыв Инвест»')}</a>.</figcaption></figure></article>' for i,(date,title,text,src,im) in enumerate(HISTORY))
        return heading('История проекта','От первых наблюдений<br>к промышленному освоению','Ранние поиски, государственная оценка, доразведка и производство. У каждого этапа — источник.')+f'''<div class="history-toolbar"><label>Перейти к событию<select id="history-select">{options}</select></label><button id="history-mode" class="map-view" type="button" aria-pressed="false">Вся хронология без анимации</button></div><section class="history-experience" aria-label="Хронология Малмыжа"><div class="history-events">{entries}</div><aside class="history-visual"><div class="history-progress"><span id="history-count" aria-live="polite">1 из {len(HISTORY)}</span><progress id="history-progress" value="1" max="{len(HISTORY)}" aria-label="Прогресс истории"></progress></div><figure><img id="history-image" src="assets/{HISTORY[0][-1]}" alt="Иллюстрация темы ранних геологических работ"><figcaption><span id="history-caption">{HISTORY[0][1]}</span>. Иллюстрация темы, не фотография события. Даты съёмки не указаны. <a id="history-photo-credit" href="sources.html#source-9">Источник фотографии</a></figcaption></figure><div class="history-controls"><button class="map-view" id="history-prev" type="button" disabled>← Назад</button><button class="map-view" id="history-next" type="button">Далее →</button></div></aside></section><section class="prose"><h2>Почему даты требуют пояснений</h2><p>Геологическое открытие, государственная оценка и запуск производства — самостоятельные этапы. Статья описывает ранние работы периодом 2005–2007 годов, а Роснедра включают объект в обзор открытий 2015 года. Поэтому история не сводится к одной универсальной дате.{cite(12,13)}</p><p>Фотографии сопровождают темы; их дата не установлена. Они не представлены архивными кадрами конкретного года.</p></section>'''

    def article(slug):
        title,desc,image,parts=ARTICLES[slug]
        image={'quarry':'malmyzh-dozer.webp','processing':'malmyzh-factory.webp','infrastructure':'malmyzh-grader.webp','professions':'malmyzh-service.webp'}.get(slug,image)
        labels={'discovery':['Признаки','Проверка','Оценка'],'exploration':['Керн','Анализ','Модель'],'quarry':['Уступ','Погрузка','Перевозка'],'processing':['Дробление','Измельчение','Обогащение'],'professions':['Наблюдение','Решение','Контроль'],'copper':['Концентрат','Металл','Изделие'],'concentrate':['Руда','Разделение','Концентрат'],'infrastructure':['Снабжение','Производство','Оборот воды']}[slug]
        diagram='<figure class="concept-diagram"><div class="concept-flow">'+''.join('<span>'+word+'</span>'+('<b aria-hidden="true">→</b>' if i<2 else '') for i,word in enumerate(labels))+'</div><figcaption>Учебная схема связи этапов. Не регламент и не проектный чертёж Малмыжского ГОКа.</figcaption></figure>'
        return heading('Разобраться в теме',title,desc)+f'<div class="longread">'+('' if slug in ['copper','concentrate'] else figure(image,'Иллюстрация темы: '+title,source=2 if image=='people.webp' else 9))+diagram+''.join(section(t,f'<p>{text}{cite(src)}</p>') for t,text,src in parts)+'<div class="related-reading"><h2>Продолжить чтение</h2><a href="about.html">Геология Малмыжа ↗</a><a href="production.html">Добыча и переработка ↗</a><a href="history.html">История проекта ↗</a></div></div>'

    def gallery():
        groups={f.replace('.jpg','.webp'):('Карьер' if 'rock' in f or 'loading' in f or 'excavator' in f else 'Техника') for f in g['PHOTO_INFO']}
        groups.update({f:m['category'] for f,m in MEDIA.items()})
        categories=list(dict.fromkeys(groups.values()))
        return heading('Фотографический атлас','Малмыж в деталях','16 разных кадров: карьер, техника, производственные корпуса и жизнь региона. У каждого снимка — источник и пояснение.')+'<label class="filter-label">Тема <select id="gallery-filter"><option value="">Все фотографии · 16</option>'+''.join(f'<option>{c}</option>' for c in categories)+'</select></label><div class="photo-grid gallery-grid">'+''.join(f'<div data-gallery-category="{c}">'+figure(f,g['PHOTO_INFO'].get(f.replace('.webp','.jpg'),('', ''))[0])+'</div>' for f,c in groups.items())+'</div>'+section('Происхождение снимков','<p>Горные работы и техника — из галереи АО «Тех Взрыв Инвест». Корпуса и освещение — из проекта БМ Электро для ООО «Амур Минералс». Культурный сюжет — с официального сайта оператора. Даты съёмки и индивидуальные фотографы не указаны; стадии строительства не представлены как сегодняшнее состояние предприятия.</p><p>Права на снимки остаются у правообладателей. Водяные знаки сохранены. <a href="assets/image-sources.json">Точные адреса изображений и сведения об источниках</a>.</p>')
    pages['gallery']=('Фотогалерея',gallery)

    pages['index']=('Главная',home);pages['company']=('Амур Минералс',company);pages['history']=('История Малмыжского проекта',history)
    for slug,data in ARTICLES.items():pages[slug]=(data[0],lambda key=slug:article(key))
    appendices={
      'about': [('Геологическое строение','Вмещающая толща представлена преимущественно песчаниками и алевролитами. Её прорывают интрузивные тела; минерализация связана с этой сложной системой пород. Разрез с истинными глубинами нельзя восстановить по одной фотографии или общей модели.',1),('Что дают геофизические исследования','Магнитные и гравитационные данные позволяют строить модели глубинного строения. В работе 2023 года такие модели рассматриваются для рудных узлов Приамурья. Они дополняют полевые исследования, но не заменяют опробование руды.',12)],
      'resources':[('Среднее содержание компонентов','Роснедра приводят средние содержания: медь около 0,35 %, золото 0,145 г/т, серебро 0,7 г/т. Проценты и граммы на тонну выражают состав руды. Эти значения нельзя ставить на общую числовую шкалу без перевода единиц и пояснения.',1)],
      'ecology':[('Что должно быть в отчёте мониторинга','Полезный отчёт связывает результат с местом и датой измерения, методом, фоновым уровнем и применимым нормативом. Серия наблюдений помогает отделить устойчивую тенденцию от единичного результата. В этой подборке такого ряда по объекту нет.',5)]}
    relations={'about':['discovery','exploration'],'production':['quarry','processing','concentrate'],'importance':['professions','infrastructure','copper'],'resources':['concentrate','copper'],'ecology':['infrastructure']}
    for slug in relations:
        original=previous[slug][1]
        def expanded(key=slug,body=original):
            text=body()
            if key=='production':
                text=re.sub(r'<section class="gallery-section">.*?</section>', '<section class="gallery-section"><h2>Корпуса и инженерное оснащение</h2><div class="photo-grid">'+figure('malmyzh-hall.webp')+figure('malmyzh-lighting.webp')+'</div></section>',text,flags=re.S)
            if key=='importance':
                text=re.sub(r'<figure class="photo">.*?</figure>',lambda m:figure('amur-culture.webp') if 'people.' in m[0] else m[0],text,flags=re.S)

            # Убираем повторение одних и тех же снимков внутри четырёх экологических карточек.
            if key=='ecology':text=re.sub(r'(<article class="risk">)<img.*?</small>',r'\1',text)
            text+=''.join(section(t,f'<p>{p}{cite(src)}</p>') for t,p,src in appendices.get(key,[]))
            text+='<section class="related-reading"><h2>Разобраться подробнее</h2>'+''.join(f'<article><h3><a href="{s}.html">{ARTICLES[s][0]} ↗</a></h3><p>{ARTICLES[s][1]}</p></article>' for s in relations[key])+'</section>'
            return text
        pages[slug]=(previous[slug][0],expanded)

    source_body=previous['sources'][1]
    def sources():
        text=source_body().replace('Шрифты Manrope и Inter','Шрифты Manrope, Inter и Unbounded')
        text=text.replace('Лицензии шрифтов</a>.','Лицензии Manrope и Inter</a> · <a href="assets/Unbounded-OFL.txt">Лицензия Unbounded</a>.')
        text=text.replace('data-category="map" id="source-12"','data-category="science" id="source-12"').replace('data-category="map" id="source-13"','data-category="state" id="source-13"')
        for n in [14,15,16]:text=text.replace(f'data-category="map" id="source-{n}"',f'data-category="company" id="source-{n}"')
        text+=section('Иллюстрации и фотографии процессов','<p>Художественные изображения минерала и ландшафта на главной созданы с помощью ИИ. Они не являются фотографиями образцов или геологическим разрезом Малмыжа. Схема порфировой системы — авторская визуализация по USGS [7].</p><p>Фотографии дробления, измельчения, флотации и фильтрации: <a href="https://www.amur-gold.ru/novosti-i-sobytiya/fotogalereya/modulnaya-obogatitelnaya-fabrika-gok-perevalnyy/">официальная галерея «Амур Золото», ГОК «Перевальный»</a>. Показаны примеры оборудования на другом предприятии. Права принадлежат правообладателям. <a href="assets/process-sources.json">Адреса оригиналов</a>.</p>')
        return text
    pages['sources']=(previous['sources'][0],sources)
    pages.pop('updates',None)

    def render(slug):
        text=base_render(slug)
        text=text.replace('</head>','<link rel="stylesheet" href="assets/light.css?v=review-2"><script type="module" src="assets/light.js?v=review-2"></script></head>')
        nav=''.join(f'<a href="{s}.html"'+(' aria-current="page"' if slug==s else '')+f'>{t}</a>' for s,t in [('about','Месторождение'),('production','Добыча'),('ecology','Экология'),('history','История'),('company','Амур Минералс')])
        extra=''.join(f'<a href="{s}.html">{t}</a>' for s,t in [('location','Карта'),('resources','Запасы'),('importance','Экономика'),('gallery','Фотогалерея'),('sources','Источники')])
        nav+='<details class="more-nav"><summary>Разделы</summary><div>'+extra+'</div></details>'
        text=re.sub(r'(<nav id="site-nav"[^>]*>).*?</nav>',lambda m:m[1]+nav+'</nav>',text,count=1)
        text=text.replace('<div class="footer-links">','<div class="footer-links"><a href="company.html">Амур Минералс</a>')
        text=text.replace('Фактические материалы: проверка 5 ноября 2026','Источники проверены 5–6 ноября 2026')
        for filename in g['PHOTO_INFO']:text=text.replace('assets/'+filename,'assets/'+filename.removesuffix('.jpg')+'.webp')
        text=re.sub(r'<a href="updates.html">.*?</a>',"",text)
        return text
    g['render']=render
