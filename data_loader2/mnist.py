from __future__ import print_function
import torch.utils.data as data
from PIL import Image
import os
import os.path
import gzip
import numpy as np
import torch
import codecs
# from .utils import download_url, makedir_exist_ok
import scipy.io as sio


import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


class MNIST(data.Dataset):
    """`MNIST <http://yann.lecun.com/exdb/mnist/>`_ Dataset.

    Args:
        root (string): Root directory of dataset where ``processed/training.pt``
            and  ``processed/test.pt`` exist.
        train (bool, optional): If True, creates dataset from ``training.pt``,
            otherwise from ``test.pt``.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
    """
    urls = [
        'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
        'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
        'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
        'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz',
    ]
    training_file = 'training.pt'
    test_file = 'test.pt'
    classes = ['0 - zero', '1 - one', '2 - two', '3 - three', '4 - four',
               '5 - five', '6 - six', '7 - seven', '8 - eight', '9 - nine']

    def __init__(self, train=True, transform=None, target_transform=None):
        # self.root = os.path.expanduser(root)
        self.transform = transform
        # self.target_transform = target_transform
        self.train = train  # training set or test set
        #
        # if download:
        #     self.download()
        #
        # if not self._check_exists():
        #     raise RuntimeError('Dataset not found.' +
        #                        ' You can use download=True to download it')

        # if self.train:
        #     data_file = self.training_file
        # else:
        #     data_file = self.test_file
        # self.data, self.targets = torch.load(os.path.join(self.processed_folder, data_file))
        # self.data = self.data.data.numpy()
        # self.targets = self.targets.data.numpy()
        # print("Fetching inlier classes in training data")
        # inlier_data_index = np.isin(self.targets, classes)
        # self.targets = self.targets[inlier_data_index]
        # self.data = self.data[inlier_data_index]
        # print(self.targets)
        # self.data = torch.tensor(self.data)
        # self.targets = torch.tensor(self.targets)

        data = sio.loadmat('detect_mnist_small.mat')
        self.im_data = np.squeeze(data['im_data']).astype(np.uint8)
        # self.im_data = torch.tensor(self.im_data)
        # self.im_info = torch.tensor(np.concatenate([np.stack(data['im_info']*100)]*100))
        self.gt_boxes = data['gt_boxes']
        # self.num_boxes = torch.tensor(np.squeeze(data['num_boxes']))
        self.labels = data['labels']
        # print(self.im_data.size())
        # print(self.im_info.size())
        # print(self.gt_boxes.size())
        # print(self.labels.size())
        # print(self.im_data[1])
        # print(self.im_info[1])
        # print(self.gt_boxes[1])
        # print(data['num_boxes'].shape)
        # print(torch.tensor(data['num_boxes']).size())
        # print(self.num_boxes[1])



    def __getitem__(self, index):

        im_data, gt_boxes, labels = self.im_data[index], self.gt_boxes[index], self.labels[index]


        im_data = Image.fromarray(im_data, mode='L')

        if self.transform is not None:
            im_data = self.transform(im_data)

        return im_data, gt_boxes, labels

    def __len__(self):
        return len(self.im_data)

    @property
    def raw_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'raw')

    @property
    def processed_folder(self):
        return os.path.join(self.root, self.__class__.__name__, 'processed')

    @property
    def class_to_idx(self):
        return {_class: i for i, _class in enumerate(self.classes)}

    def _check_exists(self):
        return os.path.exists(os.path.join(self.processed_folder, self.training_file)) and \
            os.path.exists(os.path.join(self.processed_folder, self.test_file))

    @staticmethod
    def extract_gzip(gzip_path, remove_finished=False):
        print('Extracting {}'.format(gzip_path))
        with open(gzip_path.replace('.gz', ''), 'wb') as out_f, \
                gzip.GzipFile(gzip_path) as zip_f:
            out_f.write(zip_f.read())
        if remove_finished:
            os.unlink(gzip_path)

    # def download(self):
    #     """Download the MNIST data if it doesn't exist in processed_folder already."""
    #
    #     if self._check_exists():
    #         return
    #
    #     makedir_exist_ok(self.raw_folder)
    #     makedir_exist_ok(self.processed_folder)
    #
    #     # download files
    #     for url in self.urls:
    #         filename = url.rpartition('/')[2]
    #         file_path = os.path.join(self.raw_folder, filename)
    #         download_url(url, root=self.raw_folder, filename=filename, md5=None)
    #         self.extract_gzip(gzip_path=file_path, remove_finished=True)
    #
    #     # process and save as torch files
    #     print('Processing...')
    #
    #     training_set = (
    #         read_image_file(os.path.join(self.raw_folder, 'train-images-idx3-ubyte')),
    #         read_label_file(os.path.join(self.raw_folder, 'train-labels-idx1-ubyte'))
    #     )
    #     test_set = (
    #         read_image_file(os.path.join(self.raw_folder, 't10k-images-idx3-ubyte')),
    #         read_label_file(os.path.join(self.raw_folder, 't10k-labels-idx1-ubyte'))
    #     )
    #     with open(os.path.join(self.processed_folder, self.training_file), 'wb') as f:
    #         torch.save(training_set, f)
    #     with open(os.path.join(self.processed_folder, self.test_file), 'wb') as f:
    #         torch.save(test_set, f)
    #
    #     print('Done!')

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of datapoints: {}\n'.format(self.__len__())
        tmp = 'train' if self.train is True else 'test'
        fmt_str += '    Split: {}\n'.format(tmp)
        fmt_str += '    Root Location: {}\n'.format(self.root)
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        tmp = '    Target Transforms (if any): '
        fmt_str += '{0}{1}'.format(tmp, self.target_transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        return fmt_str


class FashionMNIST(MNIST):
    """`Fashion-MNIST <https://github.com/zalandoresearch/fashion-mnist>`_ Dataset.

    Args:
        root (string): Root directory of dataset where ``processed/training.pt``
            and  ``processed/test.pt`` exist.
        train (bool, optional): If True, creates dataset from ``training.pt``,
            otherwise from ``test.pt``.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
    """
    urls = [
        'http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz',
        'http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz',
        'http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz',
        'http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz',
    ]
    classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal',
               'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


class EMNIST(MNIST):
    """`EMNIST <https://www.nist.gov/itl/iad/image-group/emnist-dataset/>`_ Dataset.

    Args:
        root (string): Root directory of dataset where ``processed/training.pt``
            and  ``processed/test.pt`` exist.
        split (string): The dataset has 6 different splits: ``byclass``, ``bymerge``,
            ``balanced``, ``letters``, ``digits`` and ``mnist``. This argument specifies
            which one to use.
        train (bool, optional): If True, creates dataset from ``training.pt``,
            otherwise from ``test.pt``.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
    """
    url = 'http://www.itl.nist.gov/iaui/vip/cs_links/EMNIST/gzip.zip'
    splits = ('byclass', 'bymerge', 'balanced', 'letters', 'digits', 'mnist')

    def __init__(self, root, split, **kwargs):
        if split not in self.splits:
            raise ValueError('Split "{}" not found. Valid splits are: {}'.format(
                split, ', '.join(self.splits),
            ))
        self.split = split
        self.training_file = self._training_file(split)
        self.test_file = self._test_file(split)
        super(EMNIST, self).__init__(root, **kwargs)

    @staticmethod
    def _training_file(split):
        return 'training_{}.pt'.format(split)

    @staticmethod
    def _test_file(split):
        return 'test_{}.pt'.format(split)

    def download(self):
        """Download the EMNIST data if it doesn't exist in processed_folder already."""
        import shutil
        import zipfile

        if self._check_exists():
            return

        makedir_exist_ok(self.raw_folder)
        makedir_exist_ok(self.processed_folder)

        # download files
        filename = self.url.rpartition('/')[2]
        file_path = os.path.join(self.raw_folder, filename)
        download_url(self.url, root=self.raw_folder, filename=filename, md5=None)

        print('Extracting zip archive')
        with zipfile.ZipFile(file_path) as zip_f:
            zip_f.extractall(self.raw_folder)
        os.unlink(file_path)
        gzip_folder = os.path.join(self.raw_folder, 'gzip')
        for gzip_file in os.listdir(gzip_folder):
            if gzip_file.endswith('.gz'):
                self.extract_gzip(gzip_path=os.path.join(gzip_folder, gzip_file))

        # process and save as torch files
        for split in self.splits:
            print('Processing ' + split)
            training_set = (
                read_image_file(os.path.join(gzip_folder, 'emnist-{}-train-images-idx3-ubyte'.format(split))),
                read_label_file(os.path.join(gzip_folder, 'emnist-{}-train-labels-idx1-ubyte'.format(split)))
            )
            test_set = (
                read_image_file(os.path.join(gzip_folder, 'emnist-{}-test-images-idx3-ubyte'.format(split))),
                read_label_file(os.path.join(gzip_folder, 'emnist-{}-test-labels-idx1-ubyte'.format(split)))
            )
            with open(os.path.join(self.processed_folder, self._training_file(split)), 'wb') as f:
                torch.save(training_set, f)
            with open(os.path.join(self.processed_folder, self._test_file(split)), 'wb') as f:
                torch.save(test_set, f)
        shutil.rmtree(gzip_folder)

        print('Done!')


def get_int(b):
    return int(codecs.encode(b, 'hex'), 16)


def read_label_file(path):
    with open(path, 'rb') as f:
        data = f.read()
        assert get_int(data[:4]) == 2049
        length = get_int(data[4:8])
        parsed = np.frombuffer(data, dtype=np.uint8, offset=8)
        return torch.from_numpy(parsed).view(length).long()


def read_image_file(path):
    with open(path, 'rb') as f:
        data = f.read()
        assert get_int(data[:4]) == 2051
        length = get_int(data[4:8])
        num_rows = get_int(data[8:12])
        num_cols = get_int(data[12:16])
        parsed = np.frombuffer(data, dtype=np.uint8, offset=16)
        return torch.from_numpy(parsed).view(length, num_rows, num_cols)
