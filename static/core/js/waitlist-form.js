// Waitlist form submission.
(function () {
  const configElement = document.getElementById('landing-config');
  const landingConfig = configElement ? JSON.parse(configElement.textContent) : {};
  const waitlistEndpoint = landingConfig.waitlistEndpoint || '/waitlist/join/';
  const container = document.getElementById('form-container');

  if (!container) return;

  function getInput()  { return document.getElementById('email-input'); }
  function getBtn()    { return document.getElementById('submit-btn'); }

  function triggerErrorState(input) {
    const original = input.placeholder;
    input.classList.add('input-error');
    input.placeholder = 'Enter a valid email';
    input.style.setProperty('--placeholder-color', '#E24B4A');
    setTimeout(() => {
      input.classList.remove('input-error');
      input.placeholder = original;
      input.value = '';
    }, 1200);
  }

  async function handleSubmit() {
    const input = getInput();
    const btn   = getBtn();
    if (!input || !btn) return;

    const email = input.value.trim();
    if (!email) { triggerErrorState(input); return; }

    btn.disabled = true;
    btn.textContent = 'Sending...';

    try {
      const res  = await fetch(waitlistEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (res.ok || res.status === 200) {
        container.innerHTML = '<p class="form-success">&check; You\'re on the list. Expect an email from joe@attribu.io within 48 hours.</p>';
      } else {
        triggerErrorState(input);
        btn.disabled = false;
        btn.textContent = 'Notify me';
      }
    } catch {
      btn.disabled = false;
      btn.textContent = 'Notify me';
      triggerErrorState(input);
    }
  }

  container.addEventListener('click', e => { if (e.target.id === 'submit-btn') handleSubmit(); });
  container.addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.id === 'email-input') handleSubmit(); });
})();
