document.addEventListener('DOMContentLoaded', function() {
  fetch('/api/solicitacoes')
    .then(function(response) {
      return response.json();
    })
    .then(function(dados) {
      const tabela = document.getElementById('tabela-solicitacoes');
      tabela.innerHTML = '';

      if (dados.length === 0) {
        tabela.innerHTML = '<tr><td colspan="5">Nenhuma solicitação encontrada.</td></tr>';
        return;
      }

      dados.forEach(function(s) {
        tabela.innerHTML += `
          <tr>
            <td>${s.protocolo}</td>
            <td>${s.tipo}</td>
            <td>${s.descricao}</td>
            <td>${s.status}</td>
            <td>${s.data_abertura}</td>
            <td><a href="/historico/${s.id}">Ver histórico</a></td>
          </tr>
        `;
      });
    })
    .catch(function(erro) {
      console.error('Erro ao carregar solicitações:', erro);
    });
});