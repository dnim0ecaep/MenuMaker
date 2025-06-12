#!/usr/bin/env zsh
set -euo pipefail

BASE_DIR="./backup-macos-arm"
mkdir -p "$BASE_DIR"

# Use parallel arrays for keys and URLs
tool_names=(
  btop bottom bandwhich gping gotop glances cointop trippy taskwarrior-tui
  nnn lf broot yazi superfile
  lazydocker k9s dry
  lazygit gitui oha bagels delta diskonaut duf
  bat fd ripgrep
)

tool_urls=(
  "https://github.com/jesseduffield/lazydocker/releases/download/v0.24.1/lazydocker_0.24.1_Darwin_arm64.tar.gz"
  "https://github.com/ClementTsang/bottom/releases/latest/download/bottom_aarch64-apple-darwin.tar.gz"
  "https://github.com/imsnif/bandwhich/releases/download/v0.23.1/bandwhich-v0.23.1-aarch64-apple-darwin.tar.gz"
  "https://github.com/xxxserxxx/gotop/releases/download/v4.2.0/gotop_v4.2.0_darwin_arm64.tgz"
  "https://github.com/jesseduffield/lazygit/releases/download/v0.52.0/lazygit_0.52.0_Darwin_arm64.tar.gz"
  "https://github.com/ClementTsang/bottom/releases/download/0.10.2/bottom_aarch64-apple-darwin.tar.gz"
  "https://github.com/kdheepak/taskwarrior-tui/releases/download/v0.26.3/taskwarrior-tui-x86_64-apple-darwin.tar.gz"
  "https://github.com/imsnif/bandwhich/releases/download/v0.23.1/bandwhich-v0.23.1-aarch64-apple-darwin.tar.gz"
  "https://github.com/kdheepak/taskwarrior-tui/releases/latest/download/taskwarrior-tui-aarch64-apple-darwin.tar.gz"
  "https://github.com/fujiapple852/trippy/releases/download/0.13.0/trippy-0.13.0-aarch64-apple-darwin.tar.gz"
  "https://github.com/muesli/duf/releases/download/v0.8.1/duf_0.8.1_Darwin_arm64.tar.gz"
)

# Main downloader loop
for i in {1..${#tool_names[@]}}; do
  tool="${tool_names[$i]}"
  url="${tool_urls[$i]}"
  filename="${tool}_$(basename "$url")"
  dest="${BASE_DIR}/${filename}"

  echo "→ Downloading $tool..."
  if curl -sL "$url" -o "$dest"; then
    echo "✅ $tool downloaded successfully."
  else
    echo "⚠️ Failed to download $tool" | tee -a download_errors.log
  fi
done
echo "🎯 All downloads complete."
