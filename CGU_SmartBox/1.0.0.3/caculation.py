import time

import data

hasWarning = False

def loop():
    global hasWarning
    if data.Box_2().getWater() > 60:
        if not hasWarning:
            data.outer().setWarning("警告！水位過高！\n目前高度：" + str(data.Box_2().getWater()*0.3) + "mm")
            hasWarning = True
    else:
        hasWarning = False


if __name__ == '__main__':
    print(data.Box_2().getWater())
    data.Box_2().setWater(9)
    print(data.Box_2().getWater())
    time.sleep(2)
    data.Box_2().setWater(99)
    print(data.Box_2().getWater())