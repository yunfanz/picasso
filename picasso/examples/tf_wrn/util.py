from PIL import Image
from operator import itemgetter
import numpy as np

SP2_DIM = (32, 384)


def preprocess(targets):
    image_arrays = []
    for target in targets:
        img = skimage.io.imread(targets).astype(np.float32)
        img = img.reshape((32,384))
        img = img*(img>55)
        img *= (1./200)
        image_arrays.append(img)
        #im = target.convert('L')
        #im = im.resize(MNIST_DIM, Image.ANTIALIAS)
        #arr = np.array(im)
        #image_arrays.append(arr)

    all_targets = np.array(image_arrays)
    return all_targets.reshape(len(all_targets),
                               32,
                               384, 1)


def postprocess(output_arr):
    images = []
    for row in output_arr:
        im_array = row.reshape(MNIST_DIM)
        images.append(im_array)

    return images


def prob_decode(probability_array, top=5):
    results = []
    classes = ['narrowband', 'narrowbanddrd', 'noise', 'squiggle']
    for row in probability_array:
        entries = []
        for i, prob in enumerate(row):
            entries.append({'index': i,
                            'name': str(classes[i]),
                            'prob': prob})

        entries = sorted(entries,
                         key=itemgetter('prob'),
                         reverse=True)[:top]

        for entry in entries:
            entry['prob'] = '{:.3f}'.format(entry['prob'])
        results.append(entries)

    return results
