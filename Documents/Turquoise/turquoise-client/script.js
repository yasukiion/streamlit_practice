document.getElementById('email-form').addEventListener('submit', function(e) {
  e.preventDefault();  // フォームのデフォルトの送信を阻止
  const email = document.getElementById('email').value;
  fetch('/api/subscribers/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email: email })
  })
  .then(response => response.json())
  .then(data => {
    alert('Email registered successfully');
    // 任意でメールアドレスの入力フィールドをクリア
    document.getElementById('email').value = '';
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error registering email');
  });
});

