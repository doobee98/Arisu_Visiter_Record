import sys
from win32comext.shell.shell import ShellExecuteEx, IsUserAnAdmin
from win32con import SW_SHOWNORMAL
from Setup.View.SetupMainView import *

def uac_require():
    asadmin = 'asadmin'
    try:
        if not IsUserAnAdmin():
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [asadmin])
            ShellExecuteEx(lpVerb='runas', lpFile = sys.executable, lpParameters=params, nShow=SW_SHOWNORMAL)
            sys.exit()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    if uac_require():
        pass
    else:
        sys.exit()

    try:
        app = QApplication(sys.argv)

        m = SetupMainView()

        if IsUserAnAdmin():
            m.setWindowTitle(m.windowTitle() + ' : 관리자')

        m.showNormal()

        app.exec_()
    except Exception as e:
        print(e)
    finally:
        print('@@Finish program@@')