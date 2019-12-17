"""
ShowingView
User에게 보여지는 Window들은 이 인터페이스를 상속함.
activeView 메소드를 통해 실제 현재로 작업되는 current View를 얻을 수 있음
"""


class ShowingView:
    def activeView(self) -> 'ShowingView':
        raise NotImplementedError