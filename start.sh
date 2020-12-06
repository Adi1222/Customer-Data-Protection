source ../cdp-env/bin/activate

cd Incident\ Logger 
nohup python3 main.py > nohupMain.out &

cd ../Application 
nohup python3 manage.py runserver 0.0.0.0:8000 > nohupServer.out &