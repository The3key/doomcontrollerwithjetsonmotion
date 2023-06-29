# SM64 Project

Hi Alex! This is Blue, with some guidance on how to get the ASL dataset ready for training,
and then where to go from there.

## Context

The Jetson-Inference Object Detection AI is set up to work with two dataset formats:

-   Google Open Images
-   Pascal VOC

(from <https://github.com/dusty-nv/pytorch-ssd/tree/57c901e3e3abf33c64dffc9292e7eb8458397ac6>)

## Dataset provided

Your ASL dataset offers a [download in Pascal VOC](https://public.roboflow.com/object-detection/american-sign-language-letters/1),
so let's use that!

...

I've gone ahead and done so already (in `~/jetson-inference/python/training/detection/ssd/data/asl_original`). The annotation files are all set up right.

But, it looks like the `jetson-inference` library expects a slightly different folder structure. Yikes...

### A Brief Description of Datasets

-   `train`:        used to train the AI model through normal batches & epochs, gradient descent, backpropagation, etc.
-   `val(id(ate))`: used to verify training progress after each epoch.
        if accuracy on `train` is increasing, but accuracy on `val` is decreasing, then the model is overfitting,
        i.e. it's learning the latent biases and statistical noise in the `train` data instead of actual useful traits.
-   `test`:         used for manual testing of the AI model once training is complete

### jetson-inference expected folder structure

    dataset_name
     |> Annotations:    a directory holding all of the `ImageID.xml` annotation files
     |> JPEGImages:     a directory holding all of the `ImageID.(png|jpg)` image files
     |> ImageSets
     |   |> Main
     |       |- train.txt:      a file listing all ImageIDs in the "train" dataset, one ImageID per line
     |       |- val.txt:        a file listing all ImageIDs in the "validate" dataset
     |       |- trainval.txt:   a file listing all ImageIDs from both the "train" and "validate" datasets
     |       |- test.txt:       a file listing all ImageIDs in the "test" dataset
     |- labels.txt: a text file containing one line for the name of each "class" of object in the dataset.
                    these "class names" should match exactly the ones used in the Annotations files
                    (in your dataset, these are just single uppercase letters, like "A", "B", "C")

### roboflow provided folder structure
    dataset_name
     |> test:   a directory holding all `ImageId.xml` and `ImageId.jpg` files for the "test" dataset
     |> train:  a directory holding all `ImageId.xml` and `ImageId.jpg` files for the "train" dataset
     |> valid:  a directory holding all `ImageId.xml` and `ImageId.jpg` files for the "valid" dataset
     |- README.roboflow.txt: basic info about the dataset and how it was collected.
     
## Our Task

Good news! It's absolutely possible for us to rework this folder structure for our own needs.
I've already got one camper (Tristan) **training** with a custom dataset in this folder structure.
(If you need help with this folder structure, try going to him.)

Your task is to take the `asl_original` dataset, and rearrange it
into the `asl_clean` folder with `jetson-inference`'s expected format.
To help with this, I've added README.md files all throughout `asl_clean` reminding you what to put in each folder.

I suggest the following order of tasks:

1.  Create `asl/labels.txt` by writing the alphabet, one capital letter per line.
1.  Write a python script to generate the files in `ImageSets/Main`. That program should:
    1.  work on one of the folders at a time, e.g. train/val/test.
        *   hint: you can hard-code the folder and just run the script 3x
    2.  list all of the files in the folder.
        *   filter out either `xml` or `jpg` so you're left with just one type of file
    3.  remove the extension from the filename to get just the ImageID
        *   hint: they're both exactly 3 characters (plus the .), so try just trimming the last 4 characters off of the filename
    4. write this list of ImageIDs into a file, one ID per line
        *   you can either collect a list of ImageIDs to write all at once, or you can write one line at a time as you go
2.  Create `ImageSets/Main/trainval.txt` by just copy/pasting `train.txt` and `val.txt` together.
3.  Use the `cp` command to copy all files ending in `xml` into `asl_clean/Annotations`, and
    all files ending in `jpg` into `asl_clean/JPEGImages`.
    *   hint: "Instead of all the above" at <https://stackoverflow.com/questions/15617016/copy-all-files-with-a-certain-extension-from-all-subdirectories>

Good luck! Let me know with your question flag if you run into any issues.

## Next steps

### Training

Once you get the dataset organized, you'll want to start training on your dataset.
Remember, you'll need to be *in* the Jetson, and *in* the "AI tools" Docker container (`jetson-inference/docker/run.sh`).
Lastly, you'll need to be in the folder: `jetson-inference/python/training/detection/ssd`.
That train command looks like:

```shell
python3 train_ssd.py --dataset-type=voc --data="data/asl_clean" --model-dir="models/asl_detect" # (or "models/<name-you-choose>")
```

### Testing

Once you get the model trained, we should try running it on some test data.

#### Export

You'll need to export your trained model to ONNX format:
<https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md#converting-the-model-to-onnx>

#### Live video setup

You may want to try setting up a live video feed for the input & output.
The easiest setup I found was just streaming over WebRTC to your browser:
*   Console command: `detectnet /dev/video0 webrtc://@:8554/my_output`
    `/dev/video0` means "input from webcam"
    `webrtc://@:8554/my_output` means "stream output over `webrtc`, serving from this machine (`@`), on port `8554`.
*   View in browser at: <http://192.168.137.188:8554>
    (that is the IP address of the Jetson; I grabbed it from your hotspot settings page)

Other resources:
*   Dusty demonstrates other ways this might work here: <https://youtu.be/QXIwdsyK7Rw?t=727>
*   and the process is documented here: <https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-streaming.md>

#### Testing with live video

Once you've got the model exported, and live video setup working, try running your model over live video:

```shell
detectnet --model="models/asl_detect/ssd-mobilenet.onnx" --labels="models/asl_detect/labels.txt" \
          --input-blob=input_0 --output-cvg=scores --output-bbox=boxes \
            /dev/video0 webrtc://@:8554/my_output
```

Try making two ASL signs at once. Does it detect well? If not, maybe it needs more training.

### Integration

Lastly, we need to run this detectnet program in our *own* python script,
so that we can send inputs back to the host computer.

#### Running detectnet in custom Python script

Check this tutorial page: <https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-example-2.md>

It should have everything you need. Work your way up to our final goal:

1.  Copy the code in, and adjust necessary things:
    * videoSource should be "/dev/video0"
    * videoOutput should be "webrtc://@:8554/my_output"
2.  Verify the basic detectnet is working.
3.  Using the arguments on that `detectNet` object, switch to your own custom-trained model.
    see docs: <https://rawgit.com/dusty-nv/jetson-inference/master/docs/html/python/jetson.inference.html#detectNet>
4.  Verify it's also working well.

##### Turning ASL into SM64 commands

The detectnet program will give you some Python `detections` with the ASL signs you make,
but it's up to you how to turn that into *commands* for SM64.

See if you can adjust the program to:
*   determine a SM64 command for the ASL letter detections you care about
*   package all the commands for each frame into one python `list` (or python `dict`)
*   print the command(s) for this frame to the console
*   render the command(s) for this frame to the video stream

#### Sending network requests from Jetson to host computer

The simplest way to send data across the network is a tech called UDP.
UDP is basically the "lightweight but spotty" network request, as opposed to the "heavyweight but reliable" TCP.
-   TCP does extra checks to verify the exact message was received correctly
-   UDP just sends a message off into the void. it's more like "hey yolo, do your best"
For these reasons, most real-time online games use UDP for in-game updates.
For our purposes, UDP is slightly simpler because it takes less configuration.
(and with a local hotspot, we're practically guaranteed our UDP packets will not get lost.)

This webpage has some strangely-formatted information, but the best code example I could find:
<https://pythontic.com/modules/socket/udp-client-server-example>
Try copying both of those files **onto the laptop**, then run the `server`, and then the `client`.

For your project, you'll want a UDP server running on your laptop, and a UDP client on the Jetson Nano.
When you get to this step, raise your question flag;
it's just much easier if I explain why certain things work certain ways in person instead of over text.

#### Python program to submit keyboard commands

The UDP server will also have to submit keyboard commands when it receives a message.
-   Try searching the internet for some examples on how Python can control the keyboard.
-   See if you can get a python program which will:
    1.  Open chrome ("Windows" key + c h r o m e + "enter")
    2.  Open a guest window (8 "tab"s + "enter")
    3.  Type in the URL for Rick Astley's Never Gonna Give You Up + "enter" (https://www.youtube.com/watch?v=dQw4w9WgXcQ)

### Lastly

This should be everything you need for your project!

1.  Detection client running on the Jetson which can:
    1.  Detect multiple ASL letters
    2.  Transform each ASL letter into a SM64 command
    3.  Transmit the list of commands each frame over the network to...
2.  Command server running on your laptop which can:
    1.  Receive commands from the Jetson
    2.  Submit keyboard presses to your computer

Now try booting up SM64 to see how well it works ^-^

