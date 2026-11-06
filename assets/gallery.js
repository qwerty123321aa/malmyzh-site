export function initGallery(){
 const dialog=document.querySelector('#photo-dialog');if(!dialog)return;
 let buttons=[...document.querySelectorAll('[data-photo]')],current=0,trigger=null;
 const image=dialog.querySelector('img'),caption=dialog.querySelector('p');
 function show(i){current=(i+buttons.length)%buttons.length;const b=buttons[current];image.src=b.dataset.photo;image.alt=b.querySelector('img').alt;caption.replaceChildren();const count=document.createElement('span');count.textContent=`${current+1} / ${buttons.length} · `;caption.append(count,b.closest('figure').querySelector('figcaption').cloneNode(true));}
 buttons.forEach(b=>b.addEventListener('click',()=>{trigger=b;buttons=[...document.querySelectorAll('[data-photo]')].filter(v=>!v.closest('[hidden]'));show(buttons.indexOf(b));dialog.showModal();}));
 dialog.querySelector('[data-prev]').addEventListener('click',()=>show(current-1));dialog.querySelector('[data-next]').addEventListener('click',()=>show(current+1));
 dialog.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();show(current+1);}if(e.key==='ArrowLeft'){e.preventDefault();show(current-1);}});
 dialog.addEventListener('close',()=>{if(document.fullscreenElement)document.exitFullscreen?.();trigger?.focus();});
 const full=dialog.querySelector('[data-fullscreen]');if(!dialog.requestFullscreen)full.hidden=true;else full.addEventListener('click',()=>{(document.fullscreenElement?document.exitFullscreen():dialog.requestFullscreen()).catch(()=>{full.textContent='Полный экран недоступен';});});
 const filter=document.querySelector('#gallery-filter');filter?.addEventListener('change',()=>document.querySelectorAll('[data-gallery-category]').forEach(el=>el.hidden=!!filter.value&&el.dataset.galleryCategory!==filter.value));
}
