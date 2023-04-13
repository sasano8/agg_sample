generate-secret:
	@openssl rand -hex 32

run-server:
	@uvicorn app:app --reload
