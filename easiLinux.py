#!/usr/bin/python3
"""
#time: 2021年9月8日21:51:02
#author: moubigsea
#function: easi use linux. it can find file, monitor service,and run linux original order directly。and it has a nice frame to easily extend fuction
#update: 2022年2月13日17:48:00 i want to make it more easier to use.
"""
import datetime, os, re, subprocess, time
from threading import Timer
# linux need to import the readline below; windows not
import readline



class aiModel():

    def __init__(self, *ags):
        self.aiDict = {'help': self.aiHelp, 'hello': self.aiHello}

    def aiTransfer(self, order):
        """
        解析ai命令
        :param order: 解析传入到ai类的执行命令
        :return: None
        """
        orderlist = order.split(' ')
        length = orderlist.__len__()
        try:
            fuc = self.aiDict.get(orderlist[0])
            if fuc:
                fuc()
        except (TypeError):
            return

    def aiHelp(self, *ags):
        aiHelpInfo = """
        say whatever you what to ask.it will be upgrade later.
        """
        print(aiHelpInfo)

    def aiHello(self, *ags):
        """
        随机响应，hello
        :param ags:
        :return:
        """
        hello = """
        hello,i'm eL, created by bigSea at 13 Sep. 2021.
        """
        print(hello)

class linuxModule():
    def __init__(self, *ags):
        """
        linux原生的命令处理模块，废弃，当前可以直接使用
        :param ags:
        """
        pass

    def beRoot(self):
        pass

class usageWarning():
    def __init__(self, *ags):
        """
        用于查看linux当前系统的资源使用率。包含硬盘、内存、cpu
        :param ags: 命令集
        """
        self.usageDict = {'help': self.usageHelp, 'disk': self.warnDisk, 'cpu': self.warnCpu, 'memory': self.warnMemory,
                          'all': self.warnAll}

    def usageTransfer(self, order):
        orderlist = order.split(' ')
        length = orderlist.__len__()
        try:
            if length == 2:
                self.usageDict.get(orderlist[1])()
            elif length == 1:
                print('warn Module need more params,see \'warn help\'')
        except (TypeError):
            return

    def usageHelp(self, *ags):
        usageHelpInfo = """
        命令         示例                       说明
        warn        :warn disk                 #打印硬盘使用占用信息。
                    :warn cpu                  #打印cpu使用占用信息
                    :warn memory               #打印内存使用占用信息
                    :warn all                  #打印cpu、硬盘、内存、系统平均负载
        """
        print(usageHelpInfo)

    def warnCpu(self, *ags):
        """
        查询cpu的使用率
        :param ags:
        :return:
        """
        cpu_usage = int(self.get_cpu() * 100)
        print("CPU使用率（最大100%）：" + str(cpu_usage) + "%")

    def warnDisk(self, *ags):
        """
        查询硬盘使用率
        :param ags:
        :return:
        """
        statvfs = os.statvfs('/')  # 根目录信息 可根据情况修改
        total_disk_space = statvfs.f_frsize * statvfs.f_blocks
        free_disk_space = statvfs.f_frsize * statvfs.f_bfree
        disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
        disk_usage = int(disk_usage)
        print("硬盘空间使用率（最大100%）：" + str(disk_usage) + "%")

    def warnMemory(self, *ags):
        """
        查询内存使用率
        :param ags:
        :return:
        """
        mem_usage = self.get_mem_usage_percent()
        mem_usage = int(mem_usage[0])
        print("物理内存使用率（最大100%）：" + str(mem_usage) + "%")

    def warnAll(self, *ags):
        """
        查询linux系统常见的3种资源指标使用率
        :param ags:
        :return:
        """
        cpu_usage = int(self.get_cpu() * 100)
        cpu_tip = "CPU使用率（最大100%）：" + str(cpu_usage) + "%"

        statvfs = os.statvfs('/')  # 根目录信息 可根据情况修改
        total_disk_space = statvfs.f_frsize * statvfs.f_blocks
        free_disk_space = statvfs.f_frsize * statvfs.f_bfree
        disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
        disk_usage = int(disk_usage)
        disk_tip = "硬盘空间使用率（最大100%）：" + str(disk_usage) + "%"

        mem_usage = self.get_mem_usage_percent()
        mem_usage = int(mem_usage[0])
        mem_tip = "物理内存使用率（最大100%）：" + str(mem_usage) + "%"

        load_average = os.getloadavg()
        load_tip = "系统负载（三个数值(1分钟、5分钟、15分钟系统平均负载)中有一个超过3就是高）：" + str(load_average)

        all_tip = cpu_tip + '\r\n' + disk_tip + '\r\n' + mem_tip + '\r\n' + load_tip
        print(all_tip)

    # 获取CPU负载信息
    def get_cpu(self, *ags):
        last_worktime = 0
        last_idletime = 0
        f = open("/proc/stat", "r")
        line = ""
        while not "cpu " in line: line = f.readline()
        f.close()
        spl = line.split(" ")
        worktime = int(spl[2]) + int(spl[3]) + int(spl[4])
        idletime = int(spl[5])
        dworktime = (worktime - last_worktime)
        didletime = (idletime - last_idletime)
        rate = float(dworktime) / (didletime + dworktime)
        last_worktime = worktime
        last_idletime = idletime
        if (last_worktime == 0): return 0
        return rate

    # 获取内存负载信息
    def get_mem_usage_percent(self, *ags):
        try:
            f = open('/proc/meminfo', 'r')
            for line in f:
                if line.startswith('MemTotal:'):
                    mem_total = int(line.split()[1])
                elif line.startswith('MemFree:'):
                    mem_free = int(line.split()[1])
                elif line.startswith('Buffers:'):
                    mem_buffer = int(line.split()[1])
                elif line.startswith('Cached:'):
                    mem_cache = int(line.split()[1])
                elif line.startswith('SwapTotal:'):
                    vmem_total = int(line.split()[1])
                elif line.startswith('SwapFree:'):
                    vmem_free = int(line.split()[1])
                else:
                    continue
            f.close()
        except:
            return None
        physical_percent = self.usage_percent(mem_total - (mem_free + mem_buffer + mem_cache), mem_total)
        virtual_percent = 0
        if vmem_total > 0:
            virtual_percent = self.usage_percent((vmem_total - vmem_free), vmem_total)
        return physical_percent, virtual_percent

    def usage_percent(self, use, total):
        try:
            ret = (float(use) / total) * 100
        except ZeroDivisionError:
            raise Exception("ERROR - zero division error")
        return ret

    # 获取系统占用信息
    def sys_info(self, *ags):
        load_average = os.getloadavg()
        load_tip = "系统负载（三个数值中有一个超过3就是高）：" + str(load_average)
        return load_tip

    # 获取计算机当前时间
    def time_info(self, *ags):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        return "主机的当前时间：%s" % now_time

    # 获取计算机主机名称
    def hostname_info(self, *ags):
        hostnames = os.popen("hostname").read().strip()
        return "你的主机名是: %s" % hostnames

    # 获取IP地址信息
    def ip_info(self, *ags):
        ipadd = os.popen("ip a| grep ens192 | grep inet | awk '{print $2}'").read().strip()
        return ipadd

    # 获取根的占用信息
    def disk_info_root(self, *ags):
        child = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
        out = child.stdout.readlines()

        for item in out:
            line = item.strip().split()
            # 我这里只查看centos的根
            if '/dev/mapper/centos-root' in line:
                title = [u'-文件系统-', u'--容量-', u'-已用-', u'-可用-', u'-已用-', u'-挂载点--']
                content = "\t".join(title)
                if eval(line[4][0:-1]) > 60:
                    line[0] = 'centos-root'
                    content += '\r\n' + '\t'.join(line)
                    return content

class gameModule():
    def __init__(self, *ags):
        """
        用于集成一些常用的小游戏。
        :param ags:
        """
        self.gameDict = {'help': self.gameHelp, 'run': self.gameRun, 'install': self.gameInstall, 'list': self.gameList}

    def gameTransfer(self, order=''):
        orderlist = order.split(' ')
        length = orderlist.__len__()
        try:
            if length == 2:
                self.gameDict.get(orderlist[1])()
            elif length >= 3:
                self.gameDict.get(orderlist[1])(orderlist[2])
            elif length == 1:
                print('game need more params,see \'game help\'')
        except (TypeError):
            return

    def gameHelp(self, *ags):
        gameHelpInfo = """
        命令         示例                       说明
        game        :nethack                   #运行nethack
                    :{game name}               #运行{game name}
        game        :install nethack           #安装nethack
                    :install {game name}       #安装{game name}
                    :list                      #目前支持的游戏列表
        """
        print(gameHelpInfo)

    def gameList(self, *ags):
        print('eL support game(untill now): nethack')

    def gameRun(self, gameName=''):
        if 'hack' in gameName.lower():
            os.system('cd ~ && nh/install/games/nethack')
        else:
            print('game named {name} not found! check the order or use f for help'.format(name=gameName))

    def gameInstall(self, gameName=''):
        if 'nethack' in gameName.lower():
            shellstr = 'yum groupinstall -y "development tools" && wget https://nethack.org/download/3.6.6/nethack-366-src.tgz && ' \
                       'tar -xaf nethack-366-src.tgz && cd NetHack-NetHack-3.6.6_Released/ && sys/unix/setup.sh sys/unix/hints/linux && ' \
                       'yum install -y ncurses-devel && make && make install && cd ~'
            subprocess.run(shellstr, shell=True, capture_output=True)
            print('use game run nethack')
        else:
            print('game named {name} not found! check the order or use h for help'.format(name=gameName))

class psModel():
    def __init__(self, *ags):
        """
        ps模块，类linux原生模块，但是更简单了。
        :param ags:
        """
        self.psDict = {'help': self.psHelp}

    def psTransfer(self, order):
        orderlist = order.split(' ')
        length = orderlist.__len__()
        try:
            if length >= 2:
                fuc = self.psDict.get(orderlist[1])
                if fuc:
                    fuc()
                else:
                    self.ps(orderlist[1])
            elif length == 1:
                print('ps need more params, see \'ps help\'')
        except (TypeError):
            return

    def ps(self, applicationName=''):
        """
        ps核心处理函数
        :param applicationName:
        :return:
        """
        # infoStatus 0为正常，256，dead或不存在服务
        infoStatus = subprocess.run('ps -ef|grep {application} |grep -v grep'.format(application=applicationName),
                                    shell=True, capture_output=True)
        statusInfo = subprocess.run('systemctl status {application}'.format(application=applicationName),
                                    shell=True, capture_output=True)
        if statusInfo.returncode == 0:
            pid = re.findall('Main PID: (.+?) \(', statusInfo.stdout.decode())
            portInfo = subprocess.run('netstat -nap | grep {pid}'.format(pid=pid[0].strip()), shell=True,
                                      capture_output=True)
            print(
                '{separate}\r\ninfoStatus: {infoStatus}\r\n{separate}\r\nstatusInfo: {statusInfo}\r\n{separate}\r\nportInfo: {portInfo}\r\n{separate}'.format(
                    infoStatus=infoStatus.stdout.decode(), separate='*-*' * 40, statusInfo=statusInfo.stdout.decode(),
                    portInfo=portInfo.stdout.decode()))
        else:
            print('\'systemctl status {application}\' return error'.format(application=applicationName))

    def psHelp(self, *ags):
        psHelpInfo = """
        命令         示例                       说明
        ps          :ps [applicationName]       #查看进程信息。包含ps文件端口、进程占用端口、运行状态查询
        """
        print(psHelpInfo)

class dogModel():
    def __init__(self, *ags):
        """
        monitor监控实现类。超简单的添加方式。只是定时，便捷添加和移除。
        :param ags:
        """
        self.dogFlag = False  # dog标识
        self.dogBiteInterval = 120  # 监控间隔，secend
        self.timer = ''
        self.foodList = ['docker'] #list中的服务，需要满足，能够用systemctl start命令开启
        self.dogDict = {
            'help': self.dogHelp,
            'time': self.dogSet, 'settime': self.dogSet,
            'add': self.dogAddService, 'setservice': self.dogAddService,
            'bite': self.dogBite, 'go': self.dogBite, 'start': self.dogBite, 'begin': self.dogBite,
            'sit': self.dogSit, 'stop': self.dogSit, 'quit': self.dogSit, 'q': self.dogSit, 'exit': self.dogSit,
            'list': self.dogList, 'show': self.dogList
        }

    def dogTransfer(self, order=''):
        orderlist = order.split(' ')
        length = len(orderlist)
        try:
            if length == 2:
                self.dogDict.get(orderlist[1])()
            elif length >= 3:
                self.dogDict.get(orderlist[1])(orderlist[2])
            elif length == 1:
                #print('easiDog: dog need more params,see \'dog help\'')
                self.dogHelp()
        except TypeError as e:
            return False

    #用于启动服务
    def dogBite(self, *ags):
        print('easiDog: dog监控运行中，当前服务list %s' % self.foodList)
        for applicationName in self.foodList:
            # infoStatus 0为正常，256，dead或不存在服务
            #procCheck = subprocess.run('ps -ef|grep {application} |grep -v grep'.format(application=applicationName), shell=True, capture_output=True)
            procCheck = subprocess.run('ps -ef|grep {application}'.format(application=applicationName),
                                       shell=True, capture_output=True)
            #print('easiDog: {application} 服务运行正常.'.format(application=applicationName))
            if procCheck.returncode != 0:
                subprocess.run('systemctl start {application}'.format(application=applicationName),
                               shell=True, capture_output=True)
                print('easiDog: {application} 未在线，dog监控已尝试重启此服务.'.format(application=applicationName))
        #重置监控间隔时间。
        if self.timer != '':
            self.timer.cancel()
        self.timer = Timer(self.dogBiteInterval, self.dogBite)
        self.timer.start()

    def dogSit(self, *ags):
        if self.timer:
            self.timer.cancel()
            print('easiDog: dog程序已退出，Husky have return home')

    def dogList(self, *ags):
        print('easiDog: dog程序当前监控服务列表为 %s '
              '当前监控时间间隔为 %s '
              '\r\n 可通过dog add 进行添加，详情查看dog help' % (self.foodList, self.dogBiteInterval))

    def dogSet(self, second=120):
        try:
            self.dogBiteInterval = int(second)
            print('easiLog: 监控间隔时间已设置为 %s 秒，每 %s 将打印一次监控日志' % second)
        except Exception as e:
            print('easiLog: 监控间隔时间设置失败，请检查时间参数 %s' % second)
            return

    def dogAddService(self, service=''):
        #校验服务是否可添加内容
        if len(service) == 0:
            return False
        procCheck = subprocess.run('systemctl status {application}'.format(application=service), shell=True, capture_output=True)
        if procCheck.returncode != 0:
            print('easiLog: {service} 添加失败,请检查服务名,或确认是否适用于systemctl指令' % service)
            return False
        self.foodList.append(service)
        print('easiLog: {service} 已添加成功' % service)

    def dogHelp(self, *ags):
        dogHelpInfo = """
        dogMoudule 主要是用于监控服务进程，通过linux内置命令，可以持续对list中的服务进行监控。
        若服务掉线，将通过命令尝试重启服务。这也要求，使用dog进行监控的服务，需要支持systemctl命令。
        命令         示例                 说明
        **********************************************************************************
        dog         :dog time {second}; dog settime {second};        #设置轮询间隔时间。默认为120 s 描述一次。
                    :dog add {service}; dog setservice {{service}}   #添加{service}
                    :dog bite; dog start; dog go; dog begin          #定时监控程序重启。默认为 120s 扫描一次。可通过dog time设置
                    :dog sit; dog stop; dog exit; dog q; dog quit    #将停止dog监控。
                    :dog list; dog show                              #将打印dog 当前服务列表。
        **********************************************************************************
        """
        print(dogHelpInfo)

class easiLinux():
    def __init__(self):
        """
        easiLinux主流程类。命令入口。
        """
        self.flag = True  # 程序运行控制标志
        self.orderHistory = []  # 存历史执行命令的列表

        self.dogM = dogModel()  #实例化dog
        self.psM = psModel()    #实例化ps
        self.aiM = aiModel()    #实例化ai模块，目前还未完善
        self.usageW = usageWarning()    #实例化资源监控模块
        self.gameM = gameModule()       #实例化game模块

        self.sysDict = {
            'dog': self.dogM.dogTransfer,
            'ps': self.psM.psTransfer,
            'find': self.find,
            'run': self.run,
            'warn': self.usageW.usageTransfer,
            'exit': self.exit, 'quit': self.exit, 'stop': self.exit,

            'hello': self.aiM.aiTransfer, 'hi': self.aiM.aiTransfer,
            'game': self.gameM.gameTransfer,

            'help': self.help, 'h': self.help,
            'version': self.version, 'v': self.version,
            'history': self.history
        }

    def mainLinux(self, *args):
        subprocess.run('clear', shell=True)
        self.version()
        while (self.flag):
            try:
                order = input('[mb@easiLinux ~]$ ')
                self.orderHistory.append(order)
                order = order.strip()  # 提出头部空格
                if len(order) == 0:
                    continue
            except KeyboardInterrupt:
                continue
            #处理命令；按空格分区，而后用首字段来匹配sysDict，调取对应实例。
            orderlist = order.split(' ')
            module = self.sysDict.get(orderlist[0])
            if module:
                module(order)
            else:
                try:
                    os.system(order)
                except BaseException:
                    continue

    def help(self, *args):
        helpInfo = """
        命令         示例                        说明
        **********************************************************************************
        dog         :dog time {second}; dog settime {second};        #设置轮询间隔时间。默认为120 s 描述一次。
                    :dog add {service}; dog setservice {{service}}   #添加{service}
                    :dog bite; dog start; dog go; dog begin          #定时监控程序重启。默认为 120s 扫描一次。可通过dog time设置
                    :dog sit; dog stop; dog exit; dog q; dog quit    #将停止dog监控。
                    :dog list; dog show                              #将打印dog 当前服务列表。
        **********************************************************************************
        ps          :ps [applicationName]       #查看进程信息。包含ps文件端口、进程占用端口、运行状态查询
        **********************************************************************************
        warn        :warn disk                  #打印硬盘使用占用信息。
                    :warn cpu                   #打印cpu使用占用信息
                    :warn memory                #打印内存使用占用信息
                    :warn all                   #打印cpu、硬盘、内存、系统平均负载
        **********************************************************************************
        find        :find [filename]            #查找/usr/local/下文件  
        ********************************************************************************** 
        version/v   :version/v                  #查看easiLiunx版本信息
        **********************************************************************************
        game        :game run nethack           #运行nethack
                    :game run {game name}       #运行{game name}
                    :game install nethack       #安装nethack
                    :game install {game name}   #安装{game name}
                    :list                       #目前支持的游戏列表
        **********************************************************************************
        exit        :exit;q,quit                #退出easiLinux
        """
        print(helpInfo)

    def exit(self, *args):
        self.flag = False

    def version(self, *args):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            'Welcome to easiLinux ! {date}\r\neasiLinx 1.1.0 ( Aug 29 2021, 01:13:18) \r\nType \"help\" for more information'.format(
                date=now))

    def history(self, *ags):
        num = 0
        for item in self.orderHistory:
            num += 1
            print('{num}  {item}'.format(num=num, item=item))

    def find(self, fileName=''):
        if len(fileName) == 0:
            print('needs params: \'fileName\'')
            return
        proclist = []
        try:
            procwhich = subprocess.run('which {file}'.format(file=fileName), shell=True, capture_output=True)
            proclist.append(procwhich)
            procwhereis = subprocess.run('whereis {file}'.format(file=fileName), shell=True, capture_output=True)
            proclist.append(procwhereis)
            proclocate = subprocess.run('locate {file}'.format(file=fileName), shell=True, capture_output=True)
            proclist.append(proclocate)
            procfind = subprocess.run('find / -name {file}'.format(file=fileName), shell=True, capture_output=True)
            proclist.append(procfind)
            for proc in proclist:
                if proc.returncode == 0:
                    print('%-50s\r\n{separate}'.format(separate='*-' * 40) % proc.stdout.decode())
                else:
                    pass
        except BaseException:
            return

    def run(self, order=''):
        orderlist = order.split(' ', 1)
        return os.system(orderlist[1])

if __name__ == '__main__':
    el = easiLinux()
    el.mainLinux()
