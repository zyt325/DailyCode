// send search=8 to the server.
function queryParams(params) {
    if (!params.hasOwnProperty('direction')) {
        params.direction = 'Forward'
    }
    if ($.session.get('zone_id')) {
        params.zone_id = $.session.get('zone_id')
    }
    if ($.session.get('zone_name')) {
        params.zone_name = $.session.get('zone_name')
    }
    if ($('#fuzzy').hasClass('fa-toggle-on')) {
        params.fuzzy = 'True'
    } else {
        params.fuzzy = 'False'
    }
    return params
}

function init() {
    $.session.clear();
    $('#table_data').bootstrapTable({
        url: '/rr_search/',
        editableEmptytext: "",
        // editableUrl: "/edit/",
        // cache: false,
        pagination: true,
        sidePagination: 'server',
        pageSize: "15",
        pageList: "[10,15,20,50]",
        paginationLoop: true,
        showRefresh: true,
        strictSearch: true,
        sortable: false,
        filterControl: true,
        toobar: '#toolbar',
        search: true,
        showSearchButton: true,
        showSearchClearButton: true,
        idField: 'id',
        selectItemName: "id",
        clickToSelect: true,
        queryParams: queryParams,
        columns: [{
            field: 'state',
            checkbox: true,
        }, {
            field: 'id',
            title: 'ID',
            visible: false,
        }, {
            field: 'name',
            title: 'Name',
            sortable: true,
            filterControl: 'input',
        }, {
            field: 'type',
            title: 'Type',
            sortable: true,
            filterControl: 'select',
            filterStrictSearch: true,
        }, {
            field: 'value',
            title: 'Value',
            sortable: true,
            filterControl: 'input',
        }, {
            field: 'zone',
            title: 'Zone',
            sortable: true,
            // filterControl: 'select',
        }, {
            field: 'disabled_flag',
            title: 'Disabled'
        }, {
            field: 'reversed_flag',
            title: 'Reversed'
        }, {
            field: 'user',
            title: 'User',
            // filterControl: 'select'
        }, {
            field: 'date',
            title: 'Date',
            sortable: true,
        }]
    })
}


function load_rrs(params) {
    $.get('/rr_search/', params, function (data) {
        if (data) {
            $('#table_data').bootstrapTable('load', JSON.parse(data));
        }
        $('#table_data').bootstrapTable('refresh');
    })
}

$(function () {
    $('#sidebar').jstree({
        'core': {
            "animation": 0,
            "check_callback": true,
            // "themes": {"stripes": true},
            'data': {
                'url': '/menu/',
            }
        },
        "plugins": ["wholerow"]
    });
    $('#sidebar').on("changed.jstree", function (e, data) {
        var selected_value = data.selected.toString();
        if (!isNaN(selected_value)) {
            params = {direction: 'Forward', zone_id: selected_value};
            $.session.clear();
            $.session.set('zone_id', selected_value);
            load_rrs(queryParams(params));
        } else {
            params = {direction: 'Forward', zone_name: selected_value};
            $.session.clear();
            $.session.set('zone_name', selected_value);
            load_rrs(queryParams(params));
        }
    });
    init();
    del_rr();
    add_rr();
    edit_rr();
    $(window).resize(function () {
        $('#tableId').bootstrapTable('resetView')
    });
    $('.fixed-table-toolbar').prepend('<div class="columns columns-right btn-group float-right"><button class="btn btn-secondary" type="button" name="Fuzzy"  title="Fuzzy"><i id="fuzzy" class="fa fa-toggle-on"></i> </button></div>');
    $('button[name=Fuzzy]').click(function () {
        $('#fuzzy').toggleClass('fa-toggle-off');
        $('#fuzzy').toggleClass('fa-toggle-on');
        if ($('#fuzzy').hasClass('fa-toggle-on')) {
            params = {fuzzy: 1}
        } else {
            params = {fuzzy: 0}
        }
        load_rrs(queryParams(params));
    })
})


function del_rr() {
    $('#del_rr').click(function () {
        var ids = $.map($('#table_data').bootstrapTable('getSelections'), function (row) {
            return row.id
        });
        if (ids.length == 0) {
            layer.open({
                title: 'Notice',
                content: 'Please select DNS record！'
            })
        }
        $.get('/rr_op/', {'ids': ids,'action':'del'});
        $('#table_data').bootstrapTable('remove', {
            field: 'id',
            values: ids
        });

    })
}

function add_rr() {
    $('#add_rr').click(function () {
        layer.open({
            type: 2,
            title: 'Add dns record',
            content: ['/rr_op/?action=add', 'no'],
            area: ['500px', '400px'],
            cancel: function (index,layero) {
                $('#table_data').bootstrapTable('refresh');
                layer.close(index);
            }
        })
    })
}

function edit_rr() {
    $('#edit_rr').click(function () {
        var ids = $.map($('#table_data').bootstrapTable('getSelections'), function (row) {
            return row.id
        });
        if (ids.length == 1) {
            layer.open({
                type: 2,
                title: 'Edit dns record',
                content: ['/rr_op/?action=edit&id='+ids[0], 'no'],
                area: ['500px', '400px'],
                cancel: function (index,layero) {
                    $('#table_data').bootstrapTable('refresh');
                    layer.close(index);
                }
            })
        }else {
            layer.open({
                title: 'Warn',
                content: 'Please select One DNS record！',
                time: 2000,
            })
        }

    })
}

