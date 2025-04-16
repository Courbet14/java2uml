#make dhirectory
[ -d "$HOME/.tools/java2uml" ] || mkdir -p "$HOME/.tools/java2uml"
cd ~/.tools/
rm -fr java2uml
#download files
git clone https://github.com/Courbet14/java2uml.git > /dev/null #2>&1
cd java2uml
chmod +x setup.sh
./setup.sh