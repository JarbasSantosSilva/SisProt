document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');

  form.addEventListener('submit', function(e) {
    const descricao = document.querySelector('textarea[name="descricao"]').value.trim();

    if (descricao.length < 10) {
      alert('A descrição deve ter pelo menos 10 caracteres.');
      e.preventDefault();
      return;
    }
  });
});