# before running this script:
# draw border file for pp_1 and pp_2 in wb_view

# run this script from the commandline:
#  bash ~/code/Brainhack/Brainhack_Oxbridge/code/get_labels.sh

### --- Update that part
# cloned github repository
rootdir=/Users/neichert/code/Brainhack/Brainhack_Oxbridge
# downloaded HCP data
HCP_dir=/Users/neichert/code/Brainhack/local_only_nicole/data
### ----
# temporary folder for intermediate files
TMPDIR=$(mktemp -d)

hemi='L'
sub_list='103414 105115 110411 113619 115320 118730 123117 124422 129028'

for sub in $sub_list; do
    echo 'work on subject' $sub

    # subject data
    DD=$HCP_dir/$sub
    # output direcory for labels
    MD=$rootdir/labels/$sub
    # for debugging:
    #TMPDIR=$MD

    # get metric file from border
    wb_command -border-to-rois $DD/MNINonLinear/fsaverage_LR32k/${sub}.${hemi}.midthickness.32k_fs_LR.surf.gii  \
    $MD/pp_${hemi}.border $TMPDIR/pp_${hemi}.func.gii

    # get label for central sulcus from FreeSurfer parcellation
    wb_command -gifti-label-to-roi $DD/MNINonLinear/fsaverage_LR32k/${sub}.${hemi}.aparc.a2009s.32k_fs_LR.label.gii \
    $TMPDIR/cs_${hemi}.func.gii -name ${hemi}_S_central

    # logical combination of drawn 'plis de passage' to split cs_label in 3 parts
    wb_command -metric-math "(x>0 && y==0 && z==0)" $TMPDIR/3_parts.func.gii \
    -var x $TMPDIR/cs_${hemi}.func.gii \
    -var y $TMPDIR/pp_${hemi}.func.gii -column pp_1 \
    -var z $TMPDIR/pp_${hemi}.func.gii -column pp_2

    # work around to split the three segments in three data arrays
    wb_command -metric-find-clusters $DD/MNINonLinear/fsaverage_LR32k/${sub}.${hemi}.midthickness.32k_fs_LR.surf.gii \
    $TMPDIR/3_parts.func.gii \
    0.9 1 $TMPDIR/clusters.func.gii

    # cs_1: 1, cs_2: 2, cs_3:
    if [ $sub != '124422' ]; then
        for seg in 1 2 3; do
            wb_command -metric-math "(x==$seg)" $TMPDIR/seg${seg}.func.gii \
            -var x $TMPDIR/clusters.func.gii
        done
    # the order of clusters for this subject is different
    elif [ $sub == '124422' ]; then
        wb_command -metric-math "(x==1)" $TMPDIR/seg2.func.gii \
        -var x $TMPDIR/clusters.func.gii
        wb_command -metric-math "(x==2)" $TMPDIR/seg3.func.gii \
        -var x $TMPDIR/clusters.func.gii
        wb_command -metric-math "(x==3)" $TMPDIR/seg1.func.gii \
        -var x $TMPDIR/clusters.func.gii
    fi

    # add the small pp ROIs to the second ROI
    wb_command -metric-math "(x+y+z)" $TMPDIR/seg2.func.gii \
    -var x $TMPDIR/pp_${hemi}.func.gii -column pp_1 \
    -var y $TMPDIR/pp_${hemi}.func.gii -column pp_2 \
    -var z $TMPDIR/seg2.func.gii

    # merge final ROIs into one file
    wb_command -metric-merge $MD/segments_${hemi}.func.gii \
    -metric $TMPDIR/seg1.func.gii -metric $TMPDIR/seg2.func.gii -metric $TMPDIR/seg3.func.gii

done

# remove the temporary files
rm -rf $TMPDIR

echo $done
