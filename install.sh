sudo cp SocialMediaDataAnalyzer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart apache2
sudo systemctl start SocialMediaDataAnalyzer.service
sudo systemctl status SocialMediaDataAnalyzer.service
