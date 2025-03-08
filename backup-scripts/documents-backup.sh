#!/bin/bash

document_dir=~/Dokumente
backup_dir=~/Sync/Sync-Backup/ThinkPad/Dokumente
mkdir -p $backup_dir
day=$(date +'%y-%m-%d-%m')
echo "Backup file: $backup_dir/doc-backup-$day.tar.gz"
tar czvf $backup_dir/doc-backup-$day.tar.gz -C $document_dir .
