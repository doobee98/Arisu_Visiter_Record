from Utility.CryptListModule import *
from Model.Database.DatabaseModel import *
from Model.Record.RecordTableModel import *
from Excel.ExcelFileNameConfig import *
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, Border, Side


class ExcelDBInfo:
    """
    이전 버전의 Excel Database에서 파일을 가져오기 위한 정보 클래스
    * FieldInfo: DatabaseFieldModelConfig의 field를 key로 가지고, 그 필드에 해당하는 데이터 딕셔너리를 value로 가진다.
        title: Excel Database에서의 field name. 실질적으로 사용하지 않는다.
        column: Excel Database에서 key에 해당하는 값(DatabaseModel에 입력되어야 하는 값)을 가지고 있는 column 값.
    * StartRow: 입력받을 데이터가 존재하는 첫 행. EndRow는 importExcelDatabase 함수에서 자체적으로 계산함.
                - 조건: 데이터와 데이터 사이에 빈 행이 있으면 그 후는 인식하지 못한다.
    * excelTextFilter(): 읽은 cell값을 받아서 str로 변환해주는 메소드.
    """
    FieldInfo = {
        '성명': {
            'title': '성명',
            'column': 4
        },
        '생년월일': {
            'title': '생년월일',
            'column': 5
        },
        '차량번호':{
            'title': '차량번호',
            'column': 6
        },
        '소속': {
            'title': '소속',
            'column': 7
        },
        '방문목적': {
            'title': '목적',
            'column': 8
        },
        '비고': {
            'title': '비고(저장만됨)',
            'column': 9
        },
        '최초출입날짜': {
            'title': '최근 들어온 시간',
            'column': 10
        },
        '최근출입날짜': {
            'title': '최근 들어온 시간',
            'column': 10
        }
    }
    StartRow = 16

    @classmethod
    def excelTextFilter(cls, property) -> str:
        """
        :param property: openpyxl을 통해 입력받은 cell값
        :return: 변환된 str값
        """
        if isinstance(property, datetime):
            return property.strftime('%Y-%m-%d')
        elif property is None:
            return ''
        else:
            return property


class ExcelReportInfo:
    """
    마감 파일을 작성할 때 필요한 정보 클래스 (베이스가 되는 마감파일명은 ExcelFileNameConfig에 있음)
    * FieldColumnDict: RecordFieldModelConfig의 field를 key로 가지고, property를 작성할 column 값을 value로 가짐
    * StartRow: 데이터 작성을 시작할 행 값
    * InfoCellAddress: 정보전달 cell의 주소를 가지고 있는 딕셔너리.
                        date - report 작성 날짜, 포맷은 yyMMdd
                        location - report의 장소-근무지, 포맷은 '장소{space}근무지'
    * CellBorder: 데이터가 작성되는 셀에 적용되는 테두리값.
    * setFieldsColumn(): field-column 딕셔너리를 입력받아 그 값을 FieldColumnDict에 적용시킴
    """
    FieldColumnDict = {
        '출입증번호': 1,
        '성명': 2,
        '생년월일': 3,
        '비고': 4,
        '차량번호': 5,
        '소속': 6,
        '방문목적': 7,
        '반출입물품명': 8,
        '반입/반출량': 9,
        '들어오다시간': 10,
        '들어오다근무자': 11,
        '나가다시간': 12,
        '나가다근무자': 13
    }
    StartRow = 7
    InfoCellAddress = {
        'date': 'A1',
        'location': 'D1'
    }
    CellBorder = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                         bottom=Side(style='thin'))

    @classmethod
    def setFieldsColumn(cls, field_column_dict: Dict[str, int]) -> bool:
        """
        :param field_column_dict
        :return: **
            field_column_dict의 입력 결과 FieldColumnDict에 column 중복값이 발생하였다면,
            변경을 취소하고 변경 실패의 False를 반환함
            중복값이 발생하지 않는다면 변경을 유지하고 True를 반환함.
        """
        original_dict = cls.FieldColumnDict.copy()
        for field, column in field_column_dict.items():
            if field in cls.FieldColumnDict.keys():
                cls.FieldColumnDict[field] = column
        column_list = list(field_column_dict.values())
        if len(column_list) != len(set(column_list)):
            cls.FieldColumnDict = original_dict.copy()
            return False
        else:
            return True


class ExcelFileModule:
    @classmethod
    def importExcelDatabase(cls, location_string: str, file_name: str) -> DatabaseModel:
        """
        file_name(ExcelFileNameConfig 참조)에 있는 이전 버전 Excel Database를
        Arisu.exe에서 사용할 수 있는 iml Database Model로 변환함.
        만들어지는 database의 location은 location string 인자를 따름
        """
        db_file = load_workbook(file_name)
        db_sheet = db_file[ExcelFileNameConfig.getExcelDatabaseSheetName()]  # Sheet1
        info = ExcelDBInfo
        start_row = info.StartRow
        end_row = db_sheet.max_row
        # for row_iter, row_cells in enumerate(db_sheet, 1):
        #     if row_iter >= start_row:
        #         if all(c.value is None for c in row_cells):
        #             end_row = row_iter - 1
        #             break
        print('setting')
        db_model = DatabaseModel(location_string, file_decorator='../')
        if db_model.isFileExist():
            return None
        db_model.blockSignals(True)
        print('load start')
        for row_iter in range(start_row, end_row + 1):
            property_dict = {field: '' for field in DatabaseFieldModelConfig.getFieldList()}
            for field_iter, info_iter in info.FieldInfo.items():
                #field_name = info_iter['title']
                field_column = info_iter['column']
                property = db_sheet.cell(row=row_iter, column=field_column).value
                property = info.excelTextFilter(property)
                property_dict[field_iter] = property
            db_model.addData(VisitorModel(property_dict))
            print(row_iter, 'row data added')
        db_model.blockSignals(False)
        db_file.close()
        #return None
        print('finish')
        db_model.save()
        return db_model

    @classmethod
    def exportExcelRecord(cls, record_table_model: RecordTableModel) -> str:
        """
        인자로 받은 RecordTableModel을 엑셀 마감 파일로 바꿈.
        반환하는 값은 생성한 마감 파일의 이름
            1. date와 location 위치에 record의 날짜와 record의 location을 삽입함
            2. recordTable의 모든 데이터를 info에 맞춰서 작성함
            3. report 파일을 생성하고 그 이름을 반환
        """
        file_decorator = '../'
        date_string = record_table_model.getRecordDate()
        location_string = record_table_model.getLocation()
        info = ExcelReportInfo
        wb = load_workbook(file_decorator + ExcelFileNameConfig.getExcelReportSampleName())
        sheet = wb['date']
        sheet.title = date_string
        sheet[info.InfoCellAddress['date']] = datetime.strptime(date_string, '%y%m%d').strftime('%Y-%m-%d')  # todo datetime으로 제대로 형식맞춰서 표시해야함
        title_string = str(sheet[info.InfoCellAddress['location']].value)
        sheet[info.InfoCellAddress['location']] = title_string.replace('location', location_string)

        row_iter = info.StartRow
        for data_iter in record_table_model.getDataList():
            if data_iter.isTakeoverRecord():
                col_list = info.FieldColumnDict.values()
                min_col, max_col = min(col_list), max(col_list)
                sheet.merge_cells(start_row=row_iter, start_column=min_col, end_row=row_iter, end_column=max_col)
                sheet.cell(row=row_iter, column=min_col).value = data_iter.getProperty('인수인계')
                sheet.cell(row=row_iter, column=min_col).alignment = Alignment(horizontal='center', vertical='center')
                sheet.cell(row=row_iter, column=min_col).font = Font(bold=True)
                for col_iter in range(min_col, max_col+1):
                    sheet.cell(row=row_iter, column=col_iter).border = info.CellBorder
            else:
                for field_iter, col_iter in info.FieldColumnDict.items():
                    sheet.cell(row=row_iter, column=col_iter).value = data_iter.getProperty(field_iter)
                    sheet.cell(row=row_iter, column=col_iter).alignment = Alignment(horizontal='center',
                                                                                    vertical='center')
                    sheet.cell(row=row_iter, column=col_iter).border = info.CellBorder
            # 하단은 inserted와 finished 데이터만 삽입하는 코드
            # elif data_iter.getState() in [RecordModel.State.Inserted, RecordModel.State.Finished]:  
            # pass
            # else:
            #     continue
            row_iter += 1
        file_name = FileNameConfig.getReportName(location_string, date_string)
        wb.save(file_decorator + file_name)
        wb.close()
        return file_name
