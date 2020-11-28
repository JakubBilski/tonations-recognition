async function postJsonData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return response.json();
}

async function postFormData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST',
    body: data
  });
  return response.json();
}
