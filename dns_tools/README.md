mkdir -p /docker_data/django/
cd /docker_data/django/
git clone url  dns_tools
cp start.sh start.sh /docker_data/django/dns_tools
docker-compose up -d