#! /bin/bash
# 代码更新后重载项目
cd /opt/myblog/
git reset --hard
git pull origin master
rm -rf /opt/myblog/myblog/settings.py
mv /opt/myblog/myblog/settings_prod.py /opt/myblog/myblog/settings.py
python3 /opt/myblog/other/make_bgc.py
docker restart myblog