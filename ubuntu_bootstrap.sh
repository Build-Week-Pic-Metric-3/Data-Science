sudo apt install gunicorn -y
mkdir picmetric
python3 -m venv env/
source env/bin/activate
git init
git pull https://github.com/Build-Week-Pic-Metric-3/Data-Science.git master
mkdir PicMetric/assets/weights
cd PicMetric/assets/weights/
pip install flask requests python-decouple boto3 pillow flask-sqlalchemy numpy tensorflow imageai opencv-python keras mtcnn flask-cors python-dotenv1