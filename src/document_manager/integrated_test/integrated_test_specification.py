from src.excel.excel import Excel
from src.excel.excel_specification import ExcelSpecification
from src.excel.sheet.excel_sheet import ExcelSheet
from src.excel.sheet.cell.excel_sheet_cell import ExcelSheetCell
from src.excel.sheet.auto_filter.excel_sheet_auto_filter import ExcelSheetAutoFilter
from src.excel.sheet.cell.alignment.excel_sheet_cell_alignment import ExcelSheetCellAlignment
from src.excel.sheet.cell.border.excel_sheet_cell_border import ExcelSheetCellBorder
from src.excel.sheet.cell.fill.excel_sheet_cell_fill import ExcelSheetCellFill
from src.excel.sheet.cell.font.excel_sheet_cell_font import ExcelSheetCellFont
from src.excel.sheet.image.excel_sheet_image import ExcelSheetImage
from src.excel.sheet.image.excel_sheet_image_size import ExcelSheetImageSize
from src.excel.sheet.cell.line.excel_sheet_cell_line import ExcelSheetCellLine
from src.excel.sheet.cell.style.excel_sheet_cell_style import ExcelSheetCellStyle

class IntegratedTestSpecification():
    @classmethod
    def createTestDataSheet(cls, testData):
        # dictから再帰的に値を取り出す一時関数
        def extractData(data, path=None):
            if path is None:
                path = []

            results = []

            if isinstance(data, dict):
                for key, value in data.items():
                    # print(f"DICT: path={path + [key]} → dive into {value}")
                    results.extend(extractData(value, path + [key]))
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    # print(f"LIST: path={path + [index]} → dive into {item}")
                    results.extend(extractData(item, path + [index]))
            else:
                # print(f"VALUE: path={path} → value={data}")
                results.append((path, data))

            return results

        # テストデータから行列データ作成
        matrix = []
        for keys, value in extractData(testData.getData()):
            matrix.append(keys + [value])

        # 行列データの列の長さを揃える
        maxLen = max(len(row) for row in matrix)
        matrix = [row[:-1] + [""] * (maxLen - len(row)) + [row[len(row) - 1]] for row in matrix]

        # シートの行作成
        sheetRows = []
        # ヘッダ部
        line = ExcelSheetCellLine('thin', '000000')
        headerCells = []
        for index in range(0, maxLen - 1):
            headerCells.append(ExcelSheetCell(
                f"キー{index + 1}",
                ExcelSheetCellStyle(
                    ExcelSheetCellBorder(line, line, line, line),
                    fill = ExcelSheetCellFill('solid', 'c8e6c6')
                )
            ))
        headerCells.append(ExcelSheetCell(
                f"値",
                ExcelSheetCellStyle(
                    ExcelSheetCellBorder(line, line, line, line),
                    fill = ExcelSheetCellFill('solid', 'c8e6c6')
                )
            ))
        sheetRows.append(headerCells)
        # データ部
        for rowIndex, row in enumerate(matrix):
            sheetRowCells = []
            for cellIndex, cell in enumerate(row):
                # パディングセルか否か
                # オートフィルタは行単位のため列方向の結合の基準は空欄でいい
                if cell == "":
                    sheetRowCells.append(cls.createMergeCell(
                        cell,
                        isTop = True,
                        isBottom = True,
                        isRight  = cellIndex == len(matrix[rowIndex]) - 1,
                        isLeft   = False
                    ))
                else:
                    sheetRowCells.append(cls.createMergeCell(
                        cell,
                        isTop    = rowIndex == 0                          or row[:cellIndex] != matrix[rowIndex-1][:cellIndex] or cell != matrix[rowIndex - 1][cellIndex],
                        isBottom = (rowIndex == len(matrix) - 1)          or row[:cellIndex] != matrix[rowIndex+1][:cellIndex] or cell != matrix[rowIndex + 1][cellIndex],
                        isRight  = cellIndex == len(matrix[rowIndex]) - 1 or matrix[rowIndex][cellIndex + 1] != "",
                        isLeft   = cellIndex == 0                         or matrix[rowIndex][cellIndex - 1] != cell
                    ))
            sheetRows.append(sheetRowCells)

        alphabet = ExcelSpecification.getAlphabet(maxLen - 1)

        return ExcelSheet(
            "テストデータ",
            sheetRows,
            cls.getAdjustedColumnWidths(sheetRows),
            ExcelSheetAutoFilter(f"A1:{alphabet}1")
        )

    @classmethod
    def createPerspectiveSheet(cls, config):
        perspectives = config.getPerspectives()
        rows = []
        for name in perspectives:
            cells = [
                ExcelSheetCell(name),
                ExcelSheetCell('') if perspectives[name] == None else ExcelSheetCell(perspectives[name])
            ]
            rows.append(cells)
        return ExcelSheet("テスト観点", rows, cls.getAdjustedColumnWidths(rows))

    @classmethod
    def createStatusSheet(cls):
        values = [
            ['テストケース数', f"=MAX(テストケース!A:A)"],
            ['実施予定数', f'=B2 - COUNTIF(テストケース!G:G,"-")'],
            ['正常数', f'=COUNTIF(テストケース!G:G,"○")'],
            ['エラー数', f'=COUNTIF(テストケース!G:G,"×")'],
            ['進捗率', '=B3/B2'],
        ]

        # 行作成
        rows = [[ExcelSheetCell('{環境名}')]]
        for _, row in enumerate(values):
            cells = []
            for cellIndex, cell in enumerate(row):
                line = ExcelSheetCellLine('thin', '000000')
                cellStyle = ExcelSheetCellStyle(
                    ExcelSheetCellBorder(line, line, line, line),
                    ExcelSheetCellFill('solid', 'c8e6c6') if cellIndex == 0 else ExcelSheetCellFill('solid', 'ffffff'),
                    ExcelSheetCellAlignment('top'),
                )
                cell = ExcelSheetCell(cell, cellStyle)
                cells.append(cell)
            rows.append(cells)

        # 列幅
        widths = [14, 8]

        return ExcelSheet("実施状況", rows, widths)

    # 事前準備・注意点シート
    @classmethod
    def createPreparationSheet(cls, preparation):
        # 行作成
        rows = []
        for value in [] if preparation == None else preparation.getList():
            cell = ExcelSheetCell(value)
            rows.append([cell])

        return ExcelSheet("事前準備・注意点", rows)

    @classmethod
    def createTestCaseAndEvidenceSheet(cls, integratedTest, integratedTestConfig):
        # シート行の作成
        testCaseSheetRows = [cls.createTestCaseSheetHeaderCells()]
        evidenceSheetRows = []

        # テストオブジェクトと共通のテストを結合
        elements = [integratedTestConfig.getBlock()] + integratedTest.getBlocks()

        # テストオブジェクトのテストケース行の作成
        headerLen = len(testCaseSheetRows)
        testCaseCount = 0
        evidenceSheetRowLen = 30
        evidenceSheetRowIndex = 1
        for _, element in enumerate(elements):
            for perspectiveIndex, perspective in enumerate(element.getPerspectives()):
                for caseIndex, case in enumerate(perspective.getCases()):
                    testCaseCount += 1

                    # 要素名、テスト観点が同じか
                    isElementTop = perspectiveIndex == 0 and caseIndex == 0
                    isElementLast = perspectiveIndex == len(element.getPerspectives()) - 1 and caseIndex == len(perspective.getCases()) - 1
                    isPerspectiveTop = caseIndex == 0
                    isPerspectiveLast = caseIndex == len(perspective.getCases()) - 1

                    # IDセル
                    IdCell = cls.createMergeCell("=ROW()-1")
                    # 要素セル
                    elementCell = cls.createMergeCell(element.getName(), isElementTop, isElementLast)
                    # テスト観点セル
                    perspectiveCell = cls.createMergeCell(
                        perspective.getName(),
                        isPerspectiveTop,
                        isPerspectiveLast,
                        validationData = '=テスト観点!$A:$A'
                    )
                    # テストパターンセル
                    patternCell = cls.createMergeCell(case.getPattern())

                    # 手順セル
                    procedures = ['・' + procedure for procedure in case.getProcedures()]
                    procedureCell = cls.createMergeCell(
                        "\r\n".join(procedures + ['・結果をエビデンスシートに記載(クリックで記載場所へ)'] if case.needsEvidence else procedures),
                        wrapText  = True,
                        hyperLink = f"#エビデンス!A{evidenceSheetRowIndex}" if case.needsEvidence else None
                    )
                    if case.needsEvidence:
                        value = element.getName() + '/' + perspective.getName() + '/' + ''.join([forecast for forecast in case.getForecasts()]) + '(クリックでテストケースへ)'
                        evidenceSheetRows.append([ExcelSheetCell(
                            value,
                            hyperLink = f"#テストケース!E{testCaseCount + headerLen}"
                        )])

                        for _ in range(evidenceSheetRowLen - 1):
                            evidenceSheetRows.append([])
                        evidenceSheetRowIndex = evidenceSheetRowIndex + evidenceSheetRowLen

                    # 想定結果セル
                    forecastCell = cls.createMergeCell(
                        "\r\n".join(['・' + forecast for forecast in case.getForecasts()]),
                        wrapText = True
                    )
                    # 実施結果、実施日、実施者、備考セル
                    resultCell = cls.createMergeCell(validationData = '"○, ×, -"')
                    dateCell = cls.createMergeCell()
                    personCell = cls.createMergeCell()
                    remarkCell = cls.createMergeCell()

                    testCaseSheetRows.append([
                        IdCell,
                        elementCell,
                        perspectiveCell,
                        patternCell,
                        procedureCell,
                        forecastCell,
                        resultCell,
                        dateCell,
                        personCell,
                        remarkCell,
                    ])

        # 列幅
        widths = [5, 16, 18, 16, 46, 40, 11, 9, 9, 40]

        # マトリクステストシート
        matrixSheets = []
        line = ExcelSheetCellLine('thin', '000000')
        for _, matrix in enumerate(integratedTest.getMatrices()):
            matrixSheetRows = []

            # ヘッダ部
            matrixSheetRowCells = []
            matrixHeaderValues = ['No.'] + matrix.getHeader() + ['実施結果']
            for _, value in enumerate(matrixHeaderValues):
                matrixSheetRowCells.append(ExcelSheetCell(value, ExcelSheetCellStyle(
                    ExcelSheetCellBorder(line, line, line, line),
                    fill = ExcelSheetCellFill('solid', 'c8e6c6')
                )))
            matrixSheetRows.append(matrixSheetRowCells)

            # データ部
            evidenceIndex = matrix.getEvidenceIndex()
            for matrixRowIndex, matrixRow in enumerate(matrix.getData()):
                matrixSheetRowCells = [ExcelSheetCell('=ROW()-1', ExcelSheetCellStyle(
                    ExcelSheetCellBorder(line, line, line, line),
                    ExcelSheetCellFill('solid', 'ffffff')
                ))]
                for index, matrixRowValue in enumerate(matrixRow):
                    if index == evidenceIndex and matrixRowValue == "要":
                        matrixSheetRowCells.append(ExcelSheetCell(
                            '要(クリックでエビデンスへ)',
                            ExcelSheetCellStyle(
                                ExcelSheetCellBorder(line, line, line, line),
                                ExcelSheetCellFill('solid', 'ffffff')
                            ),
                            hyperLink = f"#エビデンス!A{evidenceSheetRowIndex}")
                        )

                        # エビデンスシートにマトリクステストケースへのリンクを追加
                        # +1はNo.列を考慮
                        alphabet = ExcelSpecification.getAlphabet(evidenceIndex + 1)
                        evidenceSheetRows.append([ExcelSheetCell(
                            matrix.getName() + "/No." + str(matrixRowIndex + 1) + "(クリックでマトリクスへ)",
                            # +1はヘッダ部とインデックスが0始まりであることの考慮
                            hyperLink = f"#{matrix.getName()}!{alphabet}{matrixRowIndex + 1 + 1}"
                        )])
                        for _ in range(evidenceSheetRowLen - 1):
                            evidenceSheetRows.append([])

                        evidenceSheetRowIndex = evidenceSheetRowIndex + evidenceSheetRowLen
                    else:
                        matrixSheetRowCells.append(ExcelSheetCell(matrixRowValue, ExcelSheetCellStyle(
                            ExcelSheetCellBorder(line, line, line, line),
                            ExcelSheetCellFill('solid', 'ffffff')
                        )))
                    if index == len(matrixRow) - 1:
                        matrixSheetRowCells.append(ExcelSheetCell(
                            style = ExcelSheetCellStyle(
                                ExcelSheetCellBorder(line, line, line, line),
                                ExcelSheetCellFill('solid', 'ffffff')
                            ),
                            validationData = '"○, ×, -"'
                        ))
                matrixSheetRows.append(matrixSheetRowCells)
            # オートフィルタ
            alphabet = ExcelSpecification.getAlphabet(len(matrixSheetRows[0]) - 1)
            matrixSheets.append(ExcelSheet(
                matrix.getName(),
                matrixSheetRows,
                cls.getAdjustedColumnWidths(matrixSheetRows),
                ExcelSheetAutoFilter(f"A1:{alphabet}1")))

        sheets = [ExcelSheet(
            "テストケース",
            testCaseSheetRows,
            widths,
            ExcelSheetAutoFilter('A1:J1')
        )]
        sheets = sheets + matrixSheets
        sheets.append(ExcelSheet("エビデンス", evidenceSheetRows))

        return sheets

    @classmethod
    def createTestCaseSheetHeaderCells(cls):
        headerValues = [
            "ID",
            "概要",
            "テスト観点",
            "テストパターン",
            "手順",
            "想定結果",
            "実施結果",
            "実施日",
            "実施者",
            "備考"
        ]

        headerCells = []
        for i, value in enumerate(headerValues):
            line = ExcelSheetCellLine('thin', '000000')
            cellStyle = ExcelSheetCellStyle(
                ExcelSheetCellBorder(line, line, line, line),
                ExcelSheetCellFill('solid', 'c8e6c6'),
                ExcelSheetCellAlignment('top', wrapText = True)
            )
            cell = ExcelSheetCell(value, cellStyle)
            headerCells.append(cell)
        return headerCells

    @classmethod
    def createMergeCell(
        cls,
        value = "",
        isTop = True,
        isBottom = True,
        isRight = True,
        isLeft = True,
        validationData = None,
        fontColor = '000000',
        wrapText = False,
        hyperLink=None
    ):
        line = ExcelSheetCellLine('thin', '000000')
        return ExcelSheetCell(
            value,
            ExcelSheetCellStyle(
                ExcelSheetCellBorder(
                    line if isTop else None,
                    line if isBottom else None,
                    line if isRight else None,
                    line if isLeft else None
                ),
                ExcelSheetCellFill('solid', 'ffffff'),
                ExcelSheetCellAlignment('top', wrapText),
                # 白字はフィルタ用
                ExcelSheetCellFont(fontColor) if isTop else ExcelSheetCellFont('ffffff'),
            ),
            validationData,
            hyperLink
        )

    @classmethod
    def toExcel(cls, integratedTest, integratedTestConfig, prefix=''):
        testBlockName = integratedTest.getName()

        sheets = [
            cls.createStatusSheet()
        ]

        if integratedTest.hasImages():
            images = [ExcelSheetImage(
                image.getPath(),
                ExcelSheetImageSize(image.getWidth(), image.getHeight()),
                index * 30 + 2
            ) for index, image in enumerate(integratedTest.getImages())]

            rows = []
            for index, image in enumerate(integratedTest.getImages()):
                rows.append([ExcelSheetCell(image.getName())])
                for _ in range(29):
                    rows.append([ExcelSheetCell('')])
            sheets.append(ExcelSheet("画面イメージ", rows, images=images))

        sheets.append(cls.createPreparationSheet(integratedTest.getPreparation()))
        if integratedTest.hasTestData():
            sheets.append(cls.createTestDataSheet(integratedTest.getAccounts()))
        sheets = sheets + cls.createTestCaseAndEvidenceSheet(integratedTest, integratedTestConfig)
        sheets.append(cls.createPerspectiveSheet(integratedTestConfig))

        return Excel(
            f"結合テスト仕様書_{prefix}_{testBlockName}.xlsx",
            sheets
        )

    @classmethod
    def getAdjustedColumnWidths(cls, sheetRows):
        maxLenCells =  [max(col, key=lambda x: 1 if x.getValue() == "=ROW()-1" else len(x.getValue())) for col in zip(*sheetRows)]
        return [len(cell.getValue()) * 3 for cell in maxLenCells]
