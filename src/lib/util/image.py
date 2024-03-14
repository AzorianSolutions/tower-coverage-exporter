class ImageUtil:

    @staticmethod
    def get_meta(path: str) -> tuple:
        import cv2

        # load image with alpha channel
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        shape: tuple = img.shape

        return shape[1], shape[0], shape[2]
