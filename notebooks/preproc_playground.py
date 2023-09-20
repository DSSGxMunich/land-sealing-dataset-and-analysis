import layoutparser as lp
import cv2
import matplotlib.pyplot as plt


if __name__ == '__main__':
    sample_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/sample.png"
    img = cv2.imread(sample_path)
    # plot the image
    #plt.figure(figsize=(15, 10))
    #plt.imshow(img)
    #plt.show()

    # pretrained_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/models/layout_segmentation/pretrained1"
    base_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/models/layout_segmentation/publay-faster-rcnn"
    model_path = f"{base_path}/model_final.pth"
    config_path = f"{base_path}/config.yml"

    model = lp.Detectron2LayoutModel(
        config_path=config_path,  # In model catalog
        model_path=model_path,
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.7]  # Confidence threshold
    )
    plt.figure(figsize=(30, 10))
    layout = model.detect(img)
    layout_vis = lp.draw_box(img, layout, box_width=5)
    # Show the detected layout of the input image
    plt.imshow(layout_vis)
    plt.show()

    print(layout)

