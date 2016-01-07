base="/home/tahoe/pepper/dev"
shell_base="/home/tahoe/pepper/dev/scripts/supervisor"
 
source $shell_base/env-rvm1.9.3.sh

cd $base/edx-platform/

# rake cms:gather_assets:dev  
# rake lms:gather_assets:cms.dev

rm $base/staticfiles/lms/* -rf
rm $base/staticfiles/cms/* -rf

rake assets:coffee[lms,cms.staging]
rake assets:sass[lms,cms.staging]

rake assets:coffee[cms,staging]
rake assets:sass[cms,staging]

cp $base/edx-platform/common/static/* $base/staticfiles/lms/ -r
cp $base/edx-platform/common/static/* $base/staticfiles/cms/ -r

cp $base/edx-platform/lms/static/* $base/staticfiles/lms/ -r
cp $base/edx-platform/cms/static/* $base/staticfiles/cms/ -r

python manage.py lms --settings cms.staging collectstatic
python manage.py cms --settings staging collectstatic


echo ""
echo "[lms]"
ls $base/staticfiles/lms/

echo ""
echo "[cms]"
ls $base/staticfiles/cms/
echo ""

echo "done"
