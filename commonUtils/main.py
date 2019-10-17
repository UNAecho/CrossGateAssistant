import time
import win32api
import operation
import windowUtils
import inputUtils
from BIUtils import contentUtils
import readContentOfScreen

time.sleep(0.5)
# 批量文件内容处理
# contentUtils.batch_modify_file_contents(r'C:\EI_InternalAudit\DDL\internalaudit_insight_12938', 'INT')
# 用剪贴板输入内容
# inputUtils.input_with_clipboard(r'C:\EI_InternalAudit\DDL\internalaudit_insight_12938\perprod')
# 批量替换文字
# contentUtils.replace_content_in_dir(r'C:\EI_InternalAudit\DDL\internalaudit_insight_12938', 'internalaudit_preprod_insight_12938', 'internalaudit_insight_12938')
# 批量读取文件到单一文件中
# contentUtils.read_content_to_single_file(r"C:\Users\andi.you\Desktop\rtp")
# operation.mouse_click_cv(719, 362)
print(win32api.GetCursorPos())
# a = readContentOfScreen.read_number_of_screen("temp.png",1375,311,30,20);print(a)
