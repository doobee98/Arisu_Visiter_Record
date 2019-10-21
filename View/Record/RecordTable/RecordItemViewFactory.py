from Utility.Abstract.View.Table.MyItemViewFactory import *


class RecordItemViewFactory(MyItemViewFactory):
    class ItemType(MyItemViewFactory.ItemType):
        Inserted = MyItemViewFactory.ItemType.ReadOnly
        Finished = Inserted | MyItemView.Option.DarkGray

    def __init__(self, parent: 'MyTableView'):
        super().__init__(parent)


