-- Script de inicialização do banco de dados
-- Cria a tabela summaries se ela não existir

CREATE TABLE IF NOT EXISTS summaries (
    id SERIAL PRIMARY KEY,
    url VARCHAR NOT NULL UNIQUE,
    summary_data TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Cria índice na coluna url para buscas mais rápidas
CREATE INDEX IF NOT EXISTS idx_summaries_url ON summaries(url);

-- Função para atualizar automaticamente o campo updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at automaticamente
DROP TRIGGER IF EXISTS update_summaries_updated_at ON summaries;
CREATE TRIGGER update_summaries_updated_at
    BEFORE UPDATE ON summaries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
