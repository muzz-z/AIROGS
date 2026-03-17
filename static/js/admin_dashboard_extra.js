// Extra interactions for admin dashboard
document.addEventListener('click', function(e){
  if(e.target.matches('.btn.loading')){
    e.target.classList.add('busy');
  }
});
// small helper to open links in new window for downloads
document.addEventListener('DOMContentLoaded', ()=>{
  const dl = document.getElementById('btn-export');
  if(dl){dl.addEventListener('click', ()=>{setTimeout(()=>{window.location.href = dl.getAttribute('href')||dl.dataset.href},300)})}
});