import torch
import torchvision.utils
from PIL import Image
from torchvision import transforms
import torchvision
import numpy
import cv2


class GroupNormalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, Te):
        tensor = Te
        rep_mean = self.mean * (tensor.size()[0]//len(self.mean))
        rep_std = self.std * (tensor.size()[0]//len(self.std))

        # TODO: make efficient
        for t, m, s in zip(tensor, rep_mean, rep_std):
            t.sub_(m).div_(s)

        return tensor


def back_normalize(tensor, mean, std):
    rep_mean = mean * (tensor.size()[0]//len(mean))
    rep_std = std * (tensor.size()[0]//len(std))
    for t, m, s in zip(tensor, rep_mean, rep_std):
        t.mul_(s).add_(m)
    return tensor


class ToTorchFormatTensor(object):
    """ Converts a PIL.Image (RGB) or numpy.ndarray (H x W x C) in the range [0, 255]
    to a torch.FloatTensor of shape (C x H x W) in the range [0.0, 1.0] """
    def __init__(self, div=True):
        self.div = div

    def __call__(self, pi):
        pic = pi
        if isinstance(pic, numpy.ndarray):
            # handle numpy array
            img = torch.from_numpy(pic).permute(2, 0, 1).contiguous()
        else:
            # handle PIL Image
            img = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))
            img = img.view(pic.size[1], pic.size[0], len(pic.mode))
            # put it from HWC to CHW format
            # yikes, this transpose takes 80% of the loading time/CPU
            img = img.transpose(0, 1).transpose(0, 2).contiguous()
        return img.float().div(255) if self.div else img.float()


class Stack(object):

    def __init__(self, roll=False):
        self.roll = roll

    def __call__(self, img):
        img_group = img
        if img_group[0].mode == 'L':
            return numpy.concatenate([np.expand_dims(x, 2) for x in img_group], axis=2),label
        elif img_group[0].mode == 'RGB':
            if self.roll:
                return numpy.concatenate([numpy.array(x)[:, :, ::-1] for x in img_group], axis=2)
            else:
                return numpy.concatenate(img_group, axis=2)

'''
3x3x2x2
picture-h-w-c
'''
'''
a = [[[[1110, 1120],
       [1210, 1220]],
      [[1111, 1121],
       [1211, 1221]],
      [[1112, 1122],
       [1212, 1222]]],
     [[[2110, 2120],
       [2210, 2220]],
      [[2111, 2121],
       [2211, 2221]],
      [[2112, 2122],
       [2212, 2222]]],
     [[[3110, 3120],
       [3210, 3220]],
      [[3111, 3121],
       [3211, 3221]],
      [[3112, 3122],
       [3212, 3222]]]]

x = torch.tensor(a)
print(x)

x = torch.transpose(x, 1, 2)
print(x.size())
print(x)

x = torch.transpose(x, 2, 3)
print(x.size())
print(x)
'''
'''
a = torch.tensor([[[0.111111, 0.111111],
                   [0.111111, 0.111111]],
                  [[0.555555, 0.555555],
                   [0.555555, 0.555555]],
                  [[0.888888, 0.888888],
                   [0.888888, 0.888888]]])

input_mean = [0.485, 0.456, 0.406]
input_std = [0.229, 0.224, 0.225]
normalize = GroupNormalize(input_mean, input_std)

aa = list()
a = [Image.open("0.jpg").convert("RGB")]

c = a[0]
trans = transforms.Compose([transforms.ToTensor()])
print(trans(c))

aa.extend(a)
trans = torchvision.transforms.Compose([
            Stack(roll=False),
            ToTorchFormatTensor(div=True),
            normalize])

aa = trans(aa)
aa = back_normalize(aa, input_mean, input_std)
print(aa)

torchvision.utils.save_image(aa, "2.jpg")

b = Image.open("2.jpg").convert("RGB")
trans = transforms.Compose([transforms.ToTensor()])
b = trans(b)
print(b)
'''
a = torch.tensor([[[1., 1.],
                   [1., 1.]],
                  [[2., 2.],
                   [2., 2.]],
                  [[1., 2.],
                   [3., 4.]]])

b = torch.norm(a, 2, dim=(-2,-1), keepdim=True)

c = a / b * 10
print(c)
print(torch.norm(c, 2, dim=(-2,-1), keepdim=True))

print(b.repeat(1, 2, 2))

