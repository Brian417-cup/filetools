import click
import glob
import os
import  os.path
import shutil

@click.group()
def file_op():
    '''
    本文件操作支持通配符
    通配符说明: 1 *.*--全部文件
                2 *.文件后缀统配
                3 文件名统配.*
    :return:
    '''
    click.echo('这是文件操作的库')
    pass


@click.command(name='find')
@click.option('-src',help='目标文件路径')
@click.option('-base',help='是否加入目标文件路径作为基地址，默认为true',default=True,type=bool)
def traversePath(src, base):
    '''
    example: traverse -src=[base root name]/通配符
    找到目标路径下符合条件的文件(支持通配符)
    '''


    traverse_list=glob.glob(src)
    for item in traverse_list:
        if base:
            click.echo(item)
        else:
            click.echo(os.path.basename(item))



@click.command(name='add_tail')
@click.option('-src',help='目标文件路径')
@click.option('-tail',help='尾部加入的名称')
@click.option('-base',help='是否加入目标文件路径作为基地址，默认为true',default=True,type=bool)
def add_tail(src,tail,base):
    '''
    example: add_tail -src=[base root name]/通配符 -tail=尾部加入的名称(不包含后缀)
    找到目标路径下符合条件的文件(支持通配符)
    通配符说明: 1 *.*--全部文件
                2 *.文件后缀统配
                3 文件名统配.*
    '''

    targetSufix= src[src.rfind('.'):len(src)]
    for item in glob.glob(src):
        beforeSuffix=item[0:item.rfind('.')]
        # print(beforeSuffix)
        targetName=os.path.join(os.path.dirname(item),beforeSuffix+tail)
        os.rename(item,targetName)
        if base:
            click.echo(targetName)
        else:
            click.echo(os.path.basename(targetName))


@click.command(name='add_head')
@click.option('-src',help='目标文件路径')
@click.option('-head',help='首部加入的名称')
@click.option('-base',help='是否加入目标文件路径作为基地址，默认为true',default=True,type=bool)
def add_head(src,head,base):
    '''
    example: add_tail -src=[base root name]/通配符 -head=首部加入的名称
    找到目标路径下符合条件的文件(支持通配符)
    通配符说明: 1 *.*--全部文件
                2 *.文件后缀统配
                3 文件名统配.*
    '''

    targetSufix= src[src.rfind('.'):len(src)]
    for item in glob.glob(src):
        beforeSuffix= os.path.basename(item[0:item.rfind('.')])
        # print(beforeSuffix)
        targetName=os.path.join(os.path.dirname(item),head+beforeSuffix+targetSufix)
        os.rename(item,targetName)
        if base:
            click.echo(targetName)
        else:
            click.echo(os.path.basename(targetName))


@click.command('copy')
@click.option('-src',help='源路径文件批')
@click.option('-dst',help='目标文件夹')
def copy(src,dst):
    '''
    example: copy -src=f:/ttt/*.txt -dst=f:/ttt/test
    :param src:
    :param dst:
    :return:
    '''
    for item in glob.glob(src):
        file_name=os.path.basename(item)
        src_path=os.path.join(os.path.dirname(src),file_name)
        dst_path=os.path.join(dst,file_name)
        shutil.copyfile(src_path,dst_path)
        click.echo('target: {0}'.format(dst_path))


@click.command('copydir')
@click.option('-src',help='源路径文件夹')
@click.option('-dst',help='目标文件夹')
def copydir(src,dst):
    '''
    example: copy  copydir -src=f:/ttt/ -dst=f:/ttt5
    :param src:
    :param dst:
    :return:
    '''
    # if os.path.exists(dst):
    #     click.echo('目标路径已存在')
    #     return

    if os.path.exists(dst):
        click.echo('文件夹已存在，是否选择删除原文件夹，再创建同名文件夹  Y/N?')
        choose=input()
        if choose.lower()=='y':
            shutil.rmtree(dst)
        else:
            click.echo('文件创建失败')
            return

    shutil.copytree(src,dst)




@click.command('move')
@click.option('-src',help='源路径文件批，会移动源路径机器下方所有的文件')
@click.option('-dst',help='目标文件夹')
def move(src,dst):
    '''
    example: move -src=f:/ttt/*.txt -dst=f:/ttt/test/
    :param src:
    :param dst:
    :return:
    '''
    for item in glob.glob(src):
        file_name=os.path.basename(item)
        target_name=os.path.join(dst,file_name)
        shutil.move(item,target_name)
        click.echo(target_name)


@click.command('movedir')
@click.option('-src',help='源路径文件批，会移动源路径机器下方所有的文件')
@click.option('-dst',help='目标文件夹')
def movedir(src,dst):
    '''
      example: movedir -src=f:/ttt/目标文件夹名称 -dst=f:/ttt/test/
      :param src:
      :param dst:
      :return:
      '''
    for item in glob.glob(src):
        dir_name = os.path.basename(item)
        target_name = os.path.join(dst, dir_name)
        shutil.move(item, target_name)
        click.echo(target_name)


@click.command('delete')
@click.option('-src',help='源路径文件批')
def delete(src):
    '''
    对文件(非文件夹的删除)
    example: delete -src=f:/ttt/*.txt
    :param src:
    :return:
    '''
    for item in glob.glob(src):
        os.remove(item)
        click.echo(item)


@click.command('deletedir')
@click.option('-src',help='源路径文件夹批')
def deletedir(src):
    '''
    对文件夹及其子文件的删除
    example: delete -src=f:/ttt/test/
    :param src:
    :return:
    '''
    for item in glob.glob(src):
        shutil.rmtree(item)
        click.echo(item)



if __name__ == '__main__':
    file_op.add_command(traversePath)

    file_op.add_command(add_tail)
    file_op.add_command(add_head)

    file_op.add_command(copy)
    file_op.add_command(copydir)

    file_op.add_command(move)
    file_op.add_command(movedir)

    file_op.add_command(delete)
    file_op.add_command(deletedir)
    file_op()