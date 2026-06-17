# Source Drop CLI 사용법

발표에서 보여줄 수 있는 간단한 입력 CLI입니다. PDF를 터미널에 드래그해서 경로를 붙여넣으면 `data/sources/`로 복사되고, 직접 입력한 텍스트도 `.txt` source로 저장됩니다.

## 대화형 실행

```bash
python demo/source_drop_cli.py
```

메뉴에서:

1. `파일 추가`를 선택합니다.
2. PDF 파일을 터미널로 드래그해서 생긴 경로를 붙여넣습니다.
3. `텍스트 추가`를 선택하면 여러 줄 텍스트를 입력할 수 있습니다.
4. 텍스트 입력을 끝낼 때는 새 줄에 `/done`을 입력합니다.
5. `pipeline 실행`을 선택하면 기존 mock pipeline이 실행됩니다.

## 발표용 빠른 예시

```bash
python demo/source_drop_cli.py --add-text "This is a short typed research note about blockchain certificates." --title "Typed Demo Note" --no-interactive
```

## 파일을 바로 추가하는 예시

```bash
python demo/source_drop_cli.py --add-file "/path/to/paper.pdf" --no-interactive
```

## 파일 추가 후 pipeline까지 실행

```bash
python demo/source_drop_cli.py --add-file "/path/to/paper.pdf" --run-pipeline --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment
```

주의: 현재 pipeline 실행은 mock mode가 기본값입니다. 실제 WorldLand tx나 실제 WLC payment를 만들지 않습니다.
