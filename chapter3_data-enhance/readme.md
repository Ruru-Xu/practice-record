**note:**

You can run **train_time_augment.py** directly, It will read the image in the **train_dataset** folder and the tag in **train_labels.csv**, and finally generate the corresponding xml file.

------

**Enhancement method:**
     Histogram Blur Brightness adjustment Random center crop rotation (90 180 270) Horizontal flip Vertical flip Horizontal vertical flip Gaussian noise Gaussian blur Horizontal flip _ Gaussian blur
     Vertical Flip _ Gaussian Noise Horizontal Flip _ Histogram Horizontal Flip _ Histogram

------

- data_augment.py------Several data enhancement methods have been used:
  Histogram, horizontal flip, vertical flip, horizontal vertical flip, Gaussian noise, Gaussian blur, rotation
- bbox_convert.py------Convert the corresponding label box after data enhancement
- pascal_voc_xml_2_coco_json.py--------convert the format xml of pascal voc to json of coco
- train_time_augment.py-------1. Divide the data set into a training set and a test set
  2. Data enhancement and conversion of the corresponding label

