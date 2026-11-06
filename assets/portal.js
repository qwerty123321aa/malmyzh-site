import {initGallery} from './gallery.js';
const toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('#site-nav');
function closeMenu(){toggle?.setAttribute('aria-expanded','false');nav?.classList.remove('is-open');}
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(toggle?.getAttribute('aria-expanded')==='true'){closeMenu();toggle.focus();}document.querySelector('.more-nav')?.removeAttribute('open');}});
initGallery();
if(document.querySelector('#search-form'))import('./search.js');
const sourceCards=[...document.querySelectorAll('.source')];
if(sourceCards.length){const query=document.querySelector('#source-query'),filter=document.querySelector('#source-filter'),status=document.querySelector('#source-status');function update(){let count=0;sourceCards.forEach(c=>{c.hidden=!(c.textContent.toLowerCase().includes(query.value.toLowerCase())&&(!filter.value||c.dataset.category===filter.value));if(!c.hidden)count++;});status.textContent=count?`Источников: ${count}`:'Источников по запросу не найдено.';}query.addEventListener('input',update);filter.addEventListener('change',update);window.addEventListener('hashchange',()=>{query.value='';filter.value='';update();document.getElementById(location.hash.slice(1))?.scrollIntoView();});update();}
const map=document.querySelector('#location-map');document.querySelectorAll('[data-map-src]').forEach(b=>b.addEventListener('click',()=>{map.src=b.dataset.mapSrc;document.querySelectorAll('[data-map-src]').forEach(v=>{v.setAttribute('aria-pressed',String(v===b));v.classList.toggle('active',v===b);});}));
function whenVisible(element,fn){if(!element)return;const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){observer.disconnect();fn();}},{rootMargin:'150px'});observer.observe(element);}
whenVisible(document.querySelector('#leaflet-map'),()=>import('./map.js'));
whenVisible(document.querySelector('.reserves-chart'),()=>import('./charts.js'));
