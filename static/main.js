document.getElementById('start').addEventListener('click', () => {
  fetch('/istihare')
    .then(r => r.json())
    .then(data => {
      const res = `Seçilen sağ sayfa: ${data.right_page}\n` +
                  `Allah sayısı: ${data.count}\n` +
                  `Gidilen sayfa: ${data.target_page}\n` +
                  `Satır: ${data.line_number}\n` +
                  `İlk harf: ${data.letter}\n` +
                  `Yorum: ${data.meaning}`;
      document.getElementById('result').textContent = res;
    })
    .catch(err => {
      document.getElementById('result').textContent = 'Hata: ' + err;
    });
});
