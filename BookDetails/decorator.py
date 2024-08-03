# from django.shortcuts import redirect

# def login_required(function):
# 	def wraper(request, *args, **kwargs):
# 		if 'user' not in request.session.keys():
# 			return redirect("login")
# 		else:
# 			return function(request, *args, **kwargs)
        
# 	wraper.__doc__=function.__doc__
# 	wraper.__name__=function.__name__
# 	return wraper