import pytest
from unittest.mock import Mock, patch
from app.services.scrapper import Scrapper

class TestScrapper:
    
    def setup_method(self):
        self.scrapper = Scrapper()
    
    def test_validate_url_valid(self):
        """Testa se uma URL válida da Wikipedia é aceita"""
        valid_url = "https://pt.wikipedia.org/wiki/Python"
        assert self.scrapper.validate_url(valid_url) is True
    
    def test_validate_url_invalid(self):
        """Testa se uma URL inválida é rejeitada"""
        invalid_urls = [
            "https://en.wikipedia.org/wiki/Python",
            "https://www.google.com",
            "http://pt.wikipedia.org/wiki/Python",
            "https://wikipedia.org/wiki/Python"
        ]
        for url in invalid_urls:
            assert self.scrapper.validate_url(url) is False
    
    def test_create_url(self):
        """Testa a criação de URL da Wikipedia"""
        page_name = "Python_(linguagem_de_programação)"
        expected_url = f"https://pt.wikipedia.org/wiki/{page_name}"
        assert self.scrapper.create_url(page_name) == expected_url
    
    @patch('app.services.scrapper.requests.get')
    def test_scrap_page_success(self, mock_get):
        """Testa scraping bem-sucedido de uma página válida"""
        mock_response = Mock()
        mock_response.content = (
            "<html>"
            "<body>"
            "<p>Python e uma linguagem de programacao.</p>"
            "<p>Foi criada por Guido van Rossum.</p>"
            "</body>"
            "</html>"
        ).encode('utf-8')
        mock_get.return_value = mock_response
        
        url = "https://pt.wikipedia.org/wiki/Python"
        result = self.scrapper.scrap_page(url)
        
        assert "Python e uma linguagem de programacao" in result
        assert "Guido van Rossum" in result
        mock_get.assert_called_once_with(url, headers={"User-Agent": "Mozilla/5.0"})
    
    def test_scrap_page_invalid_url(self):
        """Testa scraping com URL inválida"""
        invalid_url = "https://www.google.com"
        with pytest.raises(ValueError, match="URL must be from pt.wikipedia.org/wiki"):
            self.scrapper.scrap_page(invalid_url)
    
    @patch('app.services.scrapper.requests.get')
    def test_scrap_page_not_found(self, mock_get):
        """Testa scraping de página inexistente"""
        mock_response = Mock()
        mock_response.content = (
            "<html>"
            "<body>"
            "<p>A Wikipédia não possui um artigo com este nome exato.</p>"
            "</body>"
            "</html>"
        ).encode('utf-8')
        mock_get.return_value = mock_response
        
        url = "https://pt.wikipedia.org/wiki/PaginaInexistente"
        with pytest.raises(ValueError, match="There is wikipedia page for this link"):
            self.scrapper.scrap_page(url)
    
    @patch('app.services.scrapper.requests.get')
    def test_scrap_page_empty_content(self, mock_get):
        """Testa scraping de página sem parágrafos"""
        mock_response = Mock()
        mock_response.content = "<html><body></body></html>".encode('utf-8')
        mock_get.return_value = mock_response
        
        url = "https://pt.wikipedia.org/wiki/Test"
        result = self.scrapper.scrap_page(url)
        
        assert result == ""
    
    @patch('app.services.scrapper.requests.get')
    def test_scrap_page_multiple_paragraphs(self, mock_get):
        """Testa scraping com múltiplos parágrafos"""
        mock_response = Mock()
        mock_response.content = (
            "<html>"
            "<body>"
            "<p>Primeiro paragrafo.</p>"
            "<p>Segundo paragrafo.</p>"
            "<p>Terceiro paragrafo.</p>"
            "</body>"
            "</html>"
        ).encode('utf-8')
        mock_get.return_value = mock_response
        
        url = "https://pt.wikipedia.org/wiki/Test"
        result = self.scrapper.scrap_page(url)
        
        assert "Primeiro paragrafo" in result
        assert "Segundo paragrafo" in result
        assert "Terceiro paragrafo" in result
