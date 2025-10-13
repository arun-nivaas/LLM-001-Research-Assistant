import fitz  # PyMuPDF
import pdfplumber
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TextBlock:
    """Text extraction result."""
    page: int
    text: str
    char_count: int = 0
    
    def __post_init__(self):
        self.char_count = len(self.text)


@dataclass
class TableBlock:
    """Table extraction result."""
    page: int
    table_index: int
    data: List[List[str]]
    rows: int = 0
    cols: int = 0
    
    def __post_init__(self):
        if self.data:
            self.rows = len(self.data)
            self.cols = max(len(row) for row in self.data) if self.data else 0


class PDFExtractionPipeline:
    """Optimized PDF extraction for text and tables."""
    
    MAX_WORKERS = 4
    TIMEOUT = 300
    
    def __init__(self, pdf_path: str, max_workers: int = MAX_WORKERS):
        """Initialize pipeline."""
        self.pdf_path = Path(pdf_path)
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        self.max_workers = min(max_workers, 4)
        self.texts: List[TextBlock] = []
        self.tables: List[TableBlock] = []
        self.metadata = {
            'file_path': str(self.pdf_path),
            'file_size_mb': round(self.pdf_path.stat().st_size / (1024 * 1024), 2),
            'total_pages': 0
        }
        
        logger.info(f"Pipeline initialized for: {self.pdf_path.name}")
    
    def _extract_text_page(self, page_num: int) -> Optional[TextBlock]:
        """Extract text from a single page."""
        try:
            doc = fitz.open(str(self.pdf_path))
            page = doc[page_num]
            text = page.get_text("text")
            doc.close()
            
            if not text.strip():
                logger.debug(f"Page {page_num + 1}: Empty text")
                return None
            
            return TextBlock(page=page_num + 1, text=text)
            
        except Exception as e:
            logger.error(f"Error extracting text from page {page_num + 1}: {e}")
            return None
    
    def extract_text(self) -> List[TextBlock]:
        """Extract text from all pages using threading."""
        logger.info("Starting text extraction...")
        start_time = time.time()
        
        try:
            doc = fitz.open(str(self.pdf_path))
            total_pages = len(doc)
            self.metadata['total_pages'] = total_pages
            doc.close()
            
            logger.info(f"Processing {total_pages} pages with {self.max_workers} workers")
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._extract_text_page, i): i 
                    for i in range(total_pages)
                }
                
                completed = 0
                for future in as_completed(futures, timeout=self.TIMEOUT):
                    try:
                        result = future.result()
                        if result:
                            self.texts.append(result)
                        completed += 1
                    except Exception as e:
                        logger.error(f"Worker error: {e}")
                        continue
            
            self.texts.sort(key=lambda x: x.page)
            
            elapsed = time.time() - start_time
            total_chars = sum(t.char_count for t in self.texts)
            
            logger.info(
                f"✓ Text extracted: {len(self.texts)}/{total_pages} pages, "
                f"{total_chars:,} characters ({elapsed:.2f}s)"
            )
            
            self.metadata['text_pages'] = len(self.texts)
            self.metadata['total_characters'] = total_chars
            
            return self.texts
            
        except Exception as e:
            logger.error(f"Text extraction failed: {e}", exc_info=True)
            return []
    
    def _extract_tables_page(self, page_num: int) -> List[TableBlock]:
        """Extract tables from a single page."""
        tables_data = []
        try:
            with pdfplumber.open(str(self.pdf_path)) as pdf:
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                
                if not tables:
                    return []
                
                for table_idx, table_data in enumerate(tables):
                    table_block = TableBlock(
                        page=page_num + 1,
                        table_index=table_idx,
                        data=table_data
                    )
                    tables_data.append(table_block)
                    
        except Exception as e:
            logger.warning(f"Error extracting tables from page {page_num + 1}: {e}")
        
        return tables_data
    
    def extract_tables(self) -> List[TableBlock]:
        """Extract tables from all pages using threading."""
        logger.info("Starting table extraction...")
        start_time = time.time()
        
        try:
            with pdfplumber.open(str(self.pdf_path)) as pdf:
                total_pages = len(pdf.pages)
            
            logger.info(f"Scanning {total_pages} pages for tables")
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._extract_tables_page, i): i 
                    for i in range(total_pages)
                }
                
                for future in as_completed(futures, timeout=self.TIMEOUT):
                    try:
                        results = future.result()
                        self.tables.extend(results)
                    except Exception as e:
                        logger.error(f"Worker error: {e}")
                        continue
            
            self.tables.sort(key=lambda x: (x.page, x.table_index))
            
            elapsed = time.time() - start_time
            total_rows = sum(t.rows for t in self.tables)
            
            logger.info(
                f"✓ Tables extracted: {len(self.tables)} tables, "
                f"{total_rows:,} rows ({elapsed:.2f}s)"
            )
            
            self.metadata['tables_found'] = len(self.tables)
            self.metadata['total_rows'] = total_rows
            
            return self.tables
            
        except Exception as e:
            logger.error(f"Table extraction failed: {e}", exc_info=True)
            return []
    
    def process_pdf(self) -> Dict[str, Any]:
        """Run complete extraction pipeline."""
        logger.info("="*70)
        logger.info(f"Starting PDF Extraction: {self.pdf_path.name}")
        logger.info("="*70)
        
        total_start = time.time()
        
        self.extract_text()
        self.extract_tables()
        
        total_elapsed = time.time() - total_start
        self.metadata['total_time_seconds'] = round(total_elapsed, 2)
        
        logger.info("="*70)
        logger.info(f"✓ Pipeline completed in {total_elapsed:.2f}s")
        logger.info("="*70)
        
        return self.get_results()
    
    def get_results(self) -> Dict[str, Any]:
        """Get extraction results."""
        return {
            'texts': [{'page': t.page, 'text': t.text, 'char_count': t.char_count} for t in self.texts],
            'tables': [{'page': t.page, 'table_index': t.table_index, 'data': t.data, 'rows': t.rows, 'cols': t.cols} for t in self.tables],
            'metadata': self.metadata
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        return {
            'total_pages': self.metadata.get('total_pages', 0),
            'text_pages': self.metadata.get('text_pages', 0),
            'tables_found': self.metadata.get('tables_found', 0),
            'total_characters': self.metadata.get('total_characters', 0),
            'total_rows': self.metadata.get('total_rows', 0),
            'extraction_time_seconds': self.metadata.get('total_time_seconds', 0)
        }


# ==================== USAGE ====================
if __name__ == "__main__":
    try:
        pdf_path = "source/All you need is attention.pdf"  # Update with your PDF path
        pipeline = PDFExtractionPipeline(pdf_path, max_workers=4)
        
        results = pipeline.process_pdf()
        summary = pipeline.get_summary()
        
        print("\n" + "="*70)
        print("EXTRACTION SUMMARY")
        print("="*70)
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # Sample output
        if pipeline.texts:
            print(f"\n📝 First page text (first 200 chars):")
            print(f"  {pipeline.texts[0].text[:200]}...")
        
        if pipeline.tables:
            first_table = pipeline.tables[0]
            print(f"\n📊 First table found on page {first_table.page}:")
            print(f"  Dimensions: {first_table.rows} rows × {first_table.cols} cols")
            if first_table.data:
                print(f"  Header: {first_table.data[0]}")
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)