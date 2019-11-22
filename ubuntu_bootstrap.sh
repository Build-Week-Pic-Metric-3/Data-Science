sudo apt install gunicorn -y
sudo apt install gcc -y
sudo apt install python3-flask -y
sudo apt install virtualenv -y
sudo apt-get install libpq-dev python-dev -y
sudo apt install postgresql -y
sudo apt update && sudo apt install -y libsm6 libxext6 -y
mkdir PicMetric
cd PicMetric
virtualenv -p python3 picmetricenv
git init
git pull https://github.com/Build-Week-Pic-Metric-3/Data-Science.git master
mkdir PicMetric/assets/weights
cd PicMetric/assets/weights/
wget https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5
echo "Activate your virtual enviornment and run"
echo "source picmetricenv/bin/activate"
echo "pip install -r ubuntu_requirements.txt"
echo "Also update .env file one level above the flask app!!!"