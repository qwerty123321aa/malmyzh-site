"""Interactive educational sections built into the existing static pages."""
import html
import re

PROCESS_PHOTOS = 'https://www.amur-gold.ru/novosti-i-sobytiya/fotogalereya/modulnaya-obogatitelnaya-fabrika-gok-perevalnyy/'
STAGES = [
    ('quarry', 'Карьер', 'Открыть рудное тело', 'Руду извлекают открытым способом. Горные работы ведут уступами, формируя рабочие площадки для техники.', 'malmyzh-excavator.webp', 'Горные работы на Малмыже', 'Малмыж · АО «Тех Взрыв Инвест»', 'sources.html#source-9', 'Руда в массиве → горная масса'),
    ('haul', 'Перевозка', 'Доставить руду к переработке', 'После погрузки руду перемещают к пунктам подготовки. Карьерный транспорт связывает добычу с дальнейшей технологической цепочкой.', 'malmyzh-fleet.webp', 'Карьерные самосвалы на Малмыже', 'Малмыж · АО «Тех Взрыв Инвест»', 'sources.html#source-9', 'Горная масса → подготовка'),
    ('crush', 'Дробление', 'Уменьшить размер кусков', 'Дробилки разрушают крупные куски породы. Подготовленная руда поступает на следующую стадию уменьшения крупности.', 'process-crushing.jpg', 'Дробильно-сортировочный комплекс', 'ГОК «Перевальный» · Амур Золото', PROCESS_PHOTOS, 'Крупные куски → дроблёная руда'),
    ('grind', 'Измельчение', 'Освободить полезные минералы', 'В мельницах руда измельчается ещё тоньше. Это помогает раскрыть срастания медных минералов с окружающей породой и подготовить материал к разделению.', 'process-grinding.jpg', 'Мельницы обогатительной фабрики', 'ГОК «Перевальный» · Амур Золото', PROCESS_PHOTOS, 'Дроблёная руда → тонкие частицы'),
    ('float', 'Флотация', 'Собрать ценные компоненты', 'В водной среде с реагентами полезные минералы связываются с пузырьками воздуха и переходят в пенный продукт. Так повышают содержание ценных компонентов.', 'process-flotation.jpg', 'Флотационное отделение', 'ГОК «Перевальный» · Амур Золото', PROCESS_PHOTOS, 'Минеральная смесь → обогащённый продукт'),
    ('concentrate', 'Концентрат', 'Подготовить продукт к отправке', 'Из концентрата удаляют часть воды. Медный концентрат отправляют на дальнейшую металлургическую переработку. Именно этот продукт выпускает «Амур Минералс».', 'process-filter.jpg', 'Оборудование фильтрации концентрата', 'ГОК «Перевальный» · Амур Золото', PROCESS_PHOTOS, 'Обогащённый продукт → концентрат'),
]


def ore_journey(cite):
    navigation = ''.join(f'<a href="#ore-{key}" data-ore-link="{key}">{title}</a>' for key, title, *_ in STAGES)
    steps = []
    for key, title, heading, description, image, alt, credit, source, change in STAGES:
        steps.append(f'''<article class="ore-step" id="ore-{key}" data-ore-step="{key}" data-image="assets/{image}" data-alt="{alt}" data-credit="{html.escape(credit)}" data-source="{source}">
            <span class="eyebrow">{title}</span><h2>{heading}</h2><p>{description}</p>
            <div class="ore-change">{change}</div>
            <figure class="ore-inline"><img src="assets/{image}" alt="{alt}" loading="lazy"><figcaption><a href="{source}">{credit}</a></figcaption></figure></article>''')
    first = STAGES[0]
    return f'''<section class="ore-experience" id="ore-journey"><header class="interaction-heading"><span class="eyebrow">Путь руды</span><h2>От горной породы к концентрату</h2><p>Прокручивайте страницу или выберите этап</p><p class="interaction-credit">Технологическая последовательность — учебная модель. Геология и продукт Малмыжа{cite(1,2,7)}. Фотографии оборудования — ГОК «Перевальный».</p></header>
        <div class="ore-layout"><div class="ore-visual"><nav class="ore-nav" aria-label="Этапы переработки">{navigation}</nav>
        <figure><img id="ore-image" src="assets/{first[4]}" alt="{first[5]}"><figcaption><span id="ore-current">Карьер</span> · <a id="ore-credit" href="{first[7]}">{first[6]}</a></figcaption></figure><progress id="ore-progress" max="6" value="1" aria-label="Пройденные этапы"></progress></div><div class="ore-steps">{''.join(steps)}</div></div></section>'''


def geology_explorer(cite):
    features = [
        ('host', 'Осадочные породы', 'Песчаники и алевролиты', 'Малмыжское рудное поле расположено в толще осадочных пород, преимущественно песчаников. Среди них встречаются алевролиты. Эту толщу пересекают магматические интрузии.', 'malmyzh-rock.webp', 'Горные породы на площадке Малмыжа', 1, 'sources.html#source-9', 'Фото · АО «Тех Взрыв Инвест»'),
        ('intrusion', 'Интрузия', 'Магма, застывшая в глубине', 'Интрузия — тело магматических пород, образовавшееся при застывании магмы внутри земной коры. В Малмыжском рудном поле описаны многочисленные интрузивные тела позднемелового возраста.', 'porphyry-section.svg', 'Положение интрузии в концептуальной порфировой системе', 1, 'sources.html#source-7', 'Модель порфировой системы · USGS'),
        ('veins', 'Рудные прожилки', 'Минералы вдоль трещин', 'В порфировых системах горячие растворы движутся по трещинам. При изменении условий из них осаждаются минералы. Халькопирит — сульфид меди и железа, присутствующий в рудах Малмыжа.', 'chalcopyrite.png', 'Кристаллы халькопирита, образец из Канзаса', 7, 'https://commons.wikimedia.org/wiki/File:Chalcopyrite-199453.jpg', 'Канзас, США · Rob Lavinsky, iRocks.com · CC BY-SA 3.0'),
    ]
    buttons = ''.join(f'<button type="button" class="geo-point geo-point-{key}" data-geo-target="{key}" aria-controls="geo-{key}"><span>{label}</span></button>' for key, label, *_ in features)
    panels = []
    for key, label, title, description, image, alt, source, credit_url, credit in features:
        panels.append(f'''<article class="geo-panel" id="geo-{key}"><div><span class="eyebrow">{label}</span><h3>{title}</h3><p>{description}{cite(source,1) if source != 1 else cite(1)}</p></div><figure><img src="assets/{image}" alt="{alt}" loading="lazy"><figcaption><a href="{credit_url}">{credit}</a></figcaption></figure></article>''')
    return f'''<section class="geology-explorer" id="geology-explorer"><div class="geo-canvas"><img src="assets/porphyry-section.svg" alt="Концептуальная схема порфировой системы"><div class="geo-points" aria-label="Изучить строение">{buttons}</div></div><p class="interaction-credit">Выберите объект на схеме · Концептуальная модель порфировой системы{cite(7)}</p><div class="geo-panels">{''.join(panels)}</div></section>'''


def copper_calculator(cite):
    return f'''<section class="copper-calculator" id="copper-calculator"><div class="calculator-intro"><span class="eyebrow">Руда и металл</span><h2>Сколько меди содержится в руде</h2><p>Среднее содержание меди — около 0,35% по оценке Роснедр 2021 года{cite(1)}. Выберите массу руды и посмотрите состав.</p><div class="calculator-composition"><span class="composition-main">Руда</span><span class="composition-cu">Cu</span></div></div>
        <div class="calculator-controls"><label for="ore-mass">Масса руды, тонн</label><input id="ore-mass" type="number" inputmode="decimal" min="0" max="10000" step="0.1" value="10" aria-describedby="ore-mass-help"><p id="ore-mass-help">От 0 до 10 000 тонн</p><input id="ore-mass-range" type="range" min="0" max="10000" step="0.1" value="10" aria-label="Масса руды в тоннах"><div class="mass-presets" aria-label="Выбрать массу">{''.join(f'<button type="button" data-mass="{mass}">{mass:,} т</button>'.replace(',', ' ') for mass in [1,10,100,1000])}</div><div class="calculator-result" aria-live="polite" aria-atomic="true"><span>Содержащаяся медь</span><strong><output id="copper-mass" for="ore-mass">35</output> <small>кг</small></strong><p>Другие компоненты <output id="other-mass" for="ore-mass">9 965</output> кг</p></div><p class="calculator-formula">Масса руды × 1 000 × 0,0035 = масса меди в кг</p><p class="interaction-credit">Расчёт состава руды до технологических потерь при переработке</p></div></section>'''


def install(g):
    pages = g['PAGES']
    cite = g['cite']
    for slug in ('production', 'about', 'resources', 'index'):
        title, original = pages[slug]

        def enhanced(body=original, page=slug):
            content = body()
            if page == 'production':
                content = re.sub(r'<div class="stage-grid">.*?</div>', ore_journey(cite), content, count=1, flags=re.S)
            elif page == 'about':
                content = re.sub(r'<figure class="geo-figure">.*?</figure>', geology_explorer(cite), content, count=1, flags=re.S)
            elif page == 'resources':
                content = re.sub(r'<section class="grade-visual">.*?</section>', copper_calculator(cite), content, count=1, flags=re.S)
            else:
                links = '<nav class="explore-links" aria-label="Интерактивные разделы"><a href="production.html#ore-journey"><span>Проследить путь</span><strong>От руды к концентрату ↗</strong></a><a href="about.html#geology-explorer"><span>Исследовать строение</span><strong>Геология в деталях ↗</strong></a><a href="resources.html#copper-calculator"><span>Рассчитать состав</span><strong>Сколько меди в руде ↗</strong></a></nav>'
                content = content.replace('<section class="editorial-intro">', links + '<section class="editorial-intro">', 1)
            return content

        pages[slug] = (title, enhanced)

    original_render = g['render']

    def render(slug):
        return original_render(slug).replace('</head>', '<link rel="stylesheet" href="assets/interactions.css?v=1"><script type="module" src="assets/interactions.js?v=1"></script></head>')

    g['render'] = render
