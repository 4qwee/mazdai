/**
 * Created with PyCharm.
 * User: 4qwee
 * Date: 8/13/12
 * Time: 10:54 PM
 */

myJS = function ()
{
    $("#positions-table tbody tr").live('click', function (e)
    {
        var myTable = $('#positions-table');
        var toolbar = $("div.toolbar");
        var $this = $(this);

        if ($this.find('td').first().hasClass('dataTables_empty'))
            return;

        if ($this.hasClass('row_selected'))
        {
            $this.removeClass('row_selected');

            toolbar.empty();
        }
        else
        {
            myTable.find('tr.row_selected').removeClass('row_selected');
            $this.addClass('row_selected');

            toolbar.empty();

            $sale = $('<input/>').attr('type', 'button').val('Продажа').addClass('myButton');
            $sale.click(function(e)
            {
                var $popup = $('#salesPopup');
                $popup.find('p').first().hide();
                var number = $this.find('td').first().html();
                $popup.find('#id_position_id').val(number);
                $popup.dialog({
                    modal:true,
                    title:'Продажа',
                    show:{effect:'puff', duration:100},
                    hide:{effect:'puff', duration:100}
                });
            });
            toolbar.append($sale);

            $expense = $('<input/>').attr('type', 'button').val('Расход').addClass('myButton');
            toolbar.append($expense);

            $hands = $('<input/>').attr('type', 'button').val('На руки').addClass('myButton');
            toolbar.append($hands);

            $order = $('<input/>').attr('type', 'button').val('Заказ').addClass('myButton');
            toolbar.append($order);

            $(toolbar).buttonset();
        }
    });

    var $sales_link = $('#bottom_links');
    $sales_link.buttonset();
};