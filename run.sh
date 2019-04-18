export APPDIR=$(pwd)

echo Building User Interface

pyuic4 ui/VidSelect.ui -o py/VidSelect.py
pyrcc4 ui/AppResources.qrc  -o py/AppResources_rc.py -py3
if [ "$1" == "1080" ]
then
pyuic4 ui/Application1080.ui -o py/Application.py
else
pyuic4 ui/Application720.ui -o py/Application.py
fi

echo Starting Application..
cd py/
chmod +x Main.py
./Main.py

echo Removing Temporary Files..
rm Application.py
rm VidSelect.py
rm AppResources_rc.py

echo Application Exited
cd ..
