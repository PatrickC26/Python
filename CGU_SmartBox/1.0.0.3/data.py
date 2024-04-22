import time
from datetime import datetime, timedelta

import log
import setting

location = setting.fileLocation + 'database/'

errString_size = "ERROR(1) : Due to value too large or too small, with value : "
errString_type = "ERROR(3) : Data Type mismatch, with value : "

# data_mode
data_value = 1
data_time = 2

fileExt = ".txt"

dataProcess_get_num_loop: int = 0


class dataProcess:
    class get:
        def __get(self, id, mode: int = data_value):
            allDataOriginal = "$,!"  # <start_token><data>,<time(yyyy/MM/dd hh:mm:ss)><end_token>
            try:
                with open(location + id + fileExt) as input_file:
                    dataS = input_file.read()
                    if not (("$" in dataS) & ("," in dataS) & ("!" in dataS)):
                        with open(location + id + fileExt, "w") as outputFile:
                            outputFile.write(allDataOriginal)
                        return self.__get(id, mode)
                    if mode == data_value:
                        return dataS[dataS.index("$") + 1:dataS.rfind(',')]
                    elif mode == data_time:
                        return dataS[dataS.rfind(',') + 1:dataS.index('!')]
            except FileNotFoundError:
                try:
                    print(location + id + fileExt)
                    with open(location + id + fileExt, "x") as outputFile:
                        log.addlog("File ERROR, had add original data")
                        outputFile.write(allDataOriginal)
                    return ""
                except FileNotFoundError:
                    log.addlog("[ERROR] No Directory(Folder) @ __get")
                except Exception as e1:
                    log.addError(e1)
            except Exception as e:
                log.addError(e)
            return ""

        def getNum(self, id):
            global dataProcess_get_num_loop
            try:
                dataS = self.__get(id)
                if '.' in dataS:
                    return float(self.__get(id))
                else:
                    return int(self.__get(id))
            except ValueError:
                if dataProcess_get_num_loop > 5:
                    dataProcess_get_num_loop = 0
                    return 0
                dataProcess.set().setNum(id, 0)
                dataProcess_get_num_loop += 1
                return self.__class__().getNum(id)
            except Exception as e:
                log.addError(e)
            return 0

        def getString(self, id):
            try:
                return self.__get(id)
            except Exception as e:
                log.addError(e)
            return 0

        def getTimeCode(self, id):
            try:
                return self.__get(id, mode=data_time)
            except Exception as e:
                log.addError(e)
            return 0

    class set:
        def __set(self, id, newdata: str):
            allDataOriginal = "$,!"  # <start_token><data>,<time(yyyy/MM/dd hh:mm:ss)><end_token>
            try:
                # with open(location + id + fileExt) as input_file:
                #     dataS = input_file.read()
                #     if not (("$" in dataS) & ("," in dataS) & ("!" in dataS)):
                #         with open(location + id + fileExt, "w") as outputFile:
                #             outputFile.write(allDataOriginal)
                #         return False
                with open(location + id + fileExt, "w") as outputFile:
                    dataS = "$" + newdata + "," + timeString() + "!"
                    outputFile.write(dataS)
                    return True
            except FileNotFoundError:
                try:
                    with open(location + id + fileExt, "x") as outputFile:
                        outputFile.write(allDataOriginal)
                        log.addlog("File ERROR, had add original data")
                    return self.__set(id, newdata)
                except FileNotFoundError:
                    log.addlog("[ERROR] No Directory(Folder) @ __set")
                except Exception as e1:
                    log.addError(e1)
            except Exception as e:
                log.addError(e)
            return False

        def setNum(self, id, value: int or float):
            try:
                if int is value.__class__:
                    pass
                elif float is value.__class__:
                    pass
                else:
                    print("@setNum -> " + errString_type + str(value) + " & id is : " + str(id))
                    return False
                return self.__set(id, str(value))
            except Exception as e:
                log.addError(e)
            return False

        def setString(self, id, value: str):
            return self.__set(id, str(value))


def timeString():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Box_1:
    def getTemperature(self):
        return int(dataProcess.get().getNum("A/t"))

    def getHumidity(self):
        return int(dataProcess.get().getNum("A/h"))

    def getVoltage(self):
        return int(dataProcess.get().getNum("A/v"))

    def getRFID(self):
        return dataProcess.get().getString("A/r")

    def getMSG(self):
        return dataProcess.get().getString("A/g")

    def getRFIDinfo(self):
        return dataProcess.get().getString("A/a")

    def getTemperatureTime(self):
        return dataProcess.get().getTimeCode("A/t")

    def getHumidityTime(self):
        return dataProcess.get().getTimeCode("A/h")

    def getVoltageTime(self):
        return dataProcess.get().getTimeCode("A/v")

    def getRFIDTime(self):
        return dataProcess.get().getTimeCode("A/r")

    def getMSGTime(self):
        return dataProcess.get().getTimeCode("A/g")

    def getRFIDinfoTime(self):
        return dataProcess.get().getTimeCode("A/a")

    # ------------ set void ------------------

    def setTemperature(self, value: int):
        if (value < -100) | (value > 100):
            print("@1Temperature -> " + errString_size + str(value))
            return False
        else:
            return dataProcess.set().setNum("A/t", int(value))

    def setHumidity(self, value: int or float):
        if (value < 0) | (value > 100):
            print("@1Humidity -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("A/h", int(value))

    def setVoltage(self, value: int or float):
        if (value < 0) | (value > 500):
            print("@1Voltage -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("A/v", int(value))

    def setRFID(self, value: str):
        return dataProcess.set().setString("A/r", str(value))

    def setMSG(self, value: str):
        return dataProcess.set().setString("A/g", str(value))

    def setRFIDinfo(self, value: str):
        return dataProcess.set().setString("A/a", str(value))


class Box_2:
    def getTemperature(self):
        return int(dataProcess.get().getNum("B/t"))

    def getHumidity(self):
        return int(dataProcess.get().getNum("B/h"))

    def getVoltage(self):
        return int(dataProcess.get().getNum("B/v"))

    def getWater(self):
        return int(dataProcess.get().getNum("B/w"))

    def getServo(self):
        return int(dataProcess.get().getNum("B/s"))

    def getTemperatureTime(self):
        return (dataProcess.get().getTimeCode("B/t"))

    def getHumidityTime(self):
        return (dataProcess.get().getTimeCode("B/h"))

    def getVoltageTime(self):
        return (dataProcess.get().getTimeCode("B/v"))

    def getWaterTime(self):
        return (dataProcess.get().getTimeCode("B/w"))

    def getServoTime(self):
        return (dataProcess.get().getTimeCode("B/s"))

    # ------------ set void ------------------

    def setTemperature(self, value: int):
        if (value < -100) | (value > 100):
            print("@2Temperature -> " + errString_size + str(value))
            return False
        else:
            return dataProcess.set().setNum("B/t", int(value))

    def setHumidity(self, value: int or float):
        if (value < 0) | (value > 100):
            print("@2Humidity -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("B/h", int(value))

    def setVoltage(self, value: int or float):
        if (value < 0) | (value > 500):
            print("@2Voltage -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("B/v", int(value))

    def setWater(self, value: int or float):
        if (value < 0) | (value > 100):
            print("@Voltage -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("B/w", int(value))

    def setServo(self, value: int or float):
        if (value < 0) | (value > 180):
            print("@Voltage -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("B/s", int(value))


class Box_3:
    def getTemperature(self):
        return int(dataProcess.get().getNum("C/t"))

    def getHumidity(self):
        return int(dataProcess.get().getNum("C/h"))

    def getVoltage(self):
        return int(dataProcess.get().getNum("C/v"))

    def getMotor(self):
        return int(dataProcess.get().getNum("C/m"))

    def getSpeed(self):
        return int(dataProcess.get().getNum("C/s"))

    def getTemperatureTime(self):
        return dataProcess.get().getTimeCode("C/t")

    def getHumidityTime(self):
        return dataProcess.get().getTimeCode("C/h")

    def getVoltageTime(self):
        return dataProcess.get().getTimeCode("C/v")

    def getMotorTime(self):
        return dataProcess.get().getTimeCode("C/m")

    def getSpeedTime(self):
        return dataProcess.get().getTimeCode("C/s")

    # ------------ set void ------------------

    def setTemperature(self, value: int):
        if (value < -100) | (value > 100):
            print("@3Temperature -> " + errString_size + str(value))
            return False
        else:
            return dataProcess.set().setNum("C/t", int(value))

    def setHumidity(self, value: int or float):
        if (value < 0) | (value > 100):
            print("@3Humidity -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("C/h", int(value))

    def setVoltage(self, value: int or float):
        if (value < 0) | (value > 500):
            print("@3Voltage -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("C/v", int(value))

    def setMotor(self, value: int or float):
        if (value < 0) | (value > 100):
            print("@Motor -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("C/m", int(value))

    def setSpeed(self, value: int or float):
        if (value < 0) | (value > 1800):
            print("@Speed -> " + errString_size + str(value))
            return False
        return dataProcess.set().setNum("C/s", int(value))


class outer:

    def getLineUser(self):
        return dataProcess.get().getString("line/user")

    def getLineTime(self):
        return dataProcess.get().getString("line/time")

    def addLineUser(self, value: str):
        return dataProcess.set().setString("line/user", value)

    def addLineTime(self, value: str):
        return dataProcess.set().setString("line/time", value)

    def getInternetCheck(self):
        try:
            result = dataProcess.get().getString("conn")
            if result == "1":
                return True
            elif result == "0":
                return False
            else:
                self.__class__().setInternetCheck(False)
                return False
        except Exception as e:
            log.addError(e)
            return False

    def getWarning(self):
        return dataProcess.get().getString("warning")

    # ------ put Data ------

    def setInternetCheck(self, value: bool):
        if not (bool is value.__class__):
            print("@Internet Check -> " + errString_type + str(value))
            return False
        if value:
            return dataProcess.set().setString("conn", "1")
        else:
            return dataProcess.set().setString("conn", "0")

    def setWarning(self, value: str):
        return dataProcess.set().setString("warning", str(value))


class version:
    # ----- voids --------
    def getVersion(self, id: str):
        return dataProcess.get().getString("version/" + id)

    def setVersion(self, id: str, versionS: str):
        return dataProcess.set().setString("version/" + id, str(versionS))


Box1LastTime = 0
Box2LastTime = 0
Box3LastTime = 0


class timeModule:
    # ======= Time ============
    # ----- voids --------
    def __getTimeData(self, id: str):
        timeS = dataProcess.get().getString("time/" + id)
        if not (timeS == ""):
            return timeS
        else:
            self.__class__().__setTimeDataZero("time/" + id)
        return "0001/01/01,00:00:00"

    def __setTimeDataZero(self, id: str):
        date_time = "0001/01/01,00:00:00"
        return dataProcess.set().setString(id, str(date_time))

    def __setTimeData(self, id: str):
        date_time = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
        return dataProcess.set().setString("time/" + id, str(date_time))

    # ----- GET method --------
    def getBox1Time(self):
        return self.__class__().__getTimeData("A")

    def getBox2Time(self):
        return self.__class__().__getTimeData("B")

    def getBox3Time(self):
        return self.__class__().__getTimeData("C")

    # ----- set Method --------

    def setBox1Time(self):
        return self.__class__().__setTimeData("A")

    def setBox2Time(self):
        return self.__class__().__setTimeData("B")

    def setBox3Time(self):
        return self.__class__().__setTimeData("C")

    # ----- Get status --------

    def __getStatusData(self, id: str):
        id = "time/status_" + id
        return dataProcess.get().getString(id)

    def __setStatusData(self, id: str, value: str):
        id = "time/status_" + id
        return dataProcess.set().setString(id, value)

    def getBox1Status(self):
        return self.__class__().__getStatusData("A") == "1"

    def getBox2Status(self):
        return self.__class__().__getStatusData("B") == "1"

    def getBox3Status(self):
        return self.__class__().__getStatusData("C") == "1"

    # --- Set Status -----
    def renewALLStatus(self):
        global Box1LastTime
        global Box2LastTime
        global Box3LastTime

        timeFormat = '%Y-%m-%d,%H:%M:%S'
        ti = timeModule()
        millisN = time.time() - 2
        try:
            Box1Time = datetime.strptime(ti.getBox1Time(), timeFormat)
            Box2Time = datetime.strptime(ti.getBox2Time(), timeFormat)
            Box3Time = datetime.strptime(ti.getBox3Time(), timeFormat)

            # Use 1 min as buffer time
            oktime = datetime.now() + timedelta(hours=0, minutes=0, seconds=-5)

            if Box1Time > oktime:
                self.__class__().__setStatusData("A", "1")
                Box1LastTime = time.time()
            elif Box1LastTime > millisN:
                self.__class__().__setStatusData("A", "0")
                log.addlog("Motor Turned off")
                log.addlog(str(Box1Time))

            if Box2Time > oktime:
                self.__class__().__setStatusData("B", "1")
                Box2LastTime = time.time()
            elif Box2LastTime > millisN:
                self.__class__().__setStatusData("B", "0")
                log.addlog("Motor Turned off")
                log.addlog(str(Box1Time))

            if Box3Time > oktime:
                self.__class__().__setStatusData("C", "1")
                Box3LastTime = time.time()
            elif Box3LastTime > millisN:
                self.__class__().__setStatusData("C", "0")
                log.addlog("Motor Turned off")
                log.addlog(str(Box1Time))

        except Exception as e:
            log.addError(e)
