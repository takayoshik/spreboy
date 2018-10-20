
all_files=( "`ls`" )

target_dir=costumes_png

if [ $# -eq 1 ]; then
  target_dir=$1
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
        file_postfix=${fname##*.}
        file_prefix=${fname%.*}
        if [ $file_postfix = png ]; then
                # echo This is PNG file
                # echo cp $fname $target_dir/
                cp $fname $target_dir
        elif [ $file_postfix = svg ]; then
                # echo This is SVG file
                # echo inkscape -z -e $target_dir/$file_prefix.png $fname
                inkscape -z -e $target_dir/$file_prefix.png $fname
        elif [ $file_postfix = gif ]; then
                # echo This is GIF file
                # echo convert -verbose -coalesce $fname $target_dir/$file_prefix.png
                convert -verbose -coalesce $fname $target_dir/$file_prefix.png
        elif [ $file_postfix = jpg ]; then
                convert -verbose $fname $target_dir/$file_prefix.png
        else
                echo $fname is not image file...
        fi
done

