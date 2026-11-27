(() => {
  const video = document.querySelector('#hero-video');
  if (video) {
    const list = (video.dataset.videos || '').split('|').filter(Boolean);
    let index = 0;
    video.addEventListener('ended', () => {
      if (!list.length) return;
      index = (index + 1) % list.length;
      video.src = list[index];
      video.play().catch(() => {});
    });
  }
  const menuButton = document.querySelector('.menu');
  const mobileNav = document.querySelector('#mobile-nav');
  const setMenu = (open) => {
    if (!menuButton || !mobileNav) return;
    menuButton.setAttribute('aria-expanded', String(open));
    mobileNav.setAttribute('aria-hidden', String(!open));
    mobileNav.classList.toggle('open', open);
  };
  menuButton?.addEventListener('click', () => setMenu(!mobileNav?.classList.contains('open')));
  mobileNav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));
  const chat = document.querySelector('#chat'), openers = document.querySelectorAll('[data-open-chat]'), closer = document.querySelector('[data-close-chat]');
  openers.forEach((button) => button.addEventListener('click', () => chat?.classList.add('open')));
  closer?.addEventListener('click', () => chat?.classList.remove('open'));
  const messages = document.querySelector('#chat-messages'), form = document.querySelector('#chat-form');
  const add = (text, kind) => { const p = document.createElement('p'); p.className = kind; p.textContent = text; messages?.append(p); messages?.scrollTo({ top: messages.scrollHeight, behavior: 'smooth' }); };
  async function send(message) {
    add(message, 'user'); if (form?.elements.message) form.elements.message.value = '';
    const body = new FormData(); body.append('message', message); body.append('csrf', form?.querySelector('[name=csrf]')?.value || '');
    try { const response = await fetch((window.APP_BASE || '') + '/api/chat.php', { method: 'POST', body }); const result = await response.json(); add(result.answer || 'تعذر الرد الآن.', 'assistant'); } catch { add('تعذر الرد الآن. حاول مرة أخرى.', 'assistant'); }
  }
  form?.addEventListener('submit', (event) => { event.preventDefault(); const message = form.elements.message.value.trim(); if (message) send(message); });
  document.querySelectorAll('.quick button').forEach((button) => button.addEventListener('click', () => send(button.textContent)));
  const quote = document.querySelector('#quote-form');
  quote?.addEventListener('submit', async (event) => { event.preventDefault(); const feedback = document.querySelector('#quote-feedback'); if (feedback) feedback.textContent = 'يجري الإرسال...'; try { const response = await fetch((window.APP_BASE || '') + '/api/quote.php', { method: 'POST', body: new FormData(quote) }); const result = await response.json(); if (feedback) feedback.textContent = result.message || result.error || 'تعذر الإرسال.'; if (result.success) quote.reset(); } catch { if (feedback) feedback.textContent = 'تعذر الاتصال. حاول مرة أخرى.'; } });
})();
