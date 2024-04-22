import data


def loop():
    if data.Box_2().getWater() > 60:
        data.outer().setWarning("警告！水位過高！")