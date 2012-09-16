/**
 * Created with PyCharm.
 * User: 4qwee
 * Date: 8/13/12
 * Time: 10:54 PM
 */

myJS = function ()
{
    function createPopup($sales_popup, title)
    {
        $sales_popup.dialog({
            modal:true,
            title:title,
            show:{effect:'puff', duration:100},
            hide:{effect:'puff', duration:100},
            autoOpen:false
        });
    }

    function createActionButton($row, $popup, label)
    {
        var $sale = $('<input/>').attr('type', 'button').val(label).addClass('myButton');
        $sale.click(function ()
        {
            var number = $row.find('td').first().html();
            $popup.find('#id_position_id').val(number);
            $popup.dialog('open');
        });
        return $sale;
    }

    function createActionBar($row, $toolbar)
    {
        $toolbar.append(createActionButton($row, $sales_popup, 'Продажа'));
        $toolbar.append(createActionButton($row, $move_popup, 'Расход'));
        $toolbar.append(createActionButton($row, $credit_popup, 'На руки'));
        $toolbar.append(createActionButton($row, $order_popup, 'Заказ руки'));

        $toolbar.buttonset();
    }

    function createSubmitHandler($table, $popup, $toolbar)
    {
        return function (e)
        {
            e.preventDefault();

            var $form = $popup.find('form');
            var $errors = $popup.find('.errors');

            $form.find('.submit_button').attr('disabled', 'disabled');
            $form.find('.progress_image').show();

            $.ajax({
                url:$form.attr('action'),
                type:$form.attr('method'),
                data:$form.serialize(),
                dataType:'json',
                success:function (json)
                {
                    $form.find('img.progress_image').hide();
                    $popup.find('.submit_button').removeAttr('disabled');
                    if (json.success)
                    {
                        $popup.dialog('close');
                        $toolbar.empty();
                        $table.dataTable().fnClearTable();
                        $table.dataTable().fnDraw();
                    }
                    else
                        $errors.noty({text:json.html, type:'error'});
                },
                error:function (xhr, ajaxOptions, thrownError)
                {
                    $form.find('img.progress_image').hide();
                    $errors.noty({text:thrownError, type:'error'});
                }
            })
        };
    }

    var $myTable = $('#positions-table');
    var $toolbar = $("div.toolbar");
    var $sales_popup = $('#salesPopup');

    createPopup($sales_popup, 'Продажа');

    var $move_popup = $('#movePopup');

    createPopup($move_popup, 'Расход');

    var $credit_popup = $('#creditPopup');

    createPopup($credit_popup, 'На руки');

    var $order_popup = $('#orderPopup');

    createPopup($order_popup, 'Заказ');

    $('.popup').each(function(index)
    {
        var $popup = $(this);

        $popup.find('form').submit(createSubmitHandler($myTable, $popup, $toolbar));
    });

    $('#bottom_links').buttonset();

    $("#positions-table").find("tbody tr").live('click', function (e)
    {
        var $this = $(this);

        if ($this.find('td').first().hasClass('dataTables_empty')) //don't select header
            return;

        if ($this.hasClass('row_selected'))
        {
            $this.removeClass('row_selected');
            $toolbar.empty();
        }
        else
        {
            $myTable.find('tr.row_selected').removeClass('row_selected');
            $this.addClass('row_selected');
            $toolbar.empty();

            createActionBar($this, $toolbar);
        }
    });
};