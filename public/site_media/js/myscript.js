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


        if ($(this).hasClass('row_selected'))
        {
            $(this).removeClass('row_selected');

            toolbar.empty();
        }
        else
        {
            myTable.find('tr.row_selected').removeClass('row_selected');
            $(this).addClass('row_selected');

            toolbar.empty();

            $sale = $('<input/>').attr('type', 'button').val('Продажа').addClass('myButton');
            $sale.click(function(e)
            {
                $('#salesPopup').dialog({modal:true});
            });
            toolbar.append($sale);

            $expense = $('<input/>').attr('type', 'button').val('Расход').addClass('myButton');
            toolbar.append($expense);

            $hands = $('<input/>').attr('type', 'button').val('На руки').addClass('myButton');
            toolbar.append($hands);

            $order = $('<input/>').attr('type', 'button').val('Заказ').addClass('myButton');
            toolbar.append($order);
        }
    });
};