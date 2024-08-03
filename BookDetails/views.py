from django.shortcuts import render,redirect
import sweetify
from .models import BedField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from home.models import StayPics
from BookDetails.forms import BookingForm,BedFieldForm
from BookDetails.models import BedField,BookData
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.

def bookField(req):
    pass

@login_required(login_url='login')
def booking(req, id, year=None, month=None, *args, **kwargs):
    book = StayPics.objects.get(id=id)
    bed_types = BedField.objects.all()
    form = BookingForm()
    bedtype = None 
    bookeddata_ = None
    discount = 0
    
    if req.method == 'POST':
        form = BookingForm(req.POST)
        if form.is_valid(): 
            checkin = form.cleaned_data['checkin']
            checkout = form.cleaned_data['checkout']
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            bedtype = form.cleaned_data['bedtype']

            if adults > 2:
                extra_bed_price = 5000 
                extra_beds = adults - 2
                total_extra_bed_cost = extra_beds * extra_bed_price
                bedtype.price += total_extra_bed_cost

                if adults > 3:
                    messages.warning(req, 'Please book another room for more than 4 adults.')
                    return render(req, "booking/booking.html", {'form': form, 'book': book, 'year': year, 'month': month})

            if children > 2:
                extra_bed_price = 5000 
                extra_beds = children - 2
                total_extra_bed_cost = extra_beds * extra_bed_price
                bedtype.price += total_extra_bed_cost

                if children > 3:
                    messages.warning(req, 'Please book another room for more than 3 children.')
                    return render(req, "booking/booking.html", {'form': form, 'book': book, 'year': year, 'month': month})

            num_days = (checkout - checkin).days
   
            existing_reservation = BookData.objects.filter(
                checkin__lt=checkout,
                checkout__gt=checkin,
                stay=book
            ).exists()

            if existing_reservation:
                messages.warning(req, 'Room has already been reserved')
                return render(req, "booking/booking.html", {'form': form, 'book': book, 'year': year, 'month': month})

            if num_days >= 3:
                discount = 0.10
                discounted_price = bedtype.price * (1 - discount)
            else:
                discounted_price = bedtype.price  * num_days

            bookeddata_ = BookData.objects.create(
                stay=book,
                checkin=checkin,
                checkout=checkout,
                adults=adults,
                children=children,
                bedtype=bedtype,
                customer=req.user,
                discounted_price=discounted_price
            )


            messages.success(req, 'Booking completed successfully.')
            return redirect('booking_list', id=bookeddata_.id, year=year, month=month)
    context = {
        'id': id,
        'book': book,
        'form': form,
        'year': year,
        'month': month,
        'bed_types': bed_types,
        "bookeddata_": bookeddata_,
        'discount': discount
    }

    return render(req, 'booking/booking.html', context)

@login_required(login_url='login')
def booking_list(request,id,year = None,month = None):
    print(request.user)
    bookings = BookData.objects.get(id=id)
    host = request.get_host()
    bookings_with_paypal = []
    print(bookings)
    if bookings:
        price = bookings.discounted_price if bookings.discounted_price else bookings.bedtype.price
        paypal_payment = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'item_name': bookings.stay.room,
            'amount': price,
            # 'amount': booking.bedtype.price,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('paysuccess', kwargs={'id': id})}",
            'cancel_url': f"http://{host}{reverse('payfailed', kwargs={'id':id})}",
        }
        paypal_form = PayPalPaymentsForm(initial=paypal_payment)
        bookings_with_paypal.append((bookings, paypal_form))

    context = {
        'bookings_with_paypal': bookings_with_paypal,
        'id': id,
        'year': year,
        'month': month,
    }
    return render(request, 'booking/booking_list.html', context)


@login_required(login_url='login')
def cancel_booking(request, id,year = None,month = None):
    booking = BookData.objects.get(id=id)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('stay')

    return render(request, 'booking/booking_list.html', {'booking': booking})


@login_required(login_url='login')
def payment_success(request, id):
    token = request.GET.get('PayerID')
    print(token,'kkkkkk')
    if token:
            booked_one = BookData.objects.get(customer__email=request.user.email, id=id)
            subject = "Booking Confirmation"
            message = f"""Dear {request.user.username},
            Your booking for {booked_one.stay.room} from {booked_one.checkin} to {booked_one.checkout} has been confirmed.
            Thank you for booking with us!"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'Payment successful and confirmation email sent.')
            print(token,'ffffffffff')
            return redirect('home')
    else:
        return redirect('payfailed',id)
def payment_failed(request, id):
    return render(request, 'payment/payment_failed.html', {'id': id})
    
    
