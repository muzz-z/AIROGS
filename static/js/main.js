// Site-wide micro-interactions: fade-in, header shadow, toasts, copy links
document.addEventListener('DOMContentLoaded', function(){
	// Fade in main content
	document.querySelectorAll('.card, .panel, .container, .card-body').forEach((el,i)=>{
		el.classList.add('fade-up');
		el.style.animationDelay = (i*40)+'ms';
	});

	// Header shadow on scroll (if navbar present)
	const header = document.querySelector('.navbar');
	if(header){
		window.addEventListener('scroll', ()=>{
			if(window.scrollY>10) header.classList.add('scrolled'); else header.classList.remove('scrolled');
		});
	}

	// Simple toast helper: data-toast="message"
	document.querySelectorAll('[data-toast]').forEach(btn=>{
		btn.addEventListener('click', e=>{
			const msg = btn.getAttribute('data-toast');
			showToast(msg);
		});
	});
});

function showToast(msg, timeout=3000){
	const t = document.createElement('div');
	t.className='toast fade-up';
	t.textContent = msg;
	document.body.appendChild(t);
	setTimeout(()=> t.style.opacity = '1', 20);
	setTimeout(()=>{ t.style.opacity='0'; setTimeout(()=>t.remove(),400); }, timeout);
}

// Copy to clipboard helper for links with data-copy
document.addEventListener('click', function(e){
	const el = e.target.closest('[data-copy]');
	if(!el) return;
	const text = el.getAttribute('data-copy');
	navigator.clipboard?.writeText(text).then(()=> showToast('Copied link'), ()=> showToast('Copy failed'));
});

// small helper to preview image (fallback in case inline didn't bind)
window.previewSelectedFile = function(inputId, previewId){
	const input = document.getElementById(inputId);
	const preview = document.getElementById(previewId);
	if(!input || !preview) return;
	input.addEventListener('change', e=>{
		const file = e.target.files[0];
		if(!file){ preview.style.display='none'; return; }
		const reader = new FileReader();
		reader.onload = ev => { preview.src = ev.target.result; preview.style.display='block'; }
		reader.readAsDataURL(file);
	});
}
