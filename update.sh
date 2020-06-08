mkdir -p /var/www/openmeme
git pull
yarn build
cp -ar build/. /var/www/openmeme/
chown -R www-data:www-data /var/www/openmeme