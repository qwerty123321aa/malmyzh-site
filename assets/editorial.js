const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('#site-nav');
if(toggle&&nav){
 toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
 document.addEventListener('keydown',event=>{if(event.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){toggle.setAttribute('aria-expanded','false');nav.classList.remove('is-open');toggle.focus();}});
}
const photoDialog=document.querySelector('#photo-dialog');
let photoTrigger=null;
if(photoDialog){
 document.querySelectorAll('[data-photo]').forEach(button=>button.addEventListener('click',()=>{
  photoTrigger=button;
  const image=photoDialog.querySelector('img');
  image.src=button.dataset.photo;image.alt=button.querySelector('img').alt;
  photoDialog.querySelector('p').textContent=button.closest('figure').querySelector('figcaption').innerText;
  photoDialog.showModal();
 }));
 photoDialog.querySelector('.dialog-close').addEventListener('click',()=>photoDialog.close());
 photoDialog.addEventListener('click',event=>{if(event.target===photoDialog)photoDialog.close();});
 photoDialog.addEventListener('close',()=>{if(photoTrigger)photoTrigger.focus();});
}
const map=document.querySelector('#location-map');
if(map){
 document.querySelectorAll('[data-map-src]').forEach(button=>button.addEventListener('click',()=>{
  map.src=button.dataset.mapSrc;
  document.querySelectorAll('[data-map-src]').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-pressed',String(item===button));});
 }));
}
