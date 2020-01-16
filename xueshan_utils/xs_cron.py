# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-16

# cron时间表达式相关操作包

def to_cron(cron_exp):
    '''
    将cron表达式字符串转换成cron字典返回。
    顺序单位：   秒     分     时     日     月     周      年(年一般省略不写)
    :param cron_exp:文本字符串cron表达式，至少有六项，至多有七项
    :return:组装后的dict，可用于定时任务cron表达式。目前设计的主要目的是用于apscheduler包的扩展

    【cron表达式介绍】
    *：触发所有值
    */a：a从最小值开始，触发每个值
    a-b：触发a-b范围内的任何值（必须小于b）
    a-b/c：触发在a-b之间的每个c值
    xth y：第y个工作日中第x天发触发
    last x：在一个月中第x个工作日中的最后一天触发
    last：在月末的最后一天触发
    x,y,z：触发任何匹配的表达式; 可以组合任意数量的任何上述表达式。
    注意：xth y,last x,last这3个是用在day（即日）参数中，其它所有参数都可以使用。
    '''
    values = cron_exp.split()
    if len(values) != 6 and len(values) != 7:
        raise ValueError('Wrong number of fields; got {}, expected 6 or 7'.format(len(values)))
    cron_dict = {}
    cron_dict["second"] = values[0]
    cron_dict["minute"] = values[1]
    cron_dict["hour"] = values[2]
    cron_dict["day"] = values[3]
    cron_dict["month"] = values[4]
    cron_dict["day_of_week"] = values[5]
    if len(values) == 7:
        cron_dict["year"] = values[6]
    return cron_dict

if __name__ == '__main__':
    # 以下是测试代码
    cron_expression = to_cron("*/3 * * * * *")
    print(cron_expression)