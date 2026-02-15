const providerList = document.getElementById('providerList');
const loadProvidersBtn = document.getElementById('loadProviders');
const appointmentForm = document.getElementById('appointmentForm');
const result = document.getElementById('result');

loadProvidersBtn.addEventListener('click', async () => {
  providerList.innerHTML = '<li>Loading...</li>';
  const res = await fetch('/api/providers');
  const data = await res.json();

  providerList.innerHTML = '';
  data.items.forEach((p) => {
    const li = document.createElement('li');
    li.textContent = `${p.name} (${p.specialty}) - ${p.country} - ${p.consultation_fee} ${p.currency}`;
    providerList.appendChild(li);
  });
});

appointmentForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = new FormData(appointmentForm);
  const payload = Object.fromEntries(form.entries());

  const res = await fetch('/api/appointments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    result.textContent = `Error: ${JSON.stringify(data)}`;
    return;
  }
  result.textContent = `Appointment created: ${data.id}`;
  appointmentForm.reset();
});
