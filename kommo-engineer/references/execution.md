# Execução segura e validável
1. Expresse o resultado e seu critério verificável.
2. Escolha procedimento e método viável; verifique acessos atuais.
3. Prepare inputs, diff previsto e eventual rollback.
4. Solicite autorização proporcional para alterações críticas.
5. Execute apenas com ferramenta disponível e suportada.
6. Releia recurso no destino; capture evidência sanitizada.
7. Registre evento/aceite na meta correspondente.
8. Se incerto, pare em `blocked`, não reporte sucesso presumido.

Sem API/navegador disponíveis, dê instruções de clique baseadas em tela/documentação verificadas,
não crie endpoints privados. Em produção, não faça disparos massivos sem escopo autorizado.
Use `goal record` para progresso e `goal accept` para ligar arquivo de evidência.
`goal close` exige todos os critérios verificados.
