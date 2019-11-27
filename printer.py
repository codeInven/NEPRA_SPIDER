import win32print, win32ui, win32gui
import win32con, pywintypes

def create_printer(printer_name='PSPrinter'):
    printer_info_2 = {
        'pPrinterName': printer_name,
        'pDevMode': pywintypes.DEVMODEType(),        
        'pDriverName': 'MS Publisher Imagesetter',
        'pPortName': 'FILE:',
        'pPrintProcessor': 'WinPrint',
        'Attributes': 0,
        'AveragePPM': 0,
        'cJobs': 0,
        'DefaultPriority': 0,
        'Priority': 0,
        'StartTime': 0,
        'Status': 0,
        'UntilTime': 0,
        'pComment': '',
        'pLocation': '',
        'pDatatype': None,
        'pParameters': None,
        'pSecurityDescriptor': None,
        'pSepFile': None,
        'pServerName': None,
        'pShareName': None}

    h_printer = win32print.AddPrinter(None, 2, printer_info_2)
    return h_printer


def test_raw(printer='MyPSPrinter',
             filename=r'G:/test.txt',
             text=None):
    '''send plain text to a file'''
    if text is None:
        text_data = "This is a test. This is only a test."
    else:
        text_data = text
    job_info = ("Raw File Print", filename, 'RAW')
    h_printer = win32print.OpenPrinter(printer)
    try:
        h_job = win32print.StartDocPrinter(h_printer, 1, job_info)
        try:
            win32print.StartPagePrinter(h_printer)
            win32print.WritePrinter(h_printer, text_data.encode())
            win32print.EndPagePrinter(h_printer)
        finally:
            win32print.EndDocPrinter(h_printer)
    finally:
        win32print.ClosePrinter(h_printer)


def test_ps(printer='MyPSPrinter',
            filename=r'G:/test.ps',
            margin=(0.25,1.5,0.25,1.0),
            font_size=24,
            text=None):
    '''render postscript text and graphics to a file'''
    if text is None:
        text_data = "This is a test.\nThis is only a test."
    else:
        text_data = (text.encode())

    # Get the printer's DEVMODE structure
    h_printer = win32print.OpenPrinter(printer)
    devmode = win32print.GetPrinter(h_printer, 2)['pDevMode']
    win32print.ClosePrinter(h_printer)

    # set up the device context
    # see MSDN: ff552837, aa452943, dd319099, dd145045
    devmode.FormName = 'Letter'  # or 'A4'
    devmode.PaperSize = win32con.DMPAPER_LETTER  # or DMPAPER_A4
    devmode.Orientation = win32con.DMORIENT_PORTRAIT 
    devmode.PrintQuality = win32con.DMRES_HIGH
    devmode.Color = win32con.DMCOLOR_MONOCHROME
    devmode.TTOption = win32con.DMTT_SUBDEV
    devmode.Scale = 100
    devmode.Fields |= (win32con.DM_FORMNAME | 
                       win32con.DM_PAPERSIZE | 
                       win32con.DM_ORIENTATION | 
                       win32con.DM_PRINTQUALITY | 
                       win32con.DM_COLOR | 
                       win32con.DM_TTOPTION | 
                       win32con.DM_SCALE)    
    h_dc = win32gui.CreateDC('WINSPOOL', printer, devmode)
    dc = win32ui.CreateDCFromHandle(h_dc)
    dc.SetMapMode(win32con.MM_TWIPS) # or MM_HIMETRIC (0.01 mm)

    # begin writing the document
    dc.StartDoc('Postscript File Print', filename)
    dc.StartPage()

    # we need a pen and a font
    scale = 20  # 72 pt/inch * 20 twip/pt = 1440
    inch = 72*scale
    pen = win32ui.CreatePen(win32con.PS_SOLID,
                            scale, # 1 pt
                            0)     # black
    dc.SelectObject(pen)
    font = win32ui.CreateFont({
        'name': 'Times New Roman',
        'height': font_size * scale,
        'weight': win32con.FW_NORMAL})
    dc.SelectObject(font)

    # output the text
    x = int(margin[0] * inch)
    y = -int(margin[1] * inch)
    width = int((8.5 - margin[0] - margin[2]) * inch)
    height = int((11.0 - margin[1] - margin[3]) * inch)
    rect = (x, y, x + width, y - height)
    dc.DrawText(text_data, rect, win32con.DT_LEFT)
    
    if text is None:
        # draw 8 steps starting at x = 0.25", y = 3"
        width = inch
        height = inch
        for n in range(8):
            x = n * width + 18*scale
            y = -n * height - 3*inch
            dc.MoveTo((x, y))
            dc.LineTo((x + width, y))
            dc.MoveTo((x + width, y))
            dc.LineTo((x + width, y - height))

    dc.EndPage()
    dc.EndDoc()
test_ps()
#end