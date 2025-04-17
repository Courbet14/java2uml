cd ~/.tools/java2uml
cp config ~/.zprofile
[ -f ~/.cache/.zprofile ] || (mkdir -p ~/.cache && echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' > ~/.cache/.zprofile)

