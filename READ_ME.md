# Pinterest Pin Generator (Python) — MVP

Podstawowa, modułowa struktura do:
1. odczytu gotowych mock-upów PNG/JPG z folderu,
2. doboru słów kluczowych z Twojej dużej listy (np. 300 fraz),
3. przygotowania pliku CSV pod import do Pinterest.

## Dlaczego `Media URL` nie działa dla lokalnych plików?
Pinterest CSV wymaga **publicznego URL** (`https://...`), a nie ścieżki z komputera.

### Proste rozwiązania
- Upload obrazów na serwer/CDN (np. Cloudflare R2, S3, własny hosting),
- Trzymanie obrazów w katalogu publicznym strony (`https://twojadomena.com/pins/...`),
- Następnie w CSV wpisujesz ten URL w `Media URL`.

Ten projekt tworzy też pomocniczy plik `image_upload_manifest.csv`, który mapuje:
- lokalny plik -> sugerowany publiczny URL.

## Struktura

```text
main.py
pin_generator/
  config.py
  models.py
  pipelines/generate_pins.py
  services/
    image_discovery.py
    keyword_selector.py
    text_generator.py
    csv_exporter.py
data/
  input/
    keywords.txt         # 1 fraza na linię
    etsy_links.csv       # opcjonalnie: file_stem,etsy_url
    mockups/             # Twoje PNG/JPG
  output/
```

## Jak użyć

1. Wstaw grafiki do `data/input/mockups/`.
2. Dodaj listę słów kluczowych do `data/input/keywords.txt` (1 fraza na linię).
3. (Opcjonalnie) Dodaj `data/input/etsy_links.csv`:

```csv
file_stem,etsy_url
sunset_oil_01,https://www.etsy.com/listing/1234567890
```

4. Ustaw `media_base_url` i inne parametry w `pin_generator/config.py`.
5. Uruchom:

```bash
python main.py
```

## Dobór słów kluczowych
MVP używa prostego dopasowania tokenów:
- analizuje nazwę pliku (`sunset_oil_painting_01.png`),
- analizuje wygenerowany opis,
- wybiera najlepiej pasujące frazy z banku słów.

Dzięki temu możesz używać jednej dużej listy (300+ słów), a system wybierze podzbiór do każdego pina.

## Co dalej (rozszerzenia)
- lepszy ranking keywordów (TF-IDF/embeddings),
- generacja opisu przez API LLM,
- automatyczny upload plików i zwrot prawdziwych URL.
