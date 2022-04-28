import os
import glob
import shutil
import click
import zipfile


@click.group()
def zip_file_op():
    click.echo('这是关于ZIP操作的相关库')
    pass


@click.command('findzip')
@click.option('-src',help='目标ZIP文件路径')
@click.option('-base',help='是否加入目标文件路径作为基地址，默认为true',default=True,type=bool)
@click.option('-export',help='确定是否要外输入文件，默认不输出',default='',type=str)
def traverseZIPDirectory(src,base,export):
    if os.path.exists(src)==False:
        click.echo('目标压缩包不存在')
        return
    zip=zipfile.ZipFile(src)

    if len(export)==0:
        for item in zip.namelist():
            temp = os.path.join(src, item)
            if base:
                click.echo(temp)
            else:
                click.echo(item)
    else:
        if os.path.exists(export):
            click.echo('文件夹已存在，是否选择删除原文件夹，再创建同名文件夹  Y/N?')
            choose = input()
            if choose.lower() == 'y':
                os.remove(export)
            else:
                click.echo('无法保存结果')
                return

        export_file=open(export,'w')
        for item in zip.namelist():
            temp = os.path.join(src, item)
            if base:
                export.writelines(temp+'\n')
            else:
                export_file.writelines(item+'\n')

        click.echo('结果已保存至: '+export)
    zip.close()



@click.command('package')
@click.option('-src',help='待打包的源文件夹')
@click.option('-dst',help='保存的路径,包含后缀，目前只支持.zip和.tar')
def package(src,dst):
    '''
    example: package -src=f:/ttt2  -dst=f:/ttt2.zip  默认会将ttt2下的所有文件都打包到ttt2.zip中
    :param src:
    :param dst:
    :return:
    '''
    file_name=os.path.basename(dst)
    dir_name=os.path.dirname(dst)
    file_base_name=file_name[:file_name.rfind('.')]
    suffix=file_name[file_name.rfind('.')+1:]

    if os.path.exists(dst):
        click.echo('目标压缩包已存在，是否选择覆盖原压缩包  Y/N')
        choose=input()
        if choose.lower()=='y':
            shutil.make_archive(os.path.join(dir_name, file_base_name), suffix, src)
            click.echo('压缩包已成功保存至: ' + dst)
        else:
            click.echo('打包失败')


@click.command('unpackage')
@click.option('-src',help='源压缩包')
@click.option('-dst',help='目标保存路径')
def unpackage(src,dst):
    '''
    example: unpackage -src=f:/ttt2.zip  -dst=f:/test  把ttt2.zip下的所有内容都解压到test中，如果路径不存在会自动创建
    :param src:
    :param dst:
    :return:
    '''
    if os.path.exists(src)==False:
        click.echo('源压缩包不存在')
        return
    else:
        if os.path.exists(dst):
            click.echo('文件夹已存在，是否选择删除原文件夹，再创建同名文件夹,否则覆盖原文件将会造成数据丢失  Y/N?')
            choose = input()
            if choose.lower() == 'y':
                shutil.rmtree(dst)
                click.echo('删除原文件成功')
            else:
                click.echo('选择覆盖原数据')

        shutil.unpack_archive(filename=src,extract_dir=dst)
        click.echo('已成功解压至: '+dst+' 文件夹中')


if __name__ == '__main__':
    zip_file_op.add_command(traverseZIPDirectory)
    zip_file_op.add_command(package)
    zip_file_op.add_command(unpackage)

    zip_file_op()