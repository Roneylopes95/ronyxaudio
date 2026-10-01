#!/data/data/com.termux/files/usr/bin/bash
# PC Ronyx Download Áudio Automação - versão Termux (MP3 completo)
# Uso: bash termux_baixar.sh "URL_DO_VIDEO"
# Use apenas com conteúdo que você tem direito de baixar.

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo ">> Primeira execução: instalando ferramentas (leva alguns minutos)..."
  termux-setup-storage
  pkg update -y && pkg install -y python ffmpeg nodejs
  pip install -U yt-dlp
fi

URL="$1"
if [ -z "$URL" ]; then
  read -p "Cole a URL do vídeo: " URL
fi

mkdir -p "$HOME/storage/music/PC Ronyx"
yt-dlp -x --audio-format mp3 --audio-quality 192K --no-playlist \
  --js-runtimes node --remote-components ejs:github \
  -o "$HOME/storage/music/PC Ronyx/%(title)s.%(ext)s" "$URL"

echo ">> Pronto! Veja em Música > PC Ronyx"
