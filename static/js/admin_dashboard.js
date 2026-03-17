// Small JS for admin dashboard interactions
document.addEventListener('DOMContentLoaded', function(){
  const refreshBtn = document.getElementById('refresh-btn');
  if(refreshBtn){
    refreshBtn.addEventListener('click', ()=> location.reload());
  }

  // confirm deletes and destructive actions
  document.querySelectorAll('form.inline-form').forEach(form=>{
    form.addEventListener('submit', (e)=>{
      const ok = confirm('Are you sure you want to perform this action?');
      if(!ok) e.preventDefault();
    });
  });

  // subtle hover animations
  document.querySelectorAll('.table tr').forEach(row=>{
    row.addEventListener('mouseenter', ()=> row.style.transform='translateY(-3px)');
    row.addEventListener('mouseleave', ()=> row.style.transform='none');
  });
});
