from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.http import HttpResponseRedirect

def home(request):
	# pk_354f8d90312643a68a15ffc5aca3df8f
	# pk_062031d20883444f9ea74e2610fe2011
	# api_request=requests.get("https://cloud.iexapis.com/stable/stock/appl/quote?token=pk_354f8d90312643a68a15ffc5aca3df8f")

	import requests
	import json
	if request.method == 'POST':
		ticker=request.POST['ticker']
		api_request=requests.get ("https://sandbox.iexapis.com/stable/stock/"+ ticker+"/quote?token=Tsk_4581b6ee02ba472d8f06cde50ba6f4c6")

		try:
			api=json.loads(api_request.content)

		except Exception as e:
			api="Error..."

		return render(request,'home.html',{'api':api})
	else:
		return render(request,'home.html',{'ticker':"Plz try again"})

def about(request):
	
	return render(request,'about.html',{})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form=StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ("STock Has Been Added"))
			return redirect ('add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request=requests.get ("https://sandbox.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=Tsk_4581b6ee02ba472d8f06cde50ba6f4c6")
			try:
				api=json.loads(api_request.content)
				output.append(api)

			except Exception as e:
				api="Error..."

		return render(request,'add_stock.html',{'ticker': ticker , 'output':output})

def delete(request, stock_id):
	
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("STock Has Been Deleted"))
	return redirect ('delete_stock')

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request,'delete_stock.html',{'ticker':ticker})

