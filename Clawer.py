import os
import re
import requests


def getImageList(url: str, page: int):
    url = url.format(page)
    sourceCode = requests.get(url).text
    reg = r'alt="(.*?)".*?data-original="(.*?)"'
    reg = re.compile(reg, re.S)
    imageList = re.findall(reg, sourceCode)
    return imageList


def scanner(url, start, end) -> list:
    res = []
    for i in range(start, end+1):
        res.append(getImageList(url, i))
        print("正在解析第{}页，请稍候...".format(i))
    return res


def formatName(name):
    if name[-3::] == '表情图':
        name = name[:-3:]
    if len(name) > 100:
        name = name[:65:]
    name = name.replace('/', '_')
    return name


def downloader(inputData):
    for page in inputData:
        for imageData in page:
            imageName = formatName(imageData[0])
            imageName = str(inputData.index(page) + 1) + '_' + \
                str(page.index(imageData) + 1) + imageName
            imageUrl = imageData[1]
            img = requests.get(imageUrl).content
            imgPath = './表情包/' + imageName + imageUrl[-4::]
            os.system('clear')
            print('共{}页，正在下载第{}页...'.format(
                len(inputData), inputData.index(page)+1))
            print('当前页面进度{}/{}，当前图片名称：{}。'.format(page.index(imageData) +
                                                  1, len(page), imageName + imageUrl[-4::]))
            with open(imgPath, 'wb') as f:
                f.write(img)
    print('所有项目已下载完毕，共下载{}张表情包。'.format(len(page) * len(inputData)))


def action(url, start, end):
    ret = scanner(url, start, end)
    downloader(ret)


if __name__ == '__main__':
    action('https://www.52doutu.cn/pic/{}/', 1, 2)
