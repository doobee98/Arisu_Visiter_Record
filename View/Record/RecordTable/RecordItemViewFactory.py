from Utility.TableInterface.View.MyItemViewFactory import *


class RecordItemViewFactory(MyItemViewFactory):
    class ItemType(MyItemViewFactory.ItemType):
        Inserted = MyItemViewFactory.ItemType.ReadOnly
        Finished = Inserted | MyItemView.Option.DarkGray

    def __init__(self, parent: Type['MyTableView']):
        super().__init__(parent)


