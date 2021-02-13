from django.shortcuts import render, redirect, reverse
import pandas as pd
import csv
from validator.utils import validator as vld
from django.http import HttpResponse


# Main Page
def index(request):
    context = {'validation_results':False}
    template='validator/index.html'

    if request.method == 'POST':
        file=request.FILES['file']
    
        
        global df # make df global so I can use in csv_down
        

        df = vld.validate_vat_id_csv(file,0,10000)
 
        context={
                 'count_validated': len(df),
                 'validation_results': df.to_dict('records'),
                 'valid_ids': df[df.Valid == True].to_dict('records'),
                 'invalid_ids': df[df.Valid == False].to_dict('records'),
                 'valid_count': len(df[df.Valid == True].to_dict('records')),
                 'invalid_count': len(df[df.Valid == False].to_dict('records')),
                 'invalid_percent': (len(df[df.Valid == False].to_dict('records'))*100)/len(df)
                 }

        return redirect('/results')

    else:

        return render(request, template, context)


def validation_results(request):
    context = {'validation_results':False}
    template='validator/results.html'

    
 
    context={
            'count_validated': len(df),
            'validation_results': df.to_dict('records'),
            'valid_ids': df[df.Valid == True].to_dict('records'),
            'invalid_ids': df[df.Valid == False].to_dict('records'),
            'valid_count': len(df[df.Valid == True].to_dict('records')),
            'invalid_count': len(df[df.Valid == False].to_dict('records')),
            'invalid_percent': (len(df[df.Valid == False].to_dict('records'))*100)/len(df)
            }


    return render(request, template, context)



def csv_down(request):
    context = {'validation_results':False}
    template='validator/index.html'

    if request.method== 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=validation_results.csv"
        validation_csv = df.to_csv(path_or_buf=response, index=False)
        return response 
    


