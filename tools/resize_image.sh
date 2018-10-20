
all_files=( "`ls *.png`" )

target_dir=

if [ $# -eq 1 ]; then
        target_dir=$1
else
        echo Need target directory
        exit
fi

echo Conversion targetdir is $target_dir
if [ -e $target_dir ]; then
        if [ ! -d $target_dir ]; then
                echo $target_dir must be directory.
                exit
        fi
fi

rm $target_dir/*

for fname in $all_files
do
        python ConvertPNG32.py $fname $target_dir/$fname 320 240
done

