from .models import Party, PaymentSent
from django.http import HttpResponse
import openpyxl
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from . import models

# Create your views here.


def is_valid_mobile_number(number):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, number)


def is_valid_gst_number(gstin):
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return re.match(pattern, gstin)


def home(req):
    if 'user_login_id' in req.session:
        # total trips
        total_trips = len(models.Booking.objects.all())

        # active customer
        active_customer = len(models.Party.objects.all())

        object = {'total_trips':total_trips, 'active_customer':active_customer}
        return render(req, 'index.html', object)
    else:
        return redirect('/login/')

################################################################################################################################################################
# Register


def register(req):
    return render(req, 'register.html')


def is_valid_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$&])[A-Za-z\d@#$&]{8,16}$'
    return re.match(pattern, password)


def save_user(req):
    if req.method == 'POST':
        data = req.POST

        # Password match check
        if data['user_password'] != data['user_confirm_password']:
            messages.error(req, "Passwords do not match.")
            return render(req, 'register.html')

        # Password strength check
        if not is_valid_password(data['user_password']):
            messages.error(
                req, "Password must be 8–16 chars, include uppercase, lowercase, digit & one of @#$&.")
            return render(req, 'register.html')

        # Email uniqueness check
        if models.User.objects.filter(user_email=data['user_email']).exists():
            messages.error(req, "Email already registered.")
            return render(req, 'register.html')

        # Save user
        user = models.User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_mobile=data['user_mobile'],
            user_password=make_password(data['user_password'])
        )
        user.save()
        messages.success(req, "Account created successfully!")
        return redirect('/login/')


################################################################################################################################################################
# Login


def login(req):
    return render(req, 'login.html')


def user_login(req):
    if req.method != 'POST':
        return render(req, 'login.html')

    try:
        user = models.User.objects.get(user_email=req.POST['user_email'])
    except models.User.DoesNotExist:
        messages.error(req, 'Invalid Email')
        return render(req, 'login.html')

    if not check_password(req.POST['user_password'], user.user_password):
        messages.error(req, 'Invalid Password')
        return render(req, 'login.html')

    req.session['user_login_id'] = user.id
    messages.success(req, 'Login successful!')
    return redirect('/')


def logout(req):
    req.session.flush()
    return redirect('/login/')


################################################################################################################################################################
# Party
def party(req):
    if 'user_login_id' in req.session:
        # Object Bhejna Hai
        partys = models.Party.objects.all()
        obj = {'partys': partys}
        return render(req, 'party.html', obj)
    else:
        return redirect('/login/')


def save_party(req):
    mobile = req.POST['party_mobile']

    if not is_valid_mobile_number(mobile):
        messages.error(req, f"Invalid Mobile Number Format: {mobile}")
        return redirect('/party/')

    gst_number = req.POST['party_gst_number']

    if not is_valid_gst_number(gst_number):
        messages.error(req, f"Invalid GST Number Format: {gst_number}")
        return redirect('/party/')

    party = models.Party(
        party_name=req.POST['party_name'],
        party_mobile=req.POST['party_mobile'],
        party_email=req.POST['party_email'],
        party_address=req.POST['party_address'],
        party_city=req.POST['party_city'],
        party_gst_number=req.POST['party_gst_number'],
        party_pending_amt=req.POST['party_pending_amt']
    )
    party.save()
    return redirect('/party/')


def show_party(req):
    if 'user_login_id' in req.session:
        partys = models.Party.objects.all()
        return render(req,'show_party.html',{'partys':partys})
    else:
        return redirect('/login/')


def edit_party(req):
    if 'user_login_id' in req.session:
        # Object Bhejna Hai
        party_id = req.GET['id']
        party = models.Party.objects.get(id=party_id)
        obj = {'party': party}
        return render(req, 'edit_party.html', obj)
    else:
        return redirect('/login/')


def save_edited_party(req):
    mobile = req.POST['party_mobile']

    if not is_valid_mobile_number(mobile):
        messages.error(req, f"Invalid Mobile Number Format: {mobile}")
        return redirect('/party/')

    gst_number = req.POST['party_gst_number']

    if not is_valid_gst_number(gst_number):
        messages.error(req, f"Invalid GST Number Format: {gst_number}")
        return redirect('/party/')

    party_id = req.POST['party_id']
    party = models.Party.objects.get(id=party_id)
    party.party_name = req.POST['party_name']
    party.party_mobile = req.POST['party_mobile']
    party.party_email = req.POST['party_email']
    party.party_address = req.POST['party_address']
    party.party_city = req.POST['party_city']
    party.party_gst_number = req.POST['party_gst_number']
    party.party_pending_amt = req.POST['party_pending_amt']
    party.save()
    return redirect('/party/')


def delete_party(req):
    if 'user_login_id' in req.session:
        models.Party.objects.get(id=req.GET['id']).delete()
        return redirect('/party/')
    else:
        return redirect('/login/')


# ##############################################################################################################################################################
# Owner


def owner(req):
    if 'user_login_id' in req.session:
        # Object Bhejna Hai
        owners = models.Owner.objects.all()
        obj = {'owners': owners}

        return render(req, 'owner.html', obj)
    else:
        return redirect('/login/')


def save_owner(req):
    mobile = req.POST['owner_mobile']

    if not is_valid_mobile_number(mobile):
        messages.error(req, f"Invalid Mobile Number Format: {mobile}")
        return redirect('/owner/')

    if 'user_login_id' in req.session:
        owner = models.Owner(
            owner_name=req.POST['owner_name'],
            owner_mobile=req.POST['owner_mobile'],
            owner_type=req.POST['owner_type'],
            owner_address=req.POST['owner_address']
        )
        owner.save()
        return redirect('/owner/')
    else:
        return redirect('/login/')
    
def show_owner(req):
    if 'user_login_id' in req.session:
        owners = models.Owner.objects.all()
        return render(req,'show_owner.html', {'owners':owners})
    else:
        return redirect('/login/')


def edit_owner(req):

    if 'user_login_id' in req.session:
        owner_id = req.GET['id']
        owner = models.Owner.objects.get(id=owner_id)
        obj = {'owner': owner}
        return render(req, 'edit_owner.html', obj)
    else:
        return redirect('/login/')


def save_edited_owner(req):

    mobile = req.POST['owner_mobile']

    if not is_valid_mobile_number(mobile):
        messages.error(req, f"Invalid Mobile Number Format: {mobile}")
        return redirect('/owner/')

    owner_id = req.POST['owner_id']
    owner = models.Owner.objects.get(id=owner_id)
    owner.owner_name = req.POST['owner_name']
    owner.owner_mobile = req.POST['owner_mobile']
    owner.owner_address = req.POST['owner_address']
    owner.owner_type = req.POST['owner_type']
    owner.save()
    return redirect('/owner/')


def delete_owner(req):
    if 'user_login_id' in req.session:
        models.Owner.objects.get(id=req.GET['id']).delete()
        return redirect('/owner/')
    else:
        return redirect('/login/')
################################################################################################################################################################
# Vehicle


def vehicle(req):
    if 'user_login_id' in req.session:
        # Object Bhejna Hai
        vehicles = models.Vehicle.objects.all()
        vehicle_types = models.VehicleType.objects.all()
        obj = {'vehicles': vehicles, 'vehicle_types': vehicle_types}
        return render(req, 'vehicle.html', obj)
    else:
        return redirect('/login/')


def save_vehicle_type(req):

    type = models.VehicleType(
        vehicle_type=req.POST['vehicle_type']
    )
    type.save()
    return redirect('/vehicle/')


def is_valid_vehicle_number(number):
    # Example pattern: MH 12 AB 1234 or DL 01 C AA 1111
    pattern = r'^[A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,2}\s?\d{4}$'
    return re.match(pattern, number)


def save_vehicle(req):
    vehicle_number = req.POST['vehicle_number']

    if not is_valid_vehicle_number(vehicle_number):
        messages.error(req, f"Invalid Vehicle Number Format: {vehicle_number}")
        return redirect('/vehicle/')

    owner = models.Owner.objects.filter(
        owner_name=req.POST['owner_name'],
        owner_mobile=req.POST['owner_mobile']
    )

    if len(owner) == 1:
        vehicle = models.Vehicle(
            owner=owner.first(),
            vehicle_number=vehicle_number,
            vehicle_type=models.VehicleType.objects.get(
                id=req.POST['vehicle_type']),
            balance_amount=req.POST['balance_amount']
        )
        vehicle.save()
        return redirect('/vehicle/')
    else:
        messages.error(
            req, f"No owner exists with name {req.POST['owner_name']}")
        return redirect('/vehicle/')
    

def show_vehicle(req):
    if 'user_login_id' in req.session:
        vehicles = models.Vehicle.objects.all()
        return render(req, 'show_vehicle.html', {'vehicles':vehicles})
    else:
        return redirect('/login/')


def edit_vehicle(req):

    if 'user_login_id' in req.session:
        vehicle_id = req.GET['id']
        vehicle = models.Vehicle.objects.get(id=vehicle_id)
        vehicle_types = models.VehicleType.objects.all()
        obj = {"vehicle": vehicle, 'vehicle_types': vehicle_types}
        return render(req, 'edit_vehicle.html', obj)
    else:
        return redirect('/login/')


def save_edited_vehicle(req):
    owner = models.Owner.objects.filter(
        owner_name=req.POST['owner_name'],
        owner_mobile=req.POST['owner_mobile']
    )
    if (len(owner) == 1):
        vehicle_id = req.POST['vehicle_id']
        vehicle = models.Vehicle.objects.get(id=vehicle_id)
        vehicle.vehicle_number = req.POST['vehicle_number']
        vehicle.vehicle_type = models.VehicleType.objects.get(
            id=req.POST['vehicle_type'])
        vehicle.owner = models.Owner.objects.get(
            owner_mobile=req.POST['owner_mobile'])
        vehicle.save()
        return redirect('/vehicle/')
    else:
        return HttpResponse(f"No owner exist of name {req.POST['owner_name']}")


def delete_vehicle(req):
    if 'user_login_id' in req.session:
        models.Vehicle.objects.get(id=req.GET['id']).delete()
        return redirect('/vehicle/')
    else:
        return redirect('/login/')


def get_all_vehicle(req):
    if 'user_login_id' in req.session:
        print(req.GET['id'])
        id = req.GET['id']
        vehicles = list(models.Vehicle.objects.filter(
            vehicle_type=id).values())
        print(vehicles)
        obj = {'vehicles': vehicles}
        return JsonResponse(obj)
    else:
        return redirect('/login/')


#################################################################################################################################################################
# Booking
def booking(req):

    if 'user_login_id' in req.session:
        # Party
        partys = models.Party.objects.all()

        # Vehicle
        vehicles = models.Vehicle.objects.all()

        # VehicleType
        vehicle_types = models.VehicleType.objects.all()

        # State
        states = models.State.objects.all()

        bookings = models.Booking.objects.all()

        obj = {
            'partys': partys, 'vehicles': vehicles,
            'vehicle_types': vehicle_types, 'states': states, 'bookings': bookings
        }

        return render(req, 'booking.html', obj)
    else:
        return redirect('/login/')


def is_valid_utr_number(utr):
    pattern = r'^\d{12,22}$'
    return re.match(pattern, utr)


def is_valid_transaction_id(txn_id):
    pattern = r'^[A-Z0-9]{12,30}$'
    return re.match(pattern, txn_id)


def save_booking(req):

    print(req.POST['total_balance_amount_to_send_to_vehicle_owner'])
    print(req.POST)

    utr = req.POST['utr']
    txn_id = req.POST['transaction_id']

    if not is_valid_utr_number(utr):
        messages.error(req, f"Invalid UTR Number: {utr}")
        return redirect('/booking/')

    if not is_valid_transaction_id(txn_id):
        messages.error(req, f"Invalid Transaction ID: {txn_id}")
        return redirect('/booking/')

    print(req.POST)

    booking = models.Booking(

        booking_number=req.POST['booking_number'],

        booking_date=req.POST['booking_date'],
        party=models.Party.objects.get(id=req.POST['party']),
        vehicle_type=models.VehicleType.objects.get(
            id=req.POST['vehicle_type']),
        vehicle=models.Vehicle.objects.get(id=req.POST['vehicle']),
        loading_date=req.POST['loading_date'],
        unloading_date=req.POST['unloading_date'],
        from_city=req.POST['from_city'],
        to_city=req.POST['to_city'],
        total_hire=req.POST['total_hire'],
        advance_amount=req.POST['advance_amount'],
        balance_amount=req.POST['balance_amount'],
        commission=req.POST['commission'],
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        local=req.POST['local'],
        hamali=req.POST['hamali'],
        tds=req.POST['tds'],
        st_charges=req.POST['st_charges'],
        other_charges=req.POST['other_charges'],
        remark=req.POST['remark'],
        sub_total=req.POST['sub_total'],
        previous_amount=req.POST['previous_amount'],
        pending_amount=req.POST['pending_amount'],
        total_hire_to_pay_to_vehicle=req.POST['total_hire_to_pay_to_vehicle'],
        advance_amount_to_paid_to_vehicle=req.POST['advance_amount_to_paid_to_vehicle'],
        balance_amount_to_pay_to_vehicle=req.POST['balance_amount_to_pay_to_vehicle']
    )
    booking.save()

    party = models.Party.objects.get(id=req.POST['party'])
    party.party_pending_amt = req.POST['pending_amount']
    party.save()
    print(party.party_pending_amt)

    vehicle = models.Vehicle.objects.get(id=req.POST['vehicle'])
    vehicle.balance_amount = req.POST['total_balance_amount_to_send_to_vehicle_owner']
    vehicle.save()
    print(vehicle.balance_amount)

    payment_recived = models.PaymentRecived(
        party=models.Party.objects.get(id=req.POST['party']),
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        total=req.POST['advance_amount'],
        previous_amount=req.POST['previous_amount'],
        pending_amount=req.POST['pending_amount'],
        date=req.POST['booking_date']
    )

    payment_recived.save()

    payment_sent = models.PaymentSent(
        vehicle_type=models.VehicleType.objects.get(
            id=req.POST['vehicle_type']),
        vehicle=models.Vehicle.objects.get(id=req.POST['vehicle']),
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        total=req.POST['advance_amount'],
        previous_amount=req.POST['amount_to_send_vehicle_owner'],
        balance_amount=req.POST['total_balance_amount_to_send_to_vehicle_owner'],
        date=req.POST['booking_date']
    )
    payment_sent.save()

    return redirect('/booking/')


def show_booking(req):
    if 'user_login_id' in req.session:
        bookings = models.Booking.objects.all()
        return render(req, 'show_booking.html', {'bookings':bookings})
    else:
        return redirect('/login/')


def edit_booking(req):

    if 'user_login_id' in req.session:
        # Party
        partys = models.Party.objects.all()

        # Vehicle
        vehicles = models.Vehicle.objects.all()

        # VehicleType
        vehicle_types = models.VehicleType.objects.all()

        # State
        states = models.State.objects.all()

        booking_id = req.GET['id']

        booking = models.Booking.objects.get(id=booking_id)

        obj = {
            'partys': partys, 'vehicles': vehicles, 'vehicle_types': vehicle_types, 'states': states, 'booking': booking
        }
        
        return render(req, "edit_booking.html", obj)

    else:
        return redirect('/login/')


def save_edited_booking(req):

    booking_number=req.POST['booking_number'],

    booking_id = req.POST['booking_id']
    booking = models.Booking.objects.get(id=booking_id)
    booking.booking_date = req.POST['booking_date']
    booking.party = models.Party.objects.get(id=req.POST['party'])
    booking.vehicle_type = models.VehicleType.objects.get(
        id=req.POST['vehicle_type'])
    booking.vehicle = models.Vehicle.objects.get(id=req.POST['vehicle'])
    booking.loading_date = req.POST['loading_date']
    booking.unloading_date = req.POST['unloading_date']
    booking.from_city = req.POST['from_city']
    booking.to_city = req.POST['to_city']
    booking.total_hire = req.POST['total_hire']
    booking.advance_amount = req.POST['advance_amount']
    booking.balance_amount = req.POST['balance_amount']
    booking.commission = req.POST['commission']
    booking.cash = req.POST['cash']
    booking.online = req.POST['online']
    booking.transaction_id = req.POST['transaction_id']
    booking.utr = req.POST['utr']
    booking.local = req.POST['local']
    booking.hamali = req.POST['hamali']
    booking.tds = req.POST['tds']
    booking.st_charges = req.POST['st_charges']
    booking.other_charges = req.POST['other_charges']
    booking.remark = req.POST['remark']
    booking.sub_total = req.POST['sub_total']
    booking.previous_amount = req.POST['previous_amount']
    booking.pending_amount = req.POST['pending_amount']
    booking.total_hire_to_pay_to_vehicle = req.POST['total_hire_to_pay_to_vehicle']
    booking.advance_amount_to_paid_to_vehicle = req.POST['advance_amount_to_paid_to_vehicle']
    booking.balance_amount_to_pay_to_vehicle = req.POST['balance_amount_to_pay_to_vehicle']

    booking.save()

    party = models.Party.objects.get(id=req.POST['party'])
    party.party_pending_amt = req.POST['pending_amount']
    party.save()
    print(party.party_pending_amt)

    vehicle = models.Vehicle.objects.get(id=req.POST['vehicle'])
    vehicle.balance_amount = req.POST['balance_amount_to_pay_to_vehicle']
    vehicle.save()
    print(vehicle.balance_amount)

    payment_recived = models.PaymentRecived(
        party=models.Party.objects.get(id=req.POST['party']),
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        total=req.POST['advance_amount'],
        previous_amount=req.POST['previous_amount'],
        pending_amount=req.POST['pending_amount'],
        date=req.POST['date']
    )
    payment_recived.save()

    payment_sent = models.PaymentSent(
        vehicle_type=models.VehicleType.objects.get(
            id=req.POST['vehicle_type']),
        vehicle=models.Vehicle.objects.get(id=req.POST['vehicle']),
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        total=req.POST['advance_amount'],
        previous_amount=req.POST['previous_amount'],
        pending_amount=req.POST['total_balance_amount_to_send_to_vehicle_owner'],
        date=req.POST['date']
    )
    payment_sent.save()

    return redirect('/booking/')


def delete_booking(req):
    if 'user_login_id' in req.session:
        booking = models.Booking.objects.get(id=req.GET['id'])

        party_id = booking.party.id
        party = models.Party.objects.get(id=party_id)
        party.save()

        vehicle_id = booking.vehicle.id
        vehicle = models.Vehicle.objects.get(id=vehicle_id)
        vehicle.save()

        models.Booking.objects.get(id=req.GET['id']).delete()
        return redirect('/booking/')
    else:
        return redirect('/login/')


#######################################################################################################################################################################################


def add_city(req):
    if 'user_login_id' in req.session:
        states = models.State.objects.all()
        citys = models.City.objects.all()
        return render(req, 'add_city.html', {'states': states, 'citys': citys})
    else:
        return redirect('/login/')


def save_state(req):
    state = models.State(
        state_name=req.POST['state_name']
    )
    state.save()
    return redirect('/add_city/')


def save_city(req):
    city = models.City(
        city_name=req.POST['city_name'],
        state=models.State.objects.get(id=req.POST['state'])
    )
    city.save()
    return redirect('/add_city/')


def get_all_city(req):
    if 'user_login_id' in req.session:
        id = req.GET['id']
        citys = list(models.City.objects.filter(state=id).values())
        print(citys)
        obj = {'citys': citys}
        return JsonResponse(obj)
    else:
        return redirect('/login/')


def get_previous_amount(req):
    if 'user_login_id' in req.session:
        id = req.GET['id']
        party = models.Party.objects.get(id=id)
        obj = {'party': party}
        return JsonResponse({
            'party': {
                'pending_amount': party.party_pending_amt
            }
        })
    else:
        return redirect('/login/')


def get_previous_amount_to_send_vehicle_owner(req):
    if 'user_login_id' in req.session:
        id = req.GET['id']
        vehicle = models.Vehicle.objects.get(id=id)
        obj = {'vehicle': vehicle}
        return JsonResponse(
            {
                'vehicle': {
                    'pending_amount': vehicle.balance_amount
                }
            }
        )
    else:
        return redirect('/login/')


##################################################################################################################################################################################################################################################
# Payment Recived
def payment_recived(req):
    if 'user_login_id' in req.session:
        # Party
        partys = models.Party.objects.all()

        # Payment Recived
        payment_reciveds = models.PaymentRecived.objects.all()

        obj = {'partys': partys, 'payment_reciveds': payment_reciveds}

        return render(req, 'payment_recived.html', obj)
    else:
        return redirect('/login/')


def save_payment_recived(req):
    payment_recived = models.PaymentRecived(
        booking_number=req.POST['booking_number'],
        party=models.Party.objects.get(id=req.POST['party']),
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        total=req.POST['total'],
        previous_amount=req.POST['previous_amount'],
        pending_amount=req.POST['pending_amount'],
        date=req.POST['date']
    )
    payment_recived.save()

    party = models.Party.objects.get(id=req.POST['party'])
    party.party_pending_amt = req.POST['pending_amount']
    party.save()

    return redirect('/payment_recived/')


def show_payment_recived(req):
    if 'user_login_id' in req.session:
        payment_reciveds = models.PaymentRecived.objects.all()
        return render(req, 'show_payment_recived.html', {'payment_reciveds':payment_reciveds})
    else:
        return redirect('/login/')

def edit_payment_recived(req):
    payment_recived = models.PaymentRecived.objects.get(id=req.GET['id'])

    partys = models.Party.objects.all()


    # Getting Previous Party using payment_recived
    previous_party = payment_recived.party

    # Getting Previous Amount using payment_recived
    previous_amount = payment_recived.previous_amount

    print(previous_party.party_pending_amt)

    previous_party.party_pending_amt = previous_amount

    previous_party.save()

    return render(req,'edit_payment_recived.html', {'payment_recived':payment_recived, 'partys':partys})



def save_edited_payment_recived(req):

    payment_recived = models.PaymentRecived.objects.get(id=req.POST['payment_recived_id'])

    print(req.POST['party'])

    payment_recived.booking_number=req.POST['booking_number']
    payment_recived.party=models.Party.objects.get(id=req.POST['party'])
    payment_recived.cash=req.POST['cash']
    payment_recived.online=req.POST['online']
    payment_recived.transaction_id=req.POST['transaction_id']
    payment_recived.utr=req.POST['utr']
    payment_recived.total=req.POST['total']
    payment_recived.previous_amount=req.POST['previous_amount']
    payment_recived.pending_amount=req.POST['pending_amount']
    payment_recived.date=req.POST['date']

    payment_recived.save()

    party = models.Party.objects.get(id=req.POST['party'])
    party.party_pending_amt = req.POST['pending_amount']
    party.save()

    return redirect('/payment_recived/')


def delete_payment_recived(req):
    if 'user_login_id' in req.session:
        payment_recived = models.PaymentRecived.objects.get(id=req.GET['id'])

        party_id = payment_recived.party.id

        # Jiss se paise liye the unko vapas krdo
        party = models.Party.objects.get(id=party_id)
        party.party_pending_amt = payment_recived.previous_amount
        party.save()

        # Save the Deleting payment_recived
        deleted_payment_recived = models.DeletedPaymentRecived(
            booking_number = payment_recived.booking_number,
            party = payment_recived.party,
            cash = payment_recived.cash,
            online = payment_recived.online,
            transaction_id = payment_recived.transaction_id,
            utr = payment_recived.utr,
            total = payment_recived.total,
            previous_amount = payment_recived.previous_amount,
            pending_amount = payment_recived.pending_amount,
            date = payment_recived.date
        )

        deleted_payment_recived.save()

        models.PaymentRecived.objects.get(id=req.GET['id']).delete()
        return redirect('/payment_recived/')
    else:
        return redirect('/login/')


#####################################################################################################################################################################################
# Payment Sent


def payment_sent(req):

    if 'user_login_id' in req.session:
        # Vehicle Type
        vehicle_types = models.VehicleType.objects.all()

        # Vehicles
        vehicles = models.Vehicle.objects.all()

        # Payment Sent
        payment_sents = models.PaymentSent.objects.all()

        obj = {'vehicle_types': vehicle_types,
               'vehicles': vehicles, 'payment_sents': payment_sents}
        return render(req, 'payment_sent.html', obj)
    else:
        return redirect('/login/')


def save_payment_sent(req):
    payment_sent = models.PaymentSent(
        booking_number=req.POST['booking_number'],
        vehicle_type=models.VehicleType.objects.get(
            id=req.POST['vehicle_type']),
        vehicle=models.Vehicle.objects.get(id=req.POST['vehicle']),
        cash=req.POST['cash'],
        online=req.POST['online'],
        transaction_id=req.POST['transaction_id'],
        utr=req.POST['utr'],
        total=req.POST['total'],
        previous_amount=req.POST['amount_to_send_vehicle_owner'],
        balance_amount=req.POST['pending_amount'],
        date=req.POST['date']
    )
    payment_sent.save()

    vehicle = models.Vehicle.objects.get(id=req.POST['vehicle'])
    vehicle.balance_amount = req.POST['pending_amount']
    vehicle.save()

    return redirect('/payment_sent/')


def show_payment_sent(req):
    if 'user_login_id' in req.session:
        payment_sents = models.PaymentSent.objects.all()
        return render(req, 'show_payment_sent.html', {'payment_sents':payment_sents})
    else:
        return redirect('/login/')

def edit_payment_sent(req):
    
    payment_sent = models.PaymentSent.objects.get(id=req.GET['id'])

    # Getting Previous Vehicle using payment_sent
    previous_vehicle = payment_sent.vehicle

    print(f"{previous_vehicle.balance_amount} -->> {payment_sent.previous_amount}")

    # Changing the balance_amount of previous vehicle
    previous_vehicle.balance_amount = payment_sent.previous_amount

    print(f"{previous_vehicle.balance_amount} -->> {payment_sent.previous_amount}")

    previous_vehicle.save()

    # All VehicleTypes
    vehicle_types = models.VehicleType.objects.all()

    return render(req,'edit_payment_sent.html', {'payment_sent':payment_sent, 'vehicle_types':vehicle_types})



def save_edited_payment_sent(req):
    
    payment_sent = models.PaymentSent.objects.get(id=req.POST['payment_sent_id'])

    payment_sent.booking_number=req.POST['booking_number']
    payment_sent.vehicle_type=models.VehicleType.objects.get(id=req.POST['vehicle_type'])
    payment_sent.vehicle=models.Vehicle.objects.get(id=req.POST['vehicle'])
    payment_sent.cash=req.POST['cash']
    payment_sent.online=req.POST['online']
    payment_sent.transaction_id=req.POST['transaction_id']
    payment_sent.utr=req.POST['utr']
    payment_sent.total=req.POST['total']
    payment_sent.previous_amount=req.POST['amount_to_send_vehicle_owner']
    payment_sent.balance_amount=req.POST['pending_amount']
    payment_sent.date=req.POST['date']
    
    payment_sent.save()

    return redirect('/payment_sent/')

def delete_payment_sent(req):

    if 'user_login_id' in req.session:
        payment_sent = models.PaymentSent.objects.get(id=req.GET['id'])

        vehicle_id = payment_sent.vehicle.id

        vehicle = models.Vehicle.objects.get(id=vehicle_id)

        # JissKO paise bheje the uss se paise vapas lelo
        vehicle.balance_amount = payment_sent.previous_amount
        vehicle.save()

        # Store the deleting payment into DeletedPaymentSent
        deleted_payment_sent = models.DeletedPaymentSent(
            booking_number = payment_sent.booking_number,
            vehicle_type = payment_sent.vehicle_type,
            vehicle = payment_sent.vehicle,
            cash = payment_sent.cash,
            online = payment_sent.online,
            transaction_id = payment_sent.transaction_id,
            utr = payment_sent.utr,
            total = payment_sent.total,
            previous_amount = payment_sent.previous_amount,
            balance_amount = payment_sent.balance_amount,
            date = payment_sent.date
        )
        deleted_payment_sent.save()

        models.PaymentSent.objects.get(id=req.GET['id']).delete()
        return redirect('/payment_sent/')
    else:
        return redirect('/login/')


##############################################################################################################################################################################################################################

def alert_payment_pending_by_party(req):

    if 'user_login_id' in req.session:
        pendings = models.Party.objects.filter(party_pending_amt__gt=0)
        return render(req, 'alert_recive.html', {'pendings': pendings})
    else:
        return redirect('/login/')


def alert_payment_send_to_vehicle(req):

    if 'user_login_id' in req.session:
        sends = models.Vehicle.objects.filter(balance_amount__gt=0)
        return render(req, 'alert_send.html', {'sends': sends})
    else:
        return redirect('/login/')


# views.py


def download_party_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Party Details"

    # Headers
    headers = ['Name', 'Email', 'Mobile', 'Address',
               'City', 'GST Number', 'Pending Amount']
    ws.append(headers)

    # Data rows
    parties = Party.objects.all()
    for party in parties:
        ws.append([
            party.party_name,
            party.party_email,
            party.party_mobile,
            party.party_address,
            party.party_city,
            party.party_gst_number,
            party.party_pending_amt
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=party_details.xlsx'
    wb.save(response)
    return response


def payment_sent_view(request):
    filters = {}

    # Grab each filter from GET parameters if present
    if request.GET.get('booking_number'):
        filters['booking_number__icontains'] = request.GET['booking_number']
    if request.GET.get('booking_date'):
        filters['booking_date'] = request.GET['booking_date']
    if request.GET.get('vehicle_type'):
        filters['vehicle_type__icontains'] = request.GET['vehicle_type']
    if request.GET.get('vehicle_number'):
        filters['vehicle_number__icontains'] = request.GET['vehicle_number']
    if request.GET.get('cash'):
        filters['cash'] = request.GET['cash']
    if request.GET.get('online'):
        filters['online'] = request.GET['online']
    if request.GET.get('transaction_id'):
        filters['transaction_id__icontains'] = request.GET['transaction_id']
    if request.GET.get('utr'):
        filters['utr__icontains'] = request.GET['utr']
    if request.GET.get('total_received'):
        filters['total_received'] = request.GET['total_received']
    if request.GET.get('previous_amount'):
        filters['previous_amount'] = request.GET['previous_amount']
    if request.GET.get('pending_amount'):
        filters['pending_amount'] = request.GET['pending_amount']

    # Apply all active filters at once
    payments = PaymentSent.objects.filter(**filters)

    return render(request, 'your_template.html', {'payments': payments})

