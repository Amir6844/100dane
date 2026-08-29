// 100dane — vanilla JS + HTMX helpers
function persianConfirm(msg){ return confirm(msg || 'آیا مطمئن هستید؟'); }
function faDigits(n){ return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]); }
// seed burst on save
function seedBurst(btn){
  btn.animate([{transform:'scale(1)'},{transform:'scale(1.04)'},{transform:'scale(1)'}],{duration:320});
}
// pom loading
function showLoading(btn){
  const orig=btn.innerHTML;
  btn.innerHTML='<span class="pom-spinner inline-block w-4 h-4 border-white border-t-transparent"></span> در حال پردازش...';
  btn.disabled=true;
  return ()=>{ btn.innerHTML=orig; btn.disabled=false; };
}
// copy helper
async function copyText(t, feedbackEl){
  await navigator.clipboard.writeText(t);
  if(feedbackEl){ const o=feedbackEl.textContent; feedbackEl.textContent='کپی شد ✓'; setTimeout(()=>feedbackEl.textContent=o,1500); }
}
// HTMX toast for deletes with Persian confirm
document.addEventListener('click', e=>{
  const del=e.target.closest('[data-confirm]');
  if(del && !confirm(del.dataset.confirm || 'حذف شود؟')) e.preventDefault();
});
