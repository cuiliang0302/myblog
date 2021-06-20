#!/bin/bash
# 设置mysql的登录用户名和密码(根据实际情况填写)
mysql_user="root"
mysql_password="CuiLiang@0302"
mysql_host="localhost"
mysql_port="3306"
mysql_charset="utf8mb4"
mysql_db="myblog"

# 备份文件存放地址(根据实际情况填写)
backup_location=/opt/mysql_backup

# 是否删除过期数据
expire_backup_delete="ON"
expire_days=7
backup_time=`date +%Y%m%d%H%M`
backup_dir=$backup_location
# 备份指定数据库中数据
docker exec -it mysql mysqldump -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password -B $mysql_db > $backup_dir/mysql_backup_$mysql_db-$backup_time.sql

# 删除过期数据
if [ "$expire_backup_delete" == "ON" -a  "$backup_location" != "" ];then
    `find $backup_location/ -type f -mtime +$expire_days | xargs rm -rf`
    echo "Expired backup data delete complete!"
fi