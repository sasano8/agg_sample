# 開発環境構築

```
make generate-secret
```

.env ファイルを作成する。

```
CHOCO_SECRET_KEY=<secret>
```

```
pyenv python3.8.12
```

```
poetry install
```

```
uvicorn app:app --reload
```
