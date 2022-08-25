from backbone.ErrorLevelAnalysis.ela import convert_to_ela_image
import backbone.CopyMoveDetection.copyMoveDetection as detectCopyMove


def work(filename):
    convert_to_ela_image(filename, 70)
    detect = detectCopyMove.Detect(filename)
    key_points, descriptors = detect.siftDetector()
    forgery = detect.locateForgery(60, 2)
