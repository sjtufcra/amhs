import tc_class_sets
import tc_in
import tc_assign
import tc_out
import warnings


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    d = tc_class_sets.Dataset()
    if d.pattern == 1:
        # reading
        print('Begin loading data')
        d = tc_in.generating(d)
        print('Finish loading data')
        # path allocation
        d = tc_assign.task_assign_new(d)
    elif d.pattern == 0:
        d = tc_in.generating(d)
        print('Finish loading data')
        # path allocation
        d = tc_assign.task_assign_new(d)
    # write to database
    tc_out.output_close_connection(d)
