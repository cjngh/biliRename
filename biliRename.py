import os
import json
import shutil
import winreg

# author:skybay
# date:2019/04/22
# 公众号:skybay

def getDesktop():
    key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key,'Desktop')[0]

def getSubDirNames(file_dir):
    for root,dirs,files in os.walk(file_dir):
        return dirs


def getSubFileNames(file_dir):
    for root,dirs,files in os.walk(file_dir):
        return files


if __name__=="__main__":
    print("请确保B站缓存数字文件夹保存在桌面“B站缓存”文件夹中！")
    input("若确定视频已保存在桌面“B站缓存”文件夹中，则回车开始重命名！")
    desktop=getDesktop()
    srcFile=desktop+r"\B站缓存"
    dirList=getSubDirNames(srcFile) # 获取数字子文件夹列表（只包含子文件夹）
    for path in dirList:
        dirPath=os.path.join(srcFile,path) # 拼接视频集合数字子文件夹路径
        dirList2 = getSubDirNames(dirPath)  # 获取单集数字子文件夹列表（只包含子文件夹）
        setTitle="" # 集合名
        setTitlePath="" # 集合路径
        for path1 in dirList2:
            dirPath1=os.path.join(dirPath,path1) # 拼接单集数字子文件夹路径
            fileNames=getSubFileNames(dirPath1) # 获取单集数字子文件夹中的文件列表
            for infoFileNames in fileNames: # 获取并暂存标题
                infoFilePath=os.path.join(dirPath1,infoFileNames) # 拼接单集数字子文件夹中文件的路径
                if infoFilePath.endswith("json"):
                    openFile=open(infoFilePath,encoding="UTF-8")
                    info=openFile.read()
                    if not setTitle.strip():
                        setTitle=json.loads(info)["title"] # 集合名
                        setTitlePath=os.path.join(srcFile,setTitle)
                        os.makedirs(setTitlePath)
                    title=json.loads(info)["page_data"]["part"] # 单集名
                    openFile.close()
            dir3Name=getSubDirNames(dirPath1) # 获取第四层文件夹名
            dirPath2=os.path.join(dirPath1,dir3Name[0]) # 拼接视频所在文件夹路径
            files = getSubFileNames(dirPath2)  # 获取视频文件夹中的文件列表
            for VFile in files:
                if VFile.endswith("blv"):
                    oldVFileName=dirPath2+"\\"+VFile
                    newVFileName=os.path.join(dirPath2,title)+'.blv'
                    os.rename(oldVFileName,newVFileName) # 改名
                    shutil.move(newVFileName,setTitlePath) # 移动
    for path in dirList:
        dirPath = os.path.join(srcFile, path)
        shutil.rmtree(dirPath)