#!/usr/bin/env bash
set -euo pipefail

target_env="${1:-/srv/ops/universe_rag/.env}"
shared_env="${2:-/srv/ops/rag_service/docker/.env.vps.multi}"
target_dir="$(dirname "$target_env")"
token_file="$target_dir/research_token"

if [[ -e "$target_env" ]]; then
  echo "Refusing to overwrite existing deployment env: $target_env" >&2
  exit 2
fi
if [[ ! -f "$shared_env" ]]; then
  echo "Shared RAG environment not found: $shared_env" >&2
  exit 2
fi

set -a
# shellcheck disable=SC1090
source "$shared_env"
set +a

: "${RAG_INNOVASJON_LLM_API_KEY:?Missing RAG_INNOVASJON_LLM_API_KEY}"

random_secret() {
  openssl rand -hex 32
}

postgres_password="$(random_secret)"
admin_key="$(random_secret)"
research_token="$(random_secret)"
download_signing_key="$(random_secret)"
research_tokens_json="{\"$research_token\":{\"label\":\"server-smoke\",\"scopes\":[\"research:read\"],\"case_ids\":[\"universe_project\",\"universe_tools\",\"universe_argumentation\",\"universe_prompts\"]}}"

mkdir -p "$target_dir"
umask 077
{
  printf '%s\n' \
    'UNIVERSE_REPO_DIR=/srv/ops/repos/UniverseSimulation' \
    'UNIVERSE_UPLOADS_DIR=/srv/ops/universe_rag/uploads' \
    'UNIVERSE_API_PORT=8103' \
    'UNIVERSE_RAG_RUNTIME_IMAGE=docker-rag_innovasjon_api' \
    'UNIVERSE_POSTGRES_USER=rag' \
    'UNIVERSE_POSTGRES_DB=rag_universe' \
    'UNIVERSE_LLM_PROVIDER=openai_compat' \
    'UNIVERSE_RESEARCH_RATE_LIMIT_PER_MINUTE=30' \
    'UNIVERSE_RESEARCH_RATE_LIMIT_BURST=60' \
    'UNIVERSE_RESEARCH_FRESHNESS_MAX_AGE_SECONDS=86400'
  printf 'UNIVERSE_POSTGRES_PASSWORD=%s\n' "$postgres_password"
  printf 'UNIVERSE_LLM_BASE_URL=%s\n' "${RAG_INNOVASJON_LLM_BASE_URL:-https://api.openai.com/v1}"
  printf 'UNIVERSE_LLM_API_KEY=%s\n' "$RAG_INNOVASJON_LLM_API_KEY"
  printf 'UNIVERSE_LLM_MODEL=%s\n' "${RAG_INNOVASJON_LLM_MODEL:-gpt-4o-mini}"
  printf 'UNIVERSE_ADMIN_API_KEY=%s\n' "$admin_key"
  printf "UNIVERSE_RESEARCH_API_TOKENS_JSON='%s'\n" "$research_tokens_json"
  printf 'UNIVERSE_RESEARCH_DOWNLOAD_SIGNING_KEY=%s\n' "$download_signing_key"
} >"$target_env"
printf '%s\n' "$research_token" >"$token_file"
chmod 600 "$target_env" "$token_file"

echo "Provisioned Universe RAG environment and operator token with mode 0600."
