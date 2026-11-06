const target=document.querySelector('#leaflet-map');
const css=document.createElement('link');css.rel='stylesheet';css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';document.head.append(css);
const script=document.createElement('script');script.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
script.onload=()=>{
 const L=window.L,map=L.map(target,{scrollWheelZoom:false}).setView([49.9338,136.918],9);
 const base=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'}).addTo(map);
 const marker=L.circleMarker([49.9338,136.918],{radius:10,color:'#172321',fillColor:'#526c58',fillOpacity:1}).bindPopup('<strong>Малмыжское месторождение</strong><p>Ориентировочная точка: 49.9338, 136.918. Не граница лицензии и не въезд на предприятие.</p><a href="sources.html#source-10">Каталог координат и ограничения</a>');
 const group=L.layerGroup([marker]).addTo(map);
 const cities=L.layerGroup([['Хабаровск',48.48,135.07],['Комсомольск-на-Амуре',50.55,137.00]].map(([name,lat,lon])=>L.circleMarker([lat,lon],{radius:6,color:'#172321',fillColor:'#f0ede5',fillOpacity:1}).bindPopup(`<strong>${name}</strong><p>${lat}° с. ш., ${lon}° в. д. Округлённый ориентир города.</p><a href="https://www.unn.ru/site/images/docs/science/astrocalendar_2019.pdf" target="_blank" rel="noopener">Координаты городов, ННГУ</a>`))).addTo(map);
 L.control.layers({'OpenStreetMap':base},{'Малмыж — ориентир':group,'Города Приамурья':cities},{collapsed:true}).addTo(map);marker.openPopup();
 const button=document.createElement('button');button.type='button';button.textContent='Показать Приамурье';button.className='map-view';button.addEventListener('click',()=>map.fitBounds([[48.2,134.7],[51.1,138.4]]));target.after(button);
};
script.onerror=()=>{target.textContent='Интерактивный слой не загрузился. Используйте карту OpenStreetMap ниже.';};document.head.append(script);
