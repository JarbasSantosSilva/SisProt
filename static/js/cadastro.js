document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');

  form.addEventListener('submit', function(e) {
    const nome = document.querySelector('input[name="nome"]').value.trim();
    const cpf = document.querySelector('input[name="cpf"]').value.trim();
    const email = document.querySelector('input[name="email"]').value.trim();
    const senha = document.querySelector('input[name="senha"]').value;

    if (nome.length < 3) {
      alert('Nome deve ter pelo menos 3 caracteres.');
      e.preventDefault();
      return;
    }

    if (cpf.length < 11) {
      alert('CPF inválido.');
      e.preventDefault();
      return;
    }

    if (!email.includes('@')) {
      alert('E-mail inválido.');
      e.preventDefault();
      return;
    }

    if (senha.length < 6) {
      alert('A senha deve ter pelo menos 6 caracteres.');
      e.preventDefault();
      return;
    }
  });
});