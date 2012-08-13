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

        if ($(this).hasClass('row_selected'))
        {
            $(this).removeClass('row_selected');
        }
        else
        {
            myTable.find('.row_selected').removeClass('row_selected');
            $(this).addClass('row_selected');
        }
    });
};