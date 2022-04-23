import click
import glob
import os
import  os.path

@click.group()
def file_op():
    print('这是文件操作的库')
    pass


@click.command(name='find')
@click.option('-src',help='目标文件路径')
@click.option('-base',help='是否加入目标文件路径作为基地址，默认为true',default=True,type=bool)
def traversePath(src, base):
    '''
    example: traverse -src=[base root name]/通配符
    找到目标路径下符合条件的文件(支持通配符)
    通配符说明: 1 *.*--全部文件
                2 *.文件后缀统配
                3 文件名统配.*
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
    e    example: add_tail -src=[base root name]/通配符 -head=首部加入的名称
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



if __name__ == '__main__':
    file_op.add_command(traversePath)
    file_op.add_command(add_tail)
    file_op.add_command(add_head)
    file_op()

