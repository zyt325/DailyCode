window.operateEvents = {
    'click .check': function (e, value, row, index) {
        $.get('/employee/', {'action':'check','username': row.username}, function (data) {
            result=data;
            if (result.enabled && result.unlocked){
                alert('帐户'+row.username+'正常')
            }else if(!result.exist){
                alert('帐户'+row.username+'不存在')
            }else if(!result.enabled){
                alert('帐户'+row.username+'被禁用')
            }else if(!result.unlocked){
                alert('帐户'+row.username+'被锁')
            }
        });
        // alert('You click like action, row: ' + JSON.stringify(row.username))
    },
    'click .unlock': function (e, value, row, index) {
        $.get('/employee/', {'action':'unlock','username': row.username}, function (data) {
            result=data;
            if (!result.status){
                alert('帐户'+row.username+'已解锁')
            }else if(!result.exist){
                alert('帐户'+row.username+'不存在')
            }
        });
    },
    'click .enable': function (e, value, row, index) {
        $.get('/employee/', {'action':'enable','username': row.username}, function (data) {
            result=data;
            if (!result.status){
                alert('帐户'+row.username+'已启用')
            }else if(!result.exist){
                alert('帐户'+row.username+'不存在')
            }
        });
    },
    'click .disable': function (e, value, row, index) {
        $.get('/employee/', {'action':'disable','username': row.username}, function (data) {
            result=data;
            if (!result.status){
                alert('帐户'+row.username+'已禁用')
            }else if(!result.exist){
                alert('帐户'+row.username+'不存在')
            }
        });
    }
}

function operateFormatter(value, row, index) {
    return [
        '<a class="check" href="javascript:void(0)" title="Check">',
        '<i class="fa fa-check" aria-hidden="true"></i>',
        '</a>  ',
        '<a class="unlock" href="javascript:void(0)" title="Unlock">',
        '<i class="fa fa-unlock" aria-hidden="true"></i>',
        '</a>',
        '<a class="enable" href="javascript:void(0)" title="Enable">',
        '<i class="fa fa-check-circle" aria-hidden="true"></i>',
        '</a>',
        '<a class="disable" href="javascript:void(0)" title="Disable">',
        '<i class="fa fa-circle" aria-hidden="true"></i>',
        '</a>'
    ].join('')
}

$('#table').bootstrapTable({
    url: '/employees/',
    pagination: true,
    showRefresh: true,
    showColumns: true,
    sortable: true,
    filterControl: true,
    showSearchClearButton: true,
    search: true,
    columns: [{
        field: 'id',
        title: 'ID',
        visible: false,
    }, {
        field: 'category',
        title: 'Category',
        filterControl: 'select'
    }, {
        field: 'status',
        title: 'Status',
        sortable: true,
        filterControl: 'select'
    }, {
        field: 'username',
        title: 'UserName'
    }, {
        field: 'chinese_full_name',
        title: 'Chinese_name'
    }, {
        field: 'english_full_name',
        title: 'English_name'
    }, {
        field: 'gender',
        title: 'gender'
    }, {
        field: 'department_code',
        title: 'Dep',
        sortable: true,
        filterControl: 'select'
    }, {
        field: 'office_code',
        title: 'Office',
        sortable: true,
        filterControl: 'select'
    }, {
        field: 'start_date',
        title: 'Start_date',
        sortable: true,
    }, {
        field: 'employee_start_date',
        title: 'Em_start_date'
    }, {
        field: 'end_date',
        title: 'End_date',
        sortable: true,
    }, {
        field: 'mobile',
        title: 'Mobile'
    }, {
        field: 'disable_account_date',
        title: 'disable_account'
    }, {
        field: 'backup_delete_email_date',
        title: 'Delete_backup_email'
    }, {
        field: 'operate',
        title: 'Item Operate',
        align: 'center',
        clickToSelect: false,
        events: window.operateEvents,
        formatter: operateFormatter
    }]
})
