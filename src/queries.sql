
-- Top 10 
SELECT p.id_produto,
       dp.nome,
       dp.categoria,
       SUM(p.recomendacao_final) AS total_recomendado
FROM fato_playlist_alocacoes p
LEFT JOIN dim_produtos dp ON dp.id_produto = p.id_produto
GROUP BY p.id_produto, dp.nome, dp.categoria
ORDER BY total_recomendado DESC
LIMIT 10;


-- Ranking por loja e categoria 
SELECT id_loja, categoria,
       SUM(recomendacao_final) AS recomendado
FROM fato_playlist_alocacoes
GROUP BY id_loja, categoria
ORDER BY id_loja, recomendado DESC;
