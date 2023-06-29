# ImageSets/Main

This folder should contain 4 files:

-   train.txt       (1512 lines, one per sample in `asl_original/train`)
-   val.txt         (144  lines)
-   test.txt        (72   lines)
-   trainval.txt    (1656 lines. essentially `train.txt` + `val.txt`; contents from both files)

Each of these files should list the "image IDs" in that dataset,
where the "image ID" is the filename of the image, without the extension.

Example:

    Image file:         A22_jpg.rf.f02ad8558ce1c88213b4f83c0bc66bc8.jpg
    Annotation file:    A22_jpg.rf.f02ad8558ce1c88213b4f83c0bc66bc8.xml
    Image ID:           A22_jpg.rf.f02ad8558ce1c88213b4f83c0bc66bc8

So, for example, the `test.txt` file might start like this:

```txt
A22_jpg.rf.f02ad8558ce1c88213b4f83c0bc66bc8
B14_jpg.rf.ed5ba6d44f55ab03e62d2baeac4aa1aa
B15_jpg.rf.0f0628552139144fc67c453e1f1b7b15
```

Each file should have one line for each sample in the dataset.

For your sanity, you'll probably want to write a program to generate these files.
Copy/pasted from `asl_clean/README.md`:

Write a python script to generate the files in `ImageSets/Main`. That program should:

1.  work on one of the folders at a time, e.g. train/val/test.
    *   hint: you can hard-code the folder and just run the script 3x
2.  list all of the files in the folder.
    *   filter out either `xml` or `jpg` so you're left with just one type of file
3.  remove the extension from the filename to get just the ImageID
    *   hint: they're both exactly 3 characters (plus the .), so try just trimming the last 4 characters off of the filename
4. write this list of ImageIDs into a file, one ID per line
    *   you can either collect a list of ImageIDs to write all at once, or you can write one line at a time as you go