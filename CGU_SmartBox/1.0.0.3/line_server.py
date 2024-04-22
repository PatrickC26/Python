import time

import data
import log
import line_Internet

hasWarning = False


def loop():
    global hasWarning
    if data.Box_2().getWater() > 60:
        if not hasWarning:
            data.outer().setWarning("警告！水位過高！\n目前高度：" + str(data.Box_2().getWater() * 0.3) + "mm")
            hasWarning = True
    else:
        hasWarning = False





def main():
    debug = True
    log.init()
    print("Starting Init Func")
    internetInitSuccessful = line_Internet.init()
    print(internetInitSuccessful)
    while 1:
        try:
            loop()
            if internetInitSuccessful:
                line_Internet.loop()
            else:
                internetInitSuccessful = line_Internet.init()
            time.sleep(0.05)
        except Exception as e:
            log.addError(e)


if __name__ == '__main__':
    main()