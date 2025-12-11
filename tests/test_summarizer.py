import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.summarizer import Summarizer

class TestSummarizer:
    
    def setup_method(self):
        self.summarizer = Summarizer()
    
    @patch('app.services.summarizer.ChatOllama')
    @patch('app.services.summarizer.settings')
    def test_summarize_with_ollama(self, mock_settings, mock_chat_ollama):
        """Testa summarização usando Ollama"""
        # Setup
        mock_settings.MODEL = "OLLAMA"
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Este é um resumo do artigo."
        mock_model.invoke.return_value = mock_response
        mock_chat_ollama.return_value = mock_model
        
        # Execute
        text = "Este é um longo artigo sobre Python que precisa ser resumido."
        word_count = 10
        result = self.summarizer.summarize(text, word_count)
        
        # Assert
        assert result == "Este é um resumo do artigo."
        mock_chat_ollama.assert_called_once_with(model="mistral", temperature=0)
        mock_model.invoke.assert_called_once()
    
    @patch('app.services.summarizer.init_chat_model')
    @patch('app.services.summarizer.settings')
    def test_summarize_with_gpt(self, mock_settings, mock_init_chat_model):
        """Testa summarização usando GPT"""
        # Setup
        mock_settings.MODEL = "GPT"
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Este é um resumo gerado pelo GPT."
        mock_model.invoke.return_value = mock_response
        mock_init_chat_model.return_value = mock_model
        
        # Execute
        text = "Este é um longo artigo sobre Python que precisa ser resumido."
        word_count = 10
        result = self.summarizer.summarize(text, word_count)
        
        # Assert
        assert result == "Este é um resumo gerado pelo GPT."
        mock_init_chat_model.assert_called_once_with(model="gpt-4.1", max_tokens=word_count)
        mock_model.invoke.assert_called_once()
    
    @patch('app.services.summarizer.ChatOllama')
    @patch('app.services.summarizer.settings')
    def test_summarize_calls_model_with_correct_messages(self, mock_settings, mock_chat_ollama):
        """Testa se as mensagens corretas são passadas para o modelo"""
        # Setup
        mock_settings.MODEL = "OLLAMA"
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Resumo"
        mock_model.invoke.return_value = mock_response
        mock_chat_ollama.return_value = mock_model
        
        # Execute
        text = "Artigo de teste"
        word_count = 5
        self.summarizer.summarize(text, word_count)
        
        # Assert
        call_args = mock_model.invoke.call_args[0][0]
        assert len(call_args) == 2
        assert "assistente especializado" in call_args[0].content
        assert str(word_count) in call_args[1].content
        assert text in call_args[1].content
    
    @patch('app.services.summarizer.ChatOllama')
    @patch('app.services.summarizer.settings')
    def test_summarize_with_different_word_counts(self, mock_settings, mock_chat_ollama):
        """Testa summarização com diferentes tamanhos de resumo"""
        # Setup
        mock_settings.MODEL = "OLLAMA"
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Resumo"
        mock_model.invoke.return_value = mock_response
        mock_chat_ollama.return_value = mock_model
        
        word_counts = [5, 10, 50, 100]
        text = "Texto de exemplo"
        
        for word_count in word_counts:
            result = self.summarizer.summarize(text, word_count)
            assert result == "Resumo"
            
            # Verifica se o word_count está na mensagem
            call_args = mock_model.invoke.call_args[0][0]
            assert str(word_count) in call_args[1].content
    
    @patch('app.services.summarizer.ChatOllama')
    @patch('app.services.summarizer.settings')
    def test_summarize_with_empty_text(self, mock_settings, mock_chat_ollama):
        """Testa summarização com texto vazio"""
        # Setup
        mock_settings.MODEL = "OLLAMA"
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Sem conteúdo para resumir."
        mock_model.invoke.return_value = mock_response
        mock_chat_ollama.return_value = mock_model
        
        # Execute
        result = self.summarizer.summarize("", 10)
        
        # Assert
        assert result == "Sem conteúdo para resumir."
    
    @patch('app.services.summarizer.ChatOllama')
    @patch('app.services.summarizer.settings')
    def test_summarize_with_long_text(self, mock_settings, mock_chat_ollama):
        """Testa summarização com texto longo"""
        # Setup
        mock_settings.MODEL = "OLLAMA"
        mock_model = Mock()
        mock_response = Mock()
        mock_response.content = "Resumo conciso do texto longo."
        mock_model.invoke.return_value = mock_response
        mock_chat_ollama.return_value = mock_model
        
        # Execute
        long_text = "Lorem ipsum " * 1000
        result = self.summarizer.summarize(long_text, 20)
        
        # Assert
        assert result == "Resumo conciso do texto longo."
        assert mock_model.invoke.called
