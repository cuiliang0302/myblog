#!/bin/bash

# 备份文件存放地址(根据实际情况填写)
backup_location=/opt/meida_backup

# 是否删除过期数据
expire_backup_delete="ON"
expire_days=7
backup_time=`date +%Y%m%d%H%M`
backup_dir=$backup_location
# 备份指定数据库中数据
tar -zcPf $backup_dir/meida_backup_$backup_time.tar.gz /opt/myblog/media

# 删除过期数据
if [ "$expire_backup_delete" == "ON" -a  "$backup_location" != "" ];then
    `find $backup_location/ -type f -mtime +$expire_days | xargs rm -rf`
fi