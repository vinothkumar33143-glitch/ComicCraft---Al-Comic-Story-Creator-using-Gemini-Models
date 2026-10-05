# API examples

## Generate a comic

```bash
curl -X POST http://127.0.0.1:8000/generate-comic/json ^
  -H "Content-Type: application/json" ^
  -d "{\"story_prompt\":\"A brave fox explores an enchanted forest\",\"character_name\":\"Fenn\",\"setting\":\"forest\",\"tone\":\"dramatic\",\"art_style\":\"comic book\"}"
```

## Health

```bash
curl http://127.0.0.1:8000/health
```

## Test image

```bash
curl -X POST http://127.0.0.1:8000/test-image -F "prompt=a heroic fox in a comic book forest"
```
