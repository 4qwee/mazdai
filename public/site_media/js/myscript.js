/**
 * Created with PyCharm.
 * User: 4qwee
 * Date: 8/13/12
 * Time: 10:54 PM
 */

myJS = function ()
{
    var myTable = $('#positions-table');

    alert($("#positions-table tbody tr").length);

    $("#positions-table tbody tr").click(function (e)
    {
        alert('selected!');

        if ($(this).hasClass('row_selected'))
        {
            $(this).removeClass('row_selected');
        }
        else
        {
            myTable.$('tr.row_selected').removeClass('row_selected');
            $(this).addClass('row_selected');
        }
    });
};