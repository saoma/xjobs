# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.1
# update_date：2020-01-30

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
    xth y：顺数第x个星期y触发，如2nd sun意思为第二个星期天触发【请务必理解后才使用】
    last x：在一个月的最后一个星期x触发，如last fri意思为最后一个星期五【请务必理解后才使用】
    last：在月末的最后一天触发
    x,y,z：触发任何匹配的表达式; 可以组合任意数量的任何上述表达式。
    注意：xth y,last x,last这3个是用在day（即日）参数中，其它所有参数都可以使用。
    【补充很多网上没有的】：
    星期几有啥选项？
    WEEKDAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    月份有啥选项？
    MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    排序，第几个有啥选项？
    options = ['1st', '2nd', '3rd', '4th', '5th', 'last']

    【注意】如果使用了xth y,last x等这几个表示day，中间有空格的，请在表达式中，使用单引号或双引号引起来，否则不生效！！
    请勿在除了day以外的表达式部分中使用这几项，否则会出错！
    '''
    def __check_arg_len(arg_len):
        # 检查参数个数
        if arg_len not in [6, 7]:
            raise ValueError('Wrong number of fields; got {}, expected 6 or 7'.format(arg_len))

    cron_dict = {}
    if cron_exp.find("\"") > -1 or cron_exp.find("'") > -1:
        # 处理day部分中有引号的情况
        if cron_exp.find("\"") > -1:
            all_parts = cron_exp.split("\"")
        elif cron_exp.find("'") > -1:
            all_parts = cron_exp.split("'")
        day_part = all_parts[1]
        part1 = all_parts[0].split()
        part2 = all_parts[2].split()
        part_len = len(part1) + 1 + len(part2)
        __check_arg_len(part_len)
        cron_dict["second"] = part1[0]
        cron_dict["minute"] = part1[1]
        cron_dict["hour"] = part1[2]
        cron_dict["day"] = day_part
        cron_dict["month"] = part2[0]
        cron_dict["day_of_week"] = part2[1]
        if part_len == 7:
            cron_dict["year"] = part2[2]
    else:
        # 普通情况
        values = cron_exp.split()
        part_len = len(values)
        __check_arg_len(part_len)
        cron_dict["second"] = values[0]
        cron_dict["minute"] = values[1]
        cron_dict["hour"] = values[2]
        cron_dict["day"] = values[3]
        cron_dict["month"] = values[4]
        cron_dict["day_of_week"] = values[5]
        if part_len == 7:
            cron_dict["year"] = values[6]
    return cron_dict

if __name__ == '__main__':
    # 以下是测试代码
    cron_expression = to_cron("*/3 * * * * *")
    print(cron_expression)

    cron_expression = to_cron("0 0 5 'last fri' * *")
    print(cron_expression)