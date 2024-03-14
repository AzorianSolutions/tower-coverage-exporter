from numpy import ndarray


class MaskUtil:

    @staticmethod
    def create_mask_from_image_alpha(path: str) -> ndarray:
        import cv2

        # load image with alpha channel
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        rgb_map: dict = {}

        for row in img:
            for pixel in row:
                map_key: str = ''

                for index in range(0, pixel_length := len(pixel)):
                    map_key += str(pixel[index])
                    if index < pixel_length - 1:
                        map_key += '_'

                if map_key not in rgb_map:
                    rgb_map[map_key] = pixel

        # extract alpha channel
        alpha = img[:, :, 3]

        # threshold alpha channel
        alpha = cv2.threshold(alpha, 0, 255, cv2.THRESH_BINARY)[1]

        return alpha
