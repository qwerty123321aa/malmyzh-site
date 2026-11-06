"""Малмыж: Python-сайт и генератор страниц для GitHub Pages. Python 3.10+, без зависимостей."""
from __future__ import annotations
import argparse
import functools
import html
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'docs'
CHECKED = '5 ноября 2026'
SOURCES = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
NAV = [('index','Главная'),('about','О месторождении'),('location','Где находится'),('resources','Что добывают'),('importance','Значение'),('ecology','Экология')]
ARROW = '<span aria-hidden="true">↗</span>'

def cite(*ids):
    return ' <span class="citations">' + ' '.join(f'<a href="sources.html#source-{i}" title="Источник: {html.escape(SOURCES[i-1]["name"])}">[{i}]</a>' for i in ids) + '</span>'

def tag(text): return f'<span class="eyebrow">{text.capitalize() if text.isupper() else text}</span>'
def link(url,text,cls='button'): return f'<a class="{cls}" href="{url}">{text} {ARROW}</a>'
def note(text): return f'<aside class="note">{text}</aside>'
def heading(kicker,title,desc): return f'<header class="page-heading">{tag(kicker)}<h1>{title}</h1><p class="lead">{desc}</p></header>'
def section(title,text): return f'<section class="prose"><h2>{title}</h2>{text}</section>'
PHOTO_PAGE = 'https://t-v-i.ru/proekty/malmyzhskoe-mestorozhdenie/'
PHOTO_INFO = {
 'malmyzh-loading.jpg': ('Погрузка горной породы', 'Экскаватор и карьерный самосвал на площадке Малмыжского проекта.'),
 'malmyzh-rock.jpg': ('Работа с горной породой', 'Бульдозер на участке горных работ.'),
 'malmyzh-fleet.jpg': ('Карьерный транспорт', 'Самосвалы на площадке рядом с лесным массивом.'),
 'malmyzh-drilling.jpg': ('Буровые работы', 'Буровые установки на зимней площадке.'),
 'malmyzh-excavator.jpg': ('Открытые горные работы', 'Экскаватор у уступа из горной породы.'),
 'malmyzh-night.jpg': ('Работы в тёмное время суток', 'Буровая установка и освещение рабочей площадки.'),
 'malmyzh-winter.jpg': ('Зимняя площадка', 'Экскаватор и буровая техника зимой.')
}

def photo(file,alt,caption,source=9,eager=False):
    loading='fetchpriority="high"' if eager else 'loading="lazy"'
    credit=(f'<a href="{PHOTO_PAGE}" target="_blank" rel="noopener">АО «Тех Взрыв Инвест»</a>. Дата съёмки не указана.' if source==9 else '<a href="https://amurminerals.ru/">«Амур Минералс»</a>. Автор и дата съёмки не указаны.')
    return f'<figure class="photo"><button class="photo-open" type="button" data-photo="assets/{file}" aria-label="Увеличить: {html.escape(alt)}"><img src="assets/{file}" alt="{html.escape(alt)}" {loading}><span class="zoom-hint" aria-hidden="true">Увеличить</span></button><figcaption><strong>{caption}</strong><span>Фото: {credit}{cite(source)}</span></figcaption></figure>'

def photo_gallery(files,title='Фотографии с месторождения'):
    return '<section class="gallery-section"><div class="section-heading"><h2>'+title+'</h2><p>Документальные снимки из галереи подрядчика Малмыжского проекта. Нажмите на фотографию, чтобы рассмотреть её.</p></div><div class="photo-grid">'+''.join(photo(f,PHOTO_INFO[f][1],PHOTO_INFO[f][0]) for f in files)+'</div></section>'

def reserves_chart():
    return f'''<section class="reserves-chart"><div class="section-heading"><h2>Как изменилась оценка запасов</h2><p>После доразведки оценку пересмотрели. Это изменение учтённых запасов, а не рост ежегодной добычи.{cite(1)}</p></div><div class="chart-grid"><figure><h3>Медь <span>млн тонн</span></h3><div class="bar-row"><span>До пересмотра</span><div class="bar-track"><div class="bar old" style="width:62.1%">5,156</div></div></div><div class="bar-row"><span>Оценка 2021</span><div class="bar-track"><div class="bar" style="width:100%">8,3</div></div></div><figcaption>Длина полос пропорциональна запасам меди.</figcaption></figure><figure><h3>Золото <span>тонн</span></h3><div class="bar-row"><span>До пересмотра</span><div class="bar-track"><div class="bar old" style="width:80.02%">278</div></div></div><div class="bar-row"><span>Оценка 2021</span><div class="bar-track"><div class="bar" style="width:100%">347,4</div></div></div><figcaption>У золота своя шкала; сравнивать длины с графиком меди нельзя.</figcaption></figure></div><p class="chart-source">Данные: Роснедра, 29.10.2021; протокол ГКЗ от 22.09.2021 № 6749.{cite(1)}</p></section>'''

def stat(value,label,small=''): return f'<div class="stat"><strong>{value}</strong><span>{label}</span><small>{small}</small></div>'
def next_page(url,title): return f'<div class="next-page"><span>Продолжить знакомство</span>{link(url,title,"text-link")}</div>'
def article_nav(items):return '<nav class="article-nav" aria-label="На этой странице"><span>На странице</span>'+''.join(f'<a href="#{k}">{v}</a>' for k,v in items)+'</nav>'

def home():
    topics=[('about','О месторождении','Геология, порода и полезные компоненты.','malmyzh-excavator.jpg'),('location','Где находится','Приамурье на интерактивной карте.','malmyzh-fleet.jpg'),('resources','Что добывают','Медь, золото, серебро и путь руды.','malmyzh-drilling.jpg')]
    return f'''<section class="home-hero"><div class="hero-copy">{tag('Хабаровский край')}<h1>Малмыжское месторождение</h1><p class="lead">Медь и золото Приамурья: где находится месторождение, как здесь работают и что важно знать о влиянии добычи на природу.</p><div class="hero-actions">{link('about.html','О месторождении')}{link('location.html','Посмотреть на карте','quiet-link')}</div><p class="hero-context">Информационный проект с документальными фотографиями и проверяемыми источниками.</p></div>{photo('malmyzh-loading.jpg',PHOTO_INFO['malmyzh-loading.jpg'][1],'Погрузка породы на площадке Малмыжского проекта',eager=True)}</section>
    <section class="facts-strip" aria-label="Запасы по оценке 2021 года">{stat('8,3 <i>млн т</i>','меди в запасах')}{stat('347,4 <i>т</i>','золота в запасах')}{stat('1 676 <i>т</i>','серебра в запасах')}<div class="stat-note">Оценка ГКЗ от 22.09.2021.<br>Запасы отличаются от годовой добычи.{cite(1)}</div></section>
    <section class="intro-row"><h2>Познакомиться с Малмыжем</h2><p>От геологического строения — к работе предприятия и вопросам, которые важны для Хабаровского края.</p></section>
    <div class="topic-grid">{''.join(f'<article class="topic"><a href="{slug}.html"><img src="assets/{image}" alt="{PHOTO_INFO[image][1]}" loading="lazy"><h3>{title}</h3></a><p>{desc}</p><small>Фото: <a href="sources.html#source-9">АО «Тех Взрыв Инвест»</a></small></article>' for slug,title,desc,image in topics)}</div>
    {reserves_chart()}
    <section class="editorial-links"><article><h2>Значение для региона</h2><p>Рабочие места, производственные связи и развитие территории.</p>{link('importance.html','Экономика и люди','text-link')}</article><article><h2>Добыча и природа</h2><p>Как открытые горные работы связаны с водой, воздухом и состоянием земель.</p>{link('ecology.html','Экологические вопросы','text-link')}</article></section>
    {photo_gallery(['malmyzh-drilling.jpg','malmyzh-night.jpg','malmyzh-winter.jpg'],'На площадке: зима, бурение, техника')}
    <div class="research-note"><p><strong>Материалы можно проверить.</strong> У фотографий указано происхождение, у числовых данных — источник и дата.</p>{link('sources.html','Источники и фотографии','text-link')}</div>'''

def about():
    return heading('Геология','Что такое Малмыжское месторождение','Большое скопление руд, из которых извлекают медь и попутные драгоценные металлы.')+f'''
    <div class="article-layout"><div class="article-main">{section('Месторождение простыми словами',f'<p>Это участок земной коры, где полезные компоненты сосредоточены в количестве и условиях, позволяющих рассматривать их промышленное освоение. Малмыжское относится к золото-медно-порфировому типу: медные минералы распределены в большом объёме горных пород.{cite(1)}</p><p>Руда не выглядит как сплошной кусок металла. Полезные минералы встречаются вкраплениями и тонкими прожилками. Чтобы получить продукт, породу добывают, измельчают и обогащают.{cite(7)}</p>')}
    {photo('malmyzh-excavator.jpg',PHOTO_INFO['malmyzh-excavator.jpg'][1],'Порода и экскаватор на участке горных работ')}

    {section('Что находится в руде',f'<p>Роснедра перечисляют пирит и халькопирит, реже — другие сульфидные минералы. Главные полезные компоненты — медь и золото; серебро извлекается попутно. Для разработки выбран открытый способ — карьеры.{cite(1)}</p>')}
    {section('От геологии к производству',f'<p>Оператор освоения — ООО «Амур Минералс». По данным его официального сайта, первую очередь обогатительной фабрики запустили в 2024 году. Предприятие специализируется на медном концентрате.{cite(2)}</p>')}
    {note('Геологическая оценка и производственный отчёт отвечают на разные вопросы. Запасы показывают, сколько металла учтено в недрах; выпуск — сколько продукции получено за конкретный период.')}
    </div><aside class="side-facts">{tag('ПАСПОРТ ОБЪЕКТА')}<dl><dt>Тип</dt><dd>Золото-медно-порфировый</dd><dt>Регион</dt><dd>Хабаровский край</dd><dt>Способ разработки</dt><dd>Открытый</dd><dt>Оператор</dt><dd>ООО «Амур Минералс»</dd><dt>Продукт ГОКа</dt><dd>Медный концентрат</dd></dl><p class="muted">Основание: Роснедра и официальный сайт оператора.{cite(1,2)}</p></aside></div>'''+next_page('location.html','Где находится Малмыж')

def location():
    near='https://www.openstreetmap.org/export/embed.html?bbox=136.65%2C49.80%2C137.18%2C50.06&amp;layer=mapnik&amp;marker=49.9338%2C136.918'
    region='https://www.openstreetmap.org/export/embed.html?bbox=134.7%2C48.2%2C138.4%2C51.1&amp;layer=mapnik&amp;marker=49.9338%2C136.918'
    return heading('География','Где находится месторождение','Хабаровский край, Амурский и Нанайский районы.'+cite(1))+f'''
    <section class="map-section"><div class="map-toolbar" role="group" aria-label="Масштаб карты"><button type="button" class="map-view active" data-map-src="{near}" aria-pressed="true">Район месторождения</button><button type="button" class="map-view" data-map-src="{region}" aria-pressed="false">Приамурье целиком</button><a href="https://www.openstreetmap.org/?mlat=49.9338&amp;mlon=136.918#map=11/49.9338/136.918" target="_blank" rel="noopener">Открыть большую карту ↗</a></div><iframe id="location-map" title="Интерактивная карта Приамурья с приблизительной отметкой Малмыжского месторождения" src="{near}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe><p class="map-credit">Карта: © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>, ODbL. Отметка по каталогу паспортов месторождений.{cite(10,11)}</p></section>
    <div class="two-columns">{section('Между Хабаровском и Комсомольском-на-Амуре',f'<p>Главный географический ориентир — река Амур. Малмыжское месторождение находится в Приамурье; Роснедра указывают его расположение на территории Амурского и Нанайского районов.{cite(1)}</p>')}{section('Что показывает отметка',f'<p>В каталоге приведены приблизительные координаты 49.9338° с. ш., 136.918° в. д. Это ориентир для знакомства с районом. Он не показывает точный контур месторождения, границы горного отвода или въезд на предприятие.{cite(10)}</p>')}</div>
    {note('В каталоге точность координат ограничена. Карту можно приближать и перемещать, но использовать отметку для маршрута на промышленную площадку нельзя. Если встроенная карта недоступна, откройте её по ссылке над картой.')}
    {photo_gallery(['malmyzh-fleet.jpg','malmyzh-winter.jpg'],'Территория и условия работы')}
    '''+next_page('resources.html','Что добывают на месторождении')

def resources():
    metals=[('29','Cu','Медь','8,3 млн т','Главный полезный компонент. На комбинате медную руду обогащают и получают концентрат.','copper'),('79','Au','Золото','347,4 т','Драгоценный попутный компонент медной руды. Его запасы также учтены государственной экспертизой.','gold'),('47','Ag','Серебро','1 676 т','Попутный полезный компонент. Округлённая оценка запасов из публикации Роснедр.','silver')]
    return heading('Полезные ископаемые','Медь, золото и серебро','Из недр добывают руду. Ценные металлы извлекают из неё в процессе обогащения и последующей переработки.')+f'''
    <div class="metal-grid">{''.join(f'<article class="metal {cl}"><div class="element"><small>{n}</small><strong>{symbol}</strong></div><h2>{name}</h2><b>{amount}</b><span>запасы по оценке 2021 года</span><p>{desc}</p>{cite(1)}</article>' for n,symbol,name,amount,desc,cl in metals)}</div>
    {note('Числа показывают массу металлов, учтённых в запасах по оценке ГКЗ от 22 сентября 2021 года. Это не масса ежегодно добываемой руды, не выпуск за 2026 год и не количество готовых слитков.')}
    {photo('malmyzh-rock.jpg',PHOTO_INFO['malmyzh-rock.jpg'][1],'Горная порода на рабочей площадке')}
    <section class="grade-visual"><div><h2>Много породы — небольшая доля металла</h2><p>Среднее содержание меди, приведённое Роснедрами, — около 0,35%. В одной тонне такой руды это примерно 3,5 кг содержащейся меди. Это пересчёт состава до потерь при извлечении.{cite(1)}</p></div><div class="grade-comparison"><div class="ore-block"><span>1 тонна руды</span><div class="copper-dot" aria-hidden="true"></div></div><div class="grade-label"><strong>≈ 3,5 кг меди</strong><span>Маленький квадрат — 0,35% площади большого.<br>Остальное — другие компоненты породы.</span></div></div></section>
    {section('Путь от руды к концентрату','<p>Упрощённая учебная последовательность помогает понять, почему добыча и металлургия — разные стадии.</p>'+cite(7))}
    <ol class="process"><li><h3>Добыча</h3><p>Горную породу извлекают в карьере.</p></li><li><h3>Подготовка</h3><p>Руду дробят и измельчают.</p></li><li><h3>Обогащение</h3><p>Полезные минералы отделяют от основной массы породы.</p></li><li><h3>Концентрат</h3><p>Полученный продукт отправляют на дальнейшую переработку.</p></li></ol>
    <div class="two-columns">{section('Что выпускает комбинат',f'<p>Официальный сайт «Амур Минералс» называет основным продуктом предприятия медный концентрат. Поэтому говорить, что прямо на Малмыже получают готовые медные провода или золотые украшения, неверно.{cite(2)}</p>')}{section('Где пригодится медь',f'<p>Медь используют в электрической проводке, передаче энергии и электронных изделиях. Это примеры применения металла в целом, а не перечень покупателей Малмыжского ГОКа.{cite(8)}</p>')}</div>'''+next_page('importance.html','Почему месторождение важно')

def importance():
    return heading('Экономика и люди','Значение для Хабаровского края','Значение месторождения выходит за пределы карьера: оно связано с занятостью, производством и развитием территории.')+f'''
    <div class="two-columns align-top">{photo('people.jpg','Работник на производственной площадке: фотография с официального сайта «Амур Минералс»','Изображение с сайта оператора. Автор отдельно не указан; это иллюстрация производственной темы, а не подтверждение численности персонала.',source=2)}<div class="prose"><h2>Работа и профессиональные навыки</h2><p>Горному предприятию нужны специалисты разных направлений: рабочие, инженеры, сотрудники лабораторий, транспорта и обслуживания.</p><p>Оператор указывает более 2 500 рабочих мест на предприятии и более 1 400 — в подрядных организациях. Эти значения приведены как сведения компании, без вывода о фактической занятости на определённую дату.{cite(2)}</p><div class="small-fact"><strong>2024</strong><span>год запуска первой очереди фабрики<br>по данным оператора {cite(2)}</span></div></div></div>
    {photo_gallery(['malmyzh-fleet.jpg','malmyzh-drilling.jpg'],'Транспорт и технические специальности')}
    <div class="text-sections"><article><div><h2>Минеральное сырьё</h2><p>Большая ресурсная база позволяет рассматривать длительное промышленное освоение. Но экономический результат зависит от затрат, технологии и условий реализации продукции.</p></div></article><article><div><h2>Производственная цепочка</h2><p>ГОК соединяет добычу, обогащение, энергоснабжение и перевозки. Это создаёт спрос на оборудование, обслуживание и квалификацию работников.</p></div></article><article><div><h2>Ответственность перед территорией</h2><p>Польза для региона должна оцениваться вместе с расходами на защиту природы и восстановление земель, интересами жителей и качеством экологического контроля.</p></div></article></div>
    {note('Последние три пункта — объяснение экономических связей, а не расчёт вклада предприятия в бюджет края. На сайте не приводятся неподтверждённые суммы налогов, инвестиций или обещания роста доходов.')}
    '''+next_page('ecology.html','Влияние на окружающую среду')

def ecology():
    risks=[('Вода','При контакте сульфидных пород с водой и кислородом возможно образование кислого дренажа и перенос растворённых металлов. Степень риска зависит от состава пород и условий хранения.','Исследовать состав стоков, кислотность и металлы, сравнивать фоновые и контрольные пробы.',5),('Воздух','Работа с рудой, дороги и перемещение породы требуют контроля пыления. В материалах компании предусмотрены орошение, пылеулавливание и закрытые конвейеры.','Проверять концентрации пыли, работу оборудования и эффективность пылеподавления.',4),('Земли и растительность','Открытые горные работы меняют рельеф и почвенно-растительный покров. Нарушенные участки требуют восстановления; эрозия может переносить частицы в водотоки.','Отслеживать площади нарушений, состояние почв и результаты рекультивации.',6),('Хвостохранилище','После обогащения остаются хвосты. Для их размещения необходимы инженерная защита и контроль воды; в проектных материалах Малмыжа заявлены экран и наблюдательные скважины.','Наблюдать за фильтрацией, подземными водами и устойчивостью сооружений.',4)]
    return heading('Окружающая среда','Месторождение и природа края','Для Хабаровского края важны состояние водных объектов, сохранность земель и проверяемость природоохранных мер.')+f'''
    {article_nav([('known','Что подтверждено'),('risks','Возможные риски'),('protection','Меры защиты'),('evidence','Каких данных не хватает')])}
    {photo('malmyzh-fleet.jpg',PHOTO_INFO['malmyzh-fleet.jpg'][1],'Промышленная площадка рядом с лесом. Снимок не является измерением экологического воздействия.')}
    <section id="known" class="prose"><h2>Что подтверждают источники</h2><p>Официальные сведения описывают открытый способ разработки. В уведомлении Росприроднадзора за 2025 год фигурирует обогатительная фабрика с хвостовым хозяйством и оборотным водоснабжением.{cite(1,3)}</p><p>Это означает, что при оценке воздействия нужно учитывать карьер, переработку руды, размещение отходов и движение воды. Само наличие проектной документации не доказывает ни отсутствие загрязнения, ни факт экологического ущерба.</p></section>
    <section id="risks"><div class="section-heading">{tag('РИСК ≠ УСТАНОВЛЕННЫЙ УЩЕРБ')}<h2>За чем нужно следить</h2><p>Ниже — возможные механизмы воздействия и вопросы контроля. Это не сообщение о выявленных нарушениях на Малмыже.</p></div><div class="risk-grid">{''.join(f'<article class="risk"><h3>{title}</h3><p>{text}{cite(src)}</p><details><summary>Что проверять</summary><p>{control}</p></details></article>' for i,(title,text,control,src) in enumerate(risks))}</div></section>
    <section id="protection" class="eco-banner"><div>{tag('ЗАЯВЛЕНО В МАТЕРИАЛАХ КОМПАНИИ')}<h2>Вода должна<br>возвращаться в процесс.</h2><p>Атлас «Амур Минералс» описывает оборот воды, защиту основания хвостохранилища, дренаж и наблюдательные скважины. Для воздуха — пылеподавление; для земель — рекультивацию.{cite(4)}</p><p class="muted">Это описание предусмотренных мер. Их фактическую эффективность показывают измерения и результаты контроля.</p></div><figure><img src="assets/water-cycle.svg" alt="Учебная схема оборотного водоснабжения: фабрика, хвостохранилище, возврат воды"><figcaption>Авторская упрощённая схема по атласу компании. Водный баланс и объёмы не показаны.{cite(4)}</figcaption></figure></section>
    <section id="evidence" class="prose"><h2>Каких данных не хватает для вывода</h2><p>В проверенной для этого сайта подборке нет ряда сопоставимых независимых измерений, позволяющего количественно оценить влияние Малмыжского ГОКа на весь Хабаровский край. Поэтому здесь нет утверждений о конкретном уровне загрязнения Амура или доказанном отсутствии воздействия.</p><p>Для такой оценки нужны результаты проб воды, воздуха и почв с датами и местами отбора, фоновыми значениями, описанием методов и установленными нормативами, а также сведения о работе защитных сооружений.</p></section>
    {note('<strong>Как читать экологические сообщения.</strong> Уточняйте, идёт ли речь о проектном решении, обещании, единичной пробе или серии измерений. Проверяйте дату, место, методику и автора. Общие знания о горной добыче не являются доказательством загрязнения конкретной реки.')}
    '''+next_page('sources.html','Посмотреть источники и подписи')

def sources_page():
    blocks=''.join(f'''<article class="source" id="source-{s['id']}"><div><span class="source-type">{s['type']}</span><h2><a href="{s['url']}" target="_blank" rel="noopener noreferrer">{s['title']} {ARROW}</a></h2><p class="source-meta">{s['name']} · {s['date']}</p><p><b>Что использовано:</b> {s['used']}</p><p class="muted"><b>Как оценивать:</b> {s['note']}</p></div></article>''' for s in SOURCES)
    return heading('О проекте','Источники и фотографии',f'Проверено {CHECKED} года. Ссылки в квадратных скобках рядом с текстом ведут к соответствующей записи.')+f'''
    {note('Факты пересказаны своими словами. Оценки запасов датированы 2021 годом; описание предприятия сверено с текущим сайтом оператора. Корпоративные материалы отмечены отдельно. Уведомление об обсуждениях не заменяет заключение экспертизы.')}
    <div class="sources-list">{blocks}</div>
    <section class="prose" id="images"><h2>Откуда взяты фотографии</h2><p>Снимки карьера, погрузки, самосвалов и буровых установок взяты из галереи проекта «Малмыжское месторождение» на сайте АО «Тех Взрыв Инвест». Отдельный фотограф и даты съёмки не указаны. Подписи описывают только то, что видно на кадрах.{cite(9)}</p><p>Фотография работника — с сайта оператора «Амур Минералс». Она отдельно подписана и не выдана за снимок подрядчика.{cite(2)}</p><p>Права на фотографии сохраняются за правообладателями. Исходные водяные знаки сохранены. Наличие подписи не означает свободную лицензию. Прямые адреса всех файлов: <a href="assets/image-sources.json">реестр изображений</a>.</p></section>
    {photo_gallery(['malmyzh-loading.jpg','malmyzh-excavator.jpg','malmyzh-fleet.jpg','malmyzh-drilling.jpg','malmyzh-night.jpg','malmyzh-winter.jpg'],'Фотоматериалы проекта')}
    <section class="prose"><h2>Карта, графики и шрифт</h2><p>Картографическая основа — OpenStreetMap. Приблизительная точка дана по каталогу паспортов месторождений; границы лицензии не нанесены.{cite(10,11)}</p><p>Графики запасов и схема доли меди построены по данным Роснедр. Шкалы и ограничения объяснены рядом с изображениями. Схема водооборота — учебная, по атласу компании.{cite(1,4)}</p><p>Шрифт <a href="https://fonts.google.com/specimen/Golos+Text">Golos Text</a> используется по <a href="assets/Golos-OFL.txt">SIL Open Font License</a> и хранится в проекте.</p></section>

    <section class="prose"><h2>О границах проекта</h2><p>Это самостоятельный учебный информационный проект, не официальный сайт компании или органов власти. Он знакомит с темой и показывает, как проверять источники. Если исходная публикация обновится, текст сайта нужно повторно сверить.</p></section>'''

PAGES = {'index':('Главная',home),'about':('Что такое Малмыжское месторождение',about),'location':('Где находится месторождение',location),'resources':('Что добывают на месторождении',resources),'importance':('Почему месторождение важно',importance),'ecology':('Экология Хабаровского края',ecology),'sources':('Источники и изображения',sources_page)}

def render(slug):
    title,body=PAGES[slug]
    nav=''.join(f'<a href="{key}.html"'+(' aria-current="page"' if key==slug else '')+f'>{name}</a>' for key,name in NAV)
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="description" content="Малмыжское месторождение: география, медь, золото, значение для Хабаровского края и экологические вопросы. Учебный проект с проверяемыми источниками."><title>{title} — Малмыж</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/editorial.css?v=photos-2"><script src="assets/editorial.js?v=photos-2" defer></script></head>
<body><a class="skip-link" href="#main">К содержанию</a><header class="site-header"><div class="header-inner"><a class="brand" href="index.html" aria-label="Малмыж — главная"><span>Малмыж<small>ХАБАРОВСКИЙ КРАЙ</small></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Меню <span aria-hidden="true">☰</span></button><nav id="site-nav" aria-label="Основная навигация">{nav}</nav><a class="header-sources" href="sources.html" {'aria-current="page"' if slug=='sources' else ''}>Источники {ARROW}</a></div></header><main id="main" class="container {'home' if slug=='index' else ''}">{'' if slug=='index' else '<nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span>/</span><span>'+title+'</span></nav>'}{body()}</main><dialog id="photo-dialog" aria-label="Просмотр фотографии"><button class="dialog-close" type="button" aria-label="Закрыть фотографию">Закрыть ×</button><img alt="Полноразмерная фотография"><p></p></dialog><footer class="site-footer"><div class="container footer-inner"><div><a class="footer-brand" href="index.html">Малмыж<span> / Хабаровский край</span></a><p>Геология. Люди. Природа.<br>Учебный информационный проект.</p></div><div><a href="sources.html">Источники и изображения ↗</a><p>Проверка материалов: {CHECKED}<br>Неофициальный сайт · Создан на Python</p></div></div></footer></body></html>'''

def build(destination=DIST):
    destination.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'assets',destination/'assets',dirs_exist_ok=True)
    for slug in PAGES:(destination/f'{slug}.html').write_text(render(slug),encoding='utf-8')
    (destination/'.nojekyll').touch()
    (destination/'404.html').write_text(render('index').replace('<h1>Малмыж.', '<p class="not-found">Такой страницы нет. Начните с главной.</p><h1>Малмыж.'),encoding='utf-8')
    from portal import build_extra
    build_extra(destination,PAGES,render)
    return destination

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Страницы создаются Python при каждом открытии; остальные файлы отдаются как статика.
        slug=self.path.split('?',1)[0].strip('/').removesuffix('.html') or 'index'
        if slug in PAGES:
            content=render(slug).encode('utf-8')
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
        else:super().do_GET()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','serve','check'],nargs='?',default='serve')
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    if args.command=='build':print(f'Собрано {len(PAGES)} страниц: {build()}')
    elif args.command=='check':
        import check_site
        check_site.check()
    else:
        build()
        server=ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(Handler,directory=str(DIST)))
        print(f'Малмыж: http://127.0.0.1:{args.port}',flush=True)
        try:server.serve_forever()
        except KeyboardInterrupt:server.server_close()

from portal import install
install(globals())

if __name__=='__main__':main()
