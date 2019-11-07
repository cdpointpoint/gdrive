# google-api-python-client 
cp gpush.py  gpull.py ~/bin/
chmod +x ~/bin/gpush.py
chmod +x ~/bin/gpull.py

CFGDIR=~/.credentials
[ -d "$CFGDIR" ] || mkdir -p $CFGDIR


CLIENT_SECRET=gdrive_client_secret.json
cp -p client_secret.json $CFGDIR/$CLIENT_SECRET
chmod 600 $CFGDIR/$CLIENT_SECRET
