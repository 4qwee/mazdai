from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

def get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath, *args):
    #Safety measure. If someone messes with iDisplayLength manually, we clip it to
    #the max value of 100.
    if not 'iDisplayLength' in request.GET or not request.GET['iDisplayLength']:
        iDisplayLength = 10 # default value
    else:
        iDisplayLength = min(int(request.GET['iDisplayLength']), 100)

    if not 'iDisplayStart' in request.GET or not request.GET['iDisplayStart']:
        startRecord = 0 #default value
    else:
        startRecord = int(request.GET['iDisplayStart'])
    endRecord = startRecord + iDisplayLength

    #apply ordering 
    if not 'iSortingCols' in request.GET or not request.GET['iSortingCols']:
        iSortingCols = 0 #default value
    else:
        iSortingCols = int(request.GET['iSortingCols'])
    asortingCols = []

    if iSortingCols > 0:
        for sortedColIndex in range(0, iSortingCols):
            sortedColumnIndex = int(request.GET['iSortCol_' + str(sortedColIndex)])
            sortedColName = columnIndexNameMap[sortedColumnIndex]

            try:
                sortingDirection = request.GET['sSortDir_' + str(sortedColIndex)]
                if sortingDirection == 'desc':
                    sortedColName = '-' + sortedColName
            except MultiValueDictKeyError:
                pass

            asortingCols.append(sortedColName)

        querySet = querySet.order_by(*asortingCols)

    #apply filtering by value sent by user
    if not 'sSearch' in request.GET or not request.GET['sSearch']:
        customSearch = '' #default value
    else:
        customSearch = str(request.GET['sSearch'])
    if customSearch != '':
        outputQ = None
        first = True
        for searchableColumn in searchableColumns:
            kwargz = {searchableColumn + "__icontains": customSearch}
            q = Q(**kwargz)
            if (first):
                first = False
                outputQ = q
            else:
                outputQ |= q

        querySet = querySet.filter(outputQ)

    #count how many records match the final criteria
    iTotalRecords = iTotalDisplayRecords = querySet.count()

    #get the slice
    if iDisplayLength > 0:
        querySet = querySet[startRecord:endRecord]

    #prepare the JSON with the response
    if not 'sEcho' in request.GET or not request.GET['sEcho']:
        sEcho = '0' #default value
    else:
        sEcho = request.GET['sEcho'] #this is required by datatables 
    jstonString = render_to_string(jsonTemplatePath, locals())

    return HttpResponse(jstonString, mimetype="application/javascript")